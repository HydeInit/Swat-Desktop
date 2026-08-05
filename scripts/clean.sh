#!/bin/sh
# Remove build artifacts (chroot, binary) so the next build starts fresh.
# By default this keeps live-build's cache/ (bootstrap + downloaded .debs),
# so package-list/hook changes rebuild fast. Pass --purge for a full wipe
# (e.g. after changing distribution/architecture in auto/config).
set -e

cd "$(dirname "$0")/.."

if [ "$1" = "--purge" ] || [ "$1" = "-p" ]; then
	sudo lb clean --purge
else
	sudo lb clean
fi
