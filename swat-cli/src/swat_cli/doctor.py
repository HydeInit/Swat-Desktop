"""Read-only system diagnostics: disk space, package state, firmware/driver
binding, XFCE config sanity, and broken symlinks. No checks here modify the
system."""

from __future__ import annotations

import dataclasses
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Device classes where a missing driver usually means missing firmware,
# not an intentionally-unbound bridge/host controller.
FIRMWARE_RELEVANT_CLASSES = (
    "Network controller",
    "VGA compatible controller",
    "Audio device",
    "3D controller",
)

SYMLINK_SCAN_ROOTS = (
    Path("/etc"),
    Path("/usr/share/applications"),
    Path("/etc/xdg/autostart"),
)


@dataclasses.dataclass
class CheckResult:
    name: str
    status: str  # "ok", "warn", or "error"
    message: str


def check_disk_space() -> list[CheckResult]:
    results = []
    seen_devices = set()
    for line in Path("/proc/mounts").read_text().splitlines():
        parts = line.split()
        if len(parts) < 3:
            continue
        device, mountpoint = parts[0], parts[1]
        if not device.startswith("/dev/") or device in seen_devices:
            continue
        seen_devices.add(device)
        try:
            usage = shutil.disk_usage(mountpoint)
        except OSError:
            continue
        pct = usage.used / usage.total * 100 if usage.total else 0
        if pct >= 98:
            status = "error"
        elif pct >= 90:
            status = "warn"
        else:
            status = "ok"
        results.append(CheckResult(
            name=f"disk-space:{mountpoint}",
            status=status,
            message=f"{mountpoint} ({device}) is {pct:.0f}% full",
        ))
    return results


def check_package_state() -> list[CheckResult]:
    try:
        proc = subprocess.run(
            ["dpkg", "--audit"], capture_output=True, text=True, timeout=15
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return [CheckResult("package-state", "error", f"could not run dpkg --audit: {exc}")]
    if proc.stdout.strip():
        return [CheckResult(
            "package-state", "warn",
            "dpkg reports packages in an inconsistent state (run: dpkg --audit)",
        )]
    return [CheckResult("package-state", "ok", "no broken or half-configured packages")]


def check_firmware_binding() -> list[CheckResult]:
    try:
        proc = subprocess.run(
            ["lspci", "-k"], capture_output=True, text=True, timeout=15
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return [CheckResult("firmware-binding", "warn", f"could not run lspci: {exc}")]

    unbound = []
    for block in proc.stdout.split("\n\n"):
        lines = block.strip().splitlines()
        if not lines:
            continue
        header = lines[0]
        if "Kernel driver in use:" in block:
            continue
        if any(cls in header for cls in FIRMWARE_RELEVANT_CLASSES):
            unbound.append(header.split(": ", 1)[-1] if ": " in header else header)

    if unbound:
        return [CheckResult(
            "firmware-binding", "warn",
            f"{len(unbound)} device(s) with no driver bound (possibly missing firmware): "
            + "; ".join(unbound),
        )]
    return [CheckResult("firmware-binding", "ok", "all network/graphics/audio devices have a driver bound")]


def check_xfce_config() -> list[CheckResult]:
    home = Path(os.environ.get("HOME", f"/home/{os.environ.get('USER', '')}"))
    xfce_dir = home / ".config" / "xfce4"
    if not xfce_dir.is_dir():
        return [CheckResult(
            "xfce-config", "warn",
            f"{xfce_dir} does not exist (first login not completed, or not run as the desktop user?)",
        )]
    try:
        proc = subprocess.run(
            ["xfconf-query", "-c", "xfce4-session", "-l"],
            capture_output=True, text=True, timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return [CheckResult("xfce-config", "warn", f"could not query xfconf: {exc}")]
    if proc.returncode != 0:
        return [CheckResult(
            "xfce-config", "warn",
            "xfconf-query could not reach the xfce4-session channel (session bus not running?)",
        )]
    return [CheckResult("xfce-config", "ok", "xfce config directory present and xfconf reachable")]


def _find_broken_symlinks(root: Path) -> list[str]:
    # os.scandir's DirEntry caches is_symlink() from the directory read
    # itself, avoiding a separate lstat per entry; exists() (which follows
    # the link) is only called for entries actually flagged as symlinks,
    # not every file in the tree.
    broken = []
    try:
        entries = list(os.scandir(root))
    except OSError:
        return broken
    for entry in entries:
        if entry.is_symlink():
            if not os.path.exists(entry.path):
                broken.append(entry.path)
        elif entry.is_dir(follow_symlinks=False):
            broken.extend(_find_broken_symlinks(Path(entry.path)))
    return broken


def check_broken_symlinks() -> list[CheckResult]:
    broken = []
    for root in SYMLINK_SCAN_ROOTS:
        if root.is_dir():
            broken.extend(_find_broken_symlinks(root))
    if broken:
        shown = broken[:10]
        more = f" (+{len(broken) - 10} more)" if len(broken) > 10 else ""
        return [CheckResult(
            "broken-symlinks", "warn",
            f"{len(broken)} broken symlink(s): " + ", ".join(shown) + more,
        )]
    return [CheckResult(
        "broken-symlinks", "ok",
        f"no broken symlinks found under {', '.join(str(r) for r in SYMLINK_SCAN_ROOTS)}",
    )]


ALL_CHECKS = (
    check_disk_space,
    check_package_state,
    check_firmware_binding,
    check_xfce_config,
    check_broken_symlinks,
)


def run_all() -> list[CheckResult]:
    # Checks are independent and I/O-bound (subprocess waits, disk walks) -
    # run them concurrently so total time is roughly the slowest check
    # rather than the sum of all of them.
    with ThreadPoolExecutor(max_workers=len(ALL_CHECKS)) as pool:
        results_per_check = pool.map(lambda check: check(), ALL_CHECKS)
    return [result for results in results_per_check for result in results]
