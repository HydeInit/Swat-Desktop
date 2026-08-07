# SWAT Welcome

First-boot welcome experience, built with Tauri. Static UI scaffold only
right now - five screens (Welcome, Customisations, Recommended installs,
Installing, Finish), navigable, on-brand, no install logic wired up.
Nothing here actually installs anything yet.

See issue #19 for what's still needed: real catalog data, the install
engine, polkit wiring, the first-boot trigger, packaging, and ISO
integration.

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
