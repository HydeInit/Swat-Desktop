# Contributing to SWAT

Thanks for your interest in contributing. This project is a Debian remaster built with `live-build`, so most contributions fall into a few categories: package selection, build configuration, branding/theming, and documentation.

Please read the [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## Before you start

For anything beyond a small fix (typos, broken links, obvious bugs), please open an issue first to discuss the change. This avoids wasted effort on pull requests that don't fit the project's direction.

## Development environment

`live-build` and its dependencies (`debootstrap`, `squashfs-tools`, `xorriso`, `isolinux`) only run on Linux. You'll need a native Linux machine, WSL2, or a Linux VM. See the main [README](README.md) for the full list of prerequisites.

## Making a change

1. Fork the repo and create a branch off `master`.
2. Edit the relevant files under `config/` (package lists, includes, hooks) — see the `README.md` in each subdirectory for what belongs where.
3. Build locally and confirm it produces a bootable ISO:
   ```sh
   ./scripts/build.sh
   ./scripts/test-in-qemu.sh
   ```
4. Commit your changes with a clear message describing *why*, not just *what*.
5. Open a pull request against `master`. CI will run a full build — a PR won't be merged unless it passes.

## Pull request guidelines

- Keep PRs focused on a single change; split unrelated changes into separate PRs.
- Update the relevant `README.md` if you're changing what a directory contains or how the build behaves.
- If you're adding packages, briefly explain why in the PR description — it helps keep the package list intentional rather than accumulating cruft.

## Reporting bugs / requesting features

Use the issue templates when opening a new issue — they help make sure we get the information needed to reproduce a problem or evaluate a request.
