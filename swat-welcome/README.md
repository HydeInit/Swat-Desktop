# swat-welcome

Prototype of SWAT's first-run profile selection experience. Reads
development profiles (`profiles/` at the repo root), lets you pick some,
and shows a dry-run plan of what would be set up.

**Installs nothing.** No subprocess calls, no system changes, no
privilege escalation - this is a UI/UX preview of the profile-selection
flow, not a working installer. See `docs/IDEAS.md`'s "SWAT Welcome
Application" section for the full planned scope (browser choice, git
config, SSH key setup, etc.) - only the welcome + profile-selection +
dry-run-plan pages exist so far.

## Install (development)

Requires `swat-cli` installed in the same environment (profile loading
is shared, not duplicated):

```
pip install -e ../swat-cli -e .
swat-welcome
```
