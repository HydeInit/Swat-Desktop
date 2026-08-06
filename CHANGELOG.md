# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.1.0] - 2026-08-06

### Added
- `live-build` configuration targeting Debian 13 (trixie), amd64
- Base package selection: system essentials, XFCE desktop, developer tooling (`ripgrep`, `fd-find`, `fzf`, `jq`, `tree`, etc.)
- Default locale (`en_US.UTF-8`) and timezone (UTC) for the live session
- `avahi-daemon` and `ModemManager` disabled by default (no hardware to back them)
- Installer preseed defaults for locale/timezone
- SWAT branding: desktop wallpaper, Plymouth boot splash, GRUB background, `/etc/os-release`/`lsb-release`/hostname/login banner
- Non-free firmware support (`non-free-firmware` archive component + dedicated firmware package list) for real WiFi/GPU/audio hardware
- Calamares graphical installer, supporting both BIOS and UEFI target installs from a single image, dual-boot capable alongside an existing OS
- GitHub Actions workflow building a full ISO on every push/PR, with caching
- Contributor docs: `CONTRIBUTING.md`, issue/PR templates, `SECURITY.md`, `CODEOWNERS`
- CI hardening: SHA-pinned GitHub Actions, minimal `permissions:` blocks, concurrency cancellation, privileged ISO build gated behind a required-reviewer environment for pull requests
- `packaging/`: Debian-native `.deb` packaging, validated end to end with a minimal `swat-branding` package (build, sign, publish, install)
- `swat-cli`: `swat doctor` read-only diagnostics (disk space, package state, firmware/driver binding, XFCE config sanity, broken symlinks), human and JSON output
- Release metadata baked into every build (`/etc/swat-release`, `usr/share/swat/build-info.json`): version, Debian base, git commit, build date
- `scripts/verify-iso.sh`: sanity-checks a built ISO (size, checksum, live filesystem presence) before treating it as a valid artifact
- `docs/hardware-test-matrix.md`, open for outside hardware-tester contributions via the hardware-test-report issue template

### Fixed
- Desktop wallpaper not applying on login - autostart script now detects the actual connected display output rather than assuming a fixed name
- GRUB not listing other installed operating systems for dual-boot - Debian's default GRUB config silently disables `os-prober` even when it's installed; now force-enabled at build time
