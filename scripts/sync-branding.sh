#!/bin/sh
# branding/ is the single source of truth for these assets - copies them
# into the live-build tree and packaging/ locations that consume them.
# Run before building the ISO (scripts/build.sh does this automatically)
# or before building packaging/swat-branding's .deb (dpkg-buildpackage
# doesn't call build.sh, so run this manually first).
set -e

cd "$(dirname "$0")/.."

copy() {
	echo "  $1 -> $2"
	cp "$1" "$2"
}

echo "Syncing branding assets..."
copy branding/wallpaper/wallpaper.png config/includes.chroot_after_packages/usr/share/backgrounds/swat/wallpaper.png
copy branding/wallpaper/wallpaper.png packaging/swat-branding/usr/share/backgrounds/swat/wallpaper.png
copy branding/calamares/logo.png config/includes.chroot_after_packages/etc/calamares/branding/swat/logo.png
copy branding/plymouth/swat.script config/includes.chroot_after_packages/usr/share/plymouth/themes/swat/swat.script
copy branding/plymouth/swat.plymouth config/includes.chroot_after_packages/usr/share/plymouth/themes/swat/swat.plymouth
echo "Done."
