# Wrought-iron native corner connections

Project Version: 1.1.0-dev.13

Compatible MINOR-scope feature in the existing 1.1.0 prerelease series. The user
explicitly chose vanilla-style junction posts included in paid section costs.
All 21 entity definitions, recipes, tool/consumable amounts, skills, XP, time and
health fields are unchanged. Paid corner/post entries and the gate remain.
No prior object is converted, resprited, repaired, removed or scanned.

## Authority and scope

A server/SP-only wrapper around vanilla buildUtil.checkCorner handles exact
B47 wrought-iron plain/post-ended name, sprite and north/west pairs. The native
builder calls it after adding a successfully paid section. It checks only the
opposite diagonal neighbor and junction square, accepts only same-family
perpendicular sections, and rejects missing/solid/occupied targets and existing
junction/paid post/corner sprites. Unrelated builds keep the original helper.

When eligible it passes a separate descriptor containing corner=fencing_01_69
to the original helper. Native addCorner creates a corner-marked IsoThumpable,
adds it, recalculates neighbors and transmits the complete item. The native
builder/action/cursor and recipes are not mutated. Native-generated posts use
vanilla defaults, not the paid standalone-post entity, and do not match our
standalone-post conversion name allowlist. The existing construction-health
multiplier and paid-piece health are unchanged. No custom commands, client
world writes or permanent custom markers are introduced.

Ownership: server/SP creates the post; vanilla object synchronization/save-load
owns it thereafter. No new schema/migration is needed. Startup/load does not
scan old saves. Like vanilla, removing a leg does not trigger automatic orphan
post cleanup. An existing post prevents another on rebuild. Late-chunk matching
is not deferred: if either square is unavailable, no post is created.
Native persistence, damage/collision and two-client behavior remain runtime gates.

## Server sandbox configuration

B47ANCEDBuildableFences.WroughtIronCornerPosts is a boolean on the existing
sandbox page, default true. Missing older-save values use true; malformed
values disable generation. False prevents future automatic posts and removes
nothing. Existing native vanilla behavior and other families are unaffected.
The overlay composes sandbox-options.txt and 29 Sandbox.json files with the
existing health option preserved exactly. Added name/tooltip values use English
fallback in the existing 29 language folders. No extra health/geometry settings
are exposed; adjacency/orientation/occupancy rules are correctness constraints.

## Historical dev.9 validation and runtime boundary

[TESTED dev.9 Windows offline Python/Lupa, 2026-10-14] 44 available tests PASS, including
7 new native-helper/connection tests. Five original installed-baseline checks
remain BLOCKED because that download is absent. Tests execute the installed
vanilla corner helper with mocked objects, not the game engine. Coverage includes
both approach directions and section types, duplicate prevention, mixed families,
wrong orientation/sprite/class, paid/plain posts, explicit corners, occupied
squares, server-only authority, disabled/missing/invalid configuration, idempotent
installation, unrelated native builds and 29-language configuration fallback.
Full source-contract tests preserve original paid recipes and production code.

Commands from the repository root:
```powershell
$env:PYTHONPATH=(Resolve-Path .test-dependencies).Path
$py='C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $py -m unittest discover -s tests -p test_wrought_iron_connections.py -v
& $py scripts/test_current.py --available
& $py scripts/check_versions.py --root .
& $py scripts/prepare_workshop.py
```

Required native SP and dedicated tests: both placement orders/orientations;
plain/post-ended mixes; double-fire/rebuild; paid posts and corners; adjacent
other families, gates and obstacles; sandbox on/off/older saves; section costs,
tool uses, health and cancellation; generated-post collision, damage/removal;
server restart, late join, reconnect and duplicate prevention after save/load.
G6 NOT TESTED; G7 dedicated BLOCKED / NOT TESTED; stable G8 BLOCKED.
No deployment, packaging, Workshop upload or game/server launch performed.

Existing dev.8 published ZIP/provenance remains untouched. Future authorized
corner candidates use dist/corner-development-current, declared in the version
inventory. The preparer reads that declared output instead of a fixed old path.

[VERIFIED source] Installed vanilla evidence SHA-256:
- media/lua/server/BuildingObjects/ISBuildUtil.lua: `16f0c049ec9a6e7a1f152ed14f5757d43aba65d491b3ece87ca76828eef0becb`
- media/lua/server/BuildingObjects/ISBuildIsoEntity.lua: `6f485b0a90b9b8583fc8112aeddcb3f50a50bf7d1c0c6bc369138ee781deda38`

Exact loaded runtime build UNKNOWN: no game/server launched.

## Additional fence-family connections (dev.10)

Server-owned native junction posts now support military (fencing_01_53),
sloped-top wood (fencing_01_13) and straight-top wood (fencing_01_74), alongside
wrought iron. Only exact same-family perpendicular sections connect; the two
wood styles remain separate. Independent server options MilitaryCornerPosts,
SlopedWoodCornerPosts and StraightWoodCornerPosts default true. Missing old-save
values use true; malformed values disable generation. All paid recipes, costs,
skills, time, health and gates remain unchanged. Security and razor-wire remain
unchanged by explicit user choice: neither has a matching vanilla standalone
post. No retrofit, world scan, orphan cleanup or new client commands.
49 available offline tests pass; five baseline checks remain blocked.
G6 SP NOT TESTED; G7 dedicated BLOCKED / NOT TESTED; stable G8 BLOCKED.
See docs/WROUGHT_IRON_CONNECTIONS.md (WROUGHT_IRON_CONNECTIONS.md within docs)
for native authority and required runtime tests.

Current validation commands/results are in TESTING.md. The original module name,
installation flag and iron sandbox identifier remain stable. The family registry
is internal asset identity; adjacency/orientation/occupancy rules are correctness
constraints, not configuration candidates. Meaningful automatic-post behavior is
controlled by per-family server booleans. Existing converted plain posts or paid
corners of any supported family prevent a second post at the same junction.
Native creation, complete-item sync and persistence paths are unchanged;
SP/dedicated save-load, join/rejoin, restart, collision and damage remain gates.
English option-name/tooltip fallback exists in all 29 language folders, preserving
every prior translation and the original construction-health option.

[VERIFIED installed asset definitions] media/newtiledefinitions.tiles.txt contains
post sprites fencing_01_13,53,69,74; no fencing_01_85 or fencing_01_93 entries.
Security/razor corner sprites84/92 are full wall corners, not standalone posts.
The native helper hashes recorded above remain unchanged.
Future authorized packages use dist/family-corner-development-current. Prior
published dist/corner-development-current dev.9 packages/provenance remain
untouched, classified historical in version-inventory.json. No artifact cleanup.
