#!/bin/sh
# Sanity-check a built ISO before treating it as a valid artifact.
# Usage: scripts/verify-iso.sh [path/to/image.iso]
set -e

cd "$(dirname "$0")/.."

# Same "most recent ISO in output/" resolution as test-in-qemu.sh.
iso="$1"
if [ -z "$iso" ]; then
	iso=$(find output -maxdepth 1 -name '*.iso' -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -n1 | cut -d' ' -f2-)
fi

fail=0
note() { echo "  [ok] $1"; }
problem() {
	echo "  [FAIL] $1" >&2
	fail=1
}

if [ -z "$iso" ] || [ ! -f "$iso" ]; then
	echo "No ISO found. Build one first with scripts/build.sh, or pass a path explicitly." >&2
	exit 1
fi
note "ISO exists: $iso"

size=$(stat -c%s "$iso" 2>/dev/null || stat -f%z "$iso")
min_bytes=$((300 * 1024 * 1024))  # 300MB - well under a bare vanilla build
max_bytes=$((4 * 1024 * 1024 * 1024))  # 4GB - generous ceiling before something's clearly wrong
if [ "$size" -lt "$min_bytes" ]; then
	problem "ISO is suspiciously small ($size bytes) - likely a broken/truncated build"
elif [ "$size" -gt "$max_bytes" ]; then
	problem "ISO is suspiciously large ($size bytes) - check for unintended package bloat"
else
	note "ISO size within expected bounds ($size bytes)"
fi

sha_file="$(dirname "$iso")/SHA256SUMS"
if [ -f "$sha_file" ]; then
	if (cd "$(dirname "$iso")" && sha256sum -c "$(basename "$sha_file")" >/dev/null 2>&1); then
		note "checksum matches SHA256SUMS"
	else
		problem "checksum does not match SHA256SUMS"
	fi
else
	echo "  [skip] no SHA256SUMS next to the ISO to verify against"
fi

if command -v isoinfo >/dev/null 2>&1; then
	if isoinfo -i "$iso" -f 2>/dev/null | grep -q '/LIVE/FILESYSTEM.SQUASHFS'; then
		note "live filesystem.squashfs present in ISO"
	else
		problem "live filesystem.squashfs not found in ISO"
	fi
else
	echo "  [skip] isoinfo not installed - install genisoimage to check ISO contents"
fi

if [ "$fail" -eq 0 ]; then
	echo "All checks passed."
else
	echo "One or more checks failed." >&2
	exit 1
fi
