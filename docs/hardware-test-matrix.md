# Hardware test matrix

Real-hardware boot/install reports for SWAT, tracking what's actually
been confirmed working outside a VM. Open for outside hardware-tester
contributions - file a [hardware test report](https://github.com/HydeInit/Swat-Desktop/issues/new?template=hardware-test-report.yml)
and it'll get added to the table below.

| Device | CPU | GPU | Boot mode | Result | Notes | Tester | Date |
|---|---|---|---|---|---|---|---|
| Spare laptop (older model, exact specs TBD) | Unknown | Unknown (integrated) | UEFI | Boots + installs clean | Live boot, WiFi driver/firmware, wallpaper, and display all confirmed working. Installed via Calamares manual partitioning, dual-boot alongside Windows on the internal disk (no spare external drive available) - shrank the Windows partition and added a second EFI System Partition rather than resizing the existing one, kept Windows untouched. Surfaced a real bug: GRUB wasn't listing Windows in the boot menu (`os-prober` silently disabled by Debian's default config) - found, fixed, and verified. Trackpad flakiness observed during testing, but pre-existing/unrelated hardware wear on this specific machine, not an OS issue. | Colin | 2026-08-06 |

## Reading a result

- **Boots + installs clean** - live session boots, installer completes, installed system boots and logs in.
- **Boots, install fails** - live session works but the installer errors out or produces an unbootable system.
- **Doesn't boot** - live session itself fails to boot (worth noting how far it got: BIOS/UEFI splash, boot menu, kernel panic, etc.)

Free-text notes matter more than the result category - driver/firmware
gaps, quirky hardware, and partial failures are exactly what this
matrix exists to catch before a wider release.
