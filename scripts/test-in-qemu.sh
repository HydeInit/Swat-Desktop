#!/bin/sh
# Boot a built SWAT ISO in QEMU for a quick smoke test.
# Usage: scripts/test-in-qemu.sh [path/to/image.iso]
set -e

cd "$(dirname "$0")/.."

iso="$1"
if [ -z "$iso" ]; then
	iso=$(find output -maxdepth 1 -name '*.iso' -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -n1 | cut -d' ' -f2-)
fi

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
