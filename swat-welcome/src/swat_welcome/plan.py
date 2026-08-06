"""Pure dry-run plan building - takes selected profiles and renders what
*would* happen. No subprocess calls, no system changes."""

from __future__ import annotations

from swat_cli.profile import Profile


def build_plan(profiles: list[Profile]) -> str:
    if not profiles:
        return "No profiles selected - nothing would be done."

    lines = ["Dry run - nothing has been installed. This is what would happen:", ""]

    host_packages: list[str] = []
    for p in profiles:
        for pkg in p.host_packages:
            if pkg not in host_packages:
                host_packages.append(pkg)

    if host_packages:
        lines.append(f"Host packages to install: {', '.join(host_packages)}")
        lines.append("")

    for p in profiles:
        lines.append(f"-- {p.name} ({p.id})")
        if p.environment:
            base_image = p.environment.get("base_image", "unspecified")
            env_packages = p.environment.get("packages", [])
            setup_steps = p.environment.get("setup", [])
            lines.append(f"   Container environment based on {base_image}")
            if env_packages:
                lines.append(f"   Container packages: {', '.join(env_packages)}")
            if setup_steps:
                lines.append(f"   Setup steps: {', '.join(setup_steps)}")
        if p.recommended_apps:
            lines.append(f"   Recommended apps (not auto-installed): {', '.join(p.recommended_apps)}")
        lines.append("")

    return "\n".join(lines).rstrip()
