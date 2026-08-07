# SWAT Welcome

First-boot welcome experience, built with Tauri. Five screens (Welcome,
Customisations, Recommended installs, Installing, Finish), with a real
install engine behind it - one executor per install method (apt,
apt+third-party-repo, script, flatpak), streaming output live.

Built and packaged automatically as part of `scripts/build.sh` (dropped
into `config/packages.chroot/`, which live-build installs directly - no
apt repo needed) and launched once per user on first login via the
autostart entry in `config/includes.chroot_after_packages/etc/xdg/autostart/`.

See issue #19 for what's still open: privileged installs need a polkit
authentication agent wired into the live/installed session (added, but
not yet proven against a real login flow), and the catalog itself is a
representative set, not a fully exhaustive one.

## Requirements (Debian trixie, all via apt, no extra repos)

```
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file \
  libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev \
  pkg-config cargo rustc nodejs npm
```

## Develop

```
npm install
npm run tauri dev
```

## Build

```
npm run tauri build
```
