# swat-cli

The `swat` command — system tools for SWAT. First subcommand is `doctor`:
read-only diagnostics, no system changes.

```
swat doctor          # human-readable report
swat doctor --json   # machine-readable report
```

Checks: disk space, broken/half-configured packages (`dpkg --audit`),
network/graphics/audio devices with no driver bound (possible missing
firmware), XFCE config sanity, broken symlinks under `/etc`,
`/usr/share/applications`, and `/etc/xdg/autostart`.

Exit code is the highest-severity result: `0` all checks passed, `1` at
least one warning, `2` at least one error (or a check itself failed to
run).

## Install (development)

```
pip install -e .
```

Requires Python 3.11+ and, for full check coverage, `dpkg`, `lspci`
(`pciutils`), and `xfconf-query` on `PATH` — all present on a SWAT system
by default. Missing tools degrade individual checks to a warning rather
than crashing the run.
