# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `live-build` configuration targeting Debian 13 (trixie), amd64
- Base package selection: system essentials, XFCE desktop, developer tooling (`ripgrep`, `fd-find`, `fzf`, `jq`, `tree`, etc.)
- Default locale (`en_US.UTF-8`) and timezone (UTC) for the live session
- `avahi-daemon` and `ModemManager` disabled by default (no hardware to back them)
- Installer preseed defaults for locale/timezone
- SWAT branding: desktop wallpaper, Plymouth boot splash, GRUB background, `/etc/os-release`/`lsb-release`/hostname/login banner
- GitHub Actions workflow building a full ISO on every push/PR, with caching
- Contributor docs: `CONTRIBUTING.md`, issue/PR templates, `SECURITY.md`
