#!/bin/sh
# Boot a built SWAT ISO in QEMU for a quick smoke test.
# Usage: scripts/test-in-qemu.sh [path/to/image.iso]
set -e

# shellcheck source=scripts/lib.sh
. "$(dirname "$0")/lib.sh"
cd "$(dirname "$0")/.."

iso="${1:-$(latest_iso)}"

if [ -z "$iso" ] || [ ! -f "$iso" ]; then
	echo "No ISO found. Build one first with scripts/build.sh, or pass a path explicitly." >&2
	exit 1
fi

accel="tcg"
[ -e /dev/kvm ] && accel="kvm"

echo "Booting $iso with QEMU (accel=$accel)..."
qemu-system-x86_64 \
	-accel "$accel" \
	-m 2048 \
	-cdrom "$iso" \
	-boot d
