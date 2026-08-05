# Scripts

Helper scripts for driving the build (`build.sh`, `test-in-qemu.sh`, `clean.sh`). `live-build` only runs on Linux, so these are meant to be run from a native Linux machine, WSL2, or a Linux VM — see the main README for prerequisites.

`clean.sh` keeps live-build's `cache/` (the bootstrapped base system and downloaded `.deb`s) by default, so a rebuild after a package-list or hook change only fetches what actually changed. Pass `--purge` for a full wipe, which is only needed after changing the target distribution/architecture in `auto/config`.
