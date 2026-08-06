#!/bin/sh
# Create/update the repo's standard label set. Safe to re-run (updates
# color/description in place rather than failing if a label exists).
# Requires: gh CLI, authenticated with write access to the repo.
set -e

repo="HydeInit/Swat-Desktop"

create() {
	name="$1"
	color="$2"
	desc="$3"
	gh label create "$name" --repo "$repo" --color "$color" --description "$desc" --force
}

create "bug" "d73a4a" "Something isn't working"
create "enhancement" "a2eeef" "New feature or request"
create "documentation" "0075ca" "Docs only"
create "question" "d876e3" "Further information requested"
create "duplicate" "cfd3d7" "Already reported elsewhere"
create "wontfix" "ffffff" "Won't be worked on"
create "invalid" "e4e669" "Not a valid issue as reported"
create "needs-triage" "fbca04" "Not yet reviewed/categorized"
create "good first issue" "7057ff" "Good entry point for new contributors"
create "help wanted" "008672" "Actively looking for a contributor"
create "post-foundation" "bfd4f2" "Backlog - deferred until foundation milestone is done"
create "installer" "c5def5" "Installer / Calamares"
create "branding" "c5def5" "Wallpaper, theme, Plymouth, GRUB"
create "packaging" "c5def5" ".deb packaging / apt repo"
create "cli" "c5def5" "swat-cli / swat-doctor / swat-env"
create "hardware-test" "f9d0c4" "Real-hardware boot/install report"
create "ci" "1d76db" "GitHub Actions / build pipeline"
create "security" "b60205" "Security-relevant change or report"
create "priority-high" "e11d21" "Blocking or urgent"
create "priority-medium" "fbca04" "Normal priority"
create "priority-low" "c2e0c6" "Nice to have, no urgency"

echo "Done."
