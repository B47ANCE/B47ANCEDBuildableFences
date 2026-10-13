# Public source snapshot

Project Version: 1.1.0-dev.6

Initial public source backup requested by the owner on 2026-10-13.
Authoritative source: src/B47ANCEDBuildableFences/42.
Development overlay: prototypes/cohesive/42, composed into the dev.6 candidate.
Mod ID: B47ANCEDBuildableFences. Workshop ID: 3817174798.
Version, gameplay and Workshop metadata are unchanged by this backup.
Runtime is Lua-only; research binaries, generated staging/packages, dependencies,
logs, diagnostic snapshots and linked settings are excluded from Git history.
Selected historical Lua/test fixtures and hashes preserve regression provenance.
Other historical records referenced by the inventory are retained locally.

G6 SP NOT TESTED; G7 dedicated MP BLOCKED / NOT TESTED; stable G8 BLOCKED.
No stable tag, Workshop upload, deployment or game/server launch performed.
Initial bootstrap supplies main. Future iterations require feature branches and
reviewed PRs before merging main.

[TESTED Windows offline, 2026-10-13] Version checker PASS; 26 runnable tests
PASS. Five original-installed-baseline tests remain BLOCKED (download absent).
Commands: scripts/check_versions.py --root .; unittest discover -s tests -p
test_no_testkit.py -v; full discovered suite excluding the five named baseline
methods documented in docs/TEST_KIT_REMOVAL.md. git diff --cached --check PASS.
Staged audit: 241 files, no prohibited paths or suspected credential patterns.
