# shellcheck shell=sh
# Shared helpers, sourced by other scripts/ - not meant to be run directly.

# Most recently built ISO in output/, or empty if none exists.
latest_iso() {
	find output -maxdepth 1 -name '*.iso' -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -n1 | cut -d' ' -f2-
}
