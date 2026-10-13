# Legacy fence compatibility audit

Project Version: 1.1.0-dev.6

CHANGED: explicit identity map, source regression checks, staged-load regression,
and isolated prototype initialization. No save writer or world migration added.
VALIDATED: [VERIFIED source] downloaded 1.0.37 identities retained. [TESTED Windows
offline] results and exact commands are in docs/evidence/offline-tests.txt.
UNTESTED: native old-save loading, restart, late chunks, listen/dedicated servers.
BLOCKED: release; unknown earlier releases; wooden cutaway root cause; native
state-preservation evidence. DEFERRED: new migration logic where exact identities
or safe replacement architecture cannot be established.

## Scope and identity map

Only the user's downloaded Workshop 1.0.37 is an established released baseline.
Its hash manifest remains unchanged. No older release artifacts or native save
fixture were supplied; compatibility with those versions is UNKNOWN. Dev.3
automatic-topology objects are experimental history, not an audited release.
The newly added iron pieces/gate have no established 1.0.37 legacy equivalents.

The central map is compatibility/LegacyFenceMap.json. Its 17 exact entity names,
every face/sprite pair, embedded CraftRecipe locations and XUI style identifiers
are enumerated in docs/evidence/legacy-identity-table.md. Each maps to itself.
Military 4, Security 3, Razor Security 3, Sloped Top wood 4 and Straight Top wood 3
remain defined. The current prototype hides internal iron menu entries, not
legacy entities or their recipes. The production wooden/security/military menu
entries remain visible until the cohesive prototype passes its gates.

Mod ID B47ANCEDBuildableFences and Workshop ID 3810187215 remain unchanged.
All legacy SpriteConfig faces, LogicClass, health/skillBaseHealth, collision
and UI definitions remain; approved construction skills/material costs and
OnCreate initialization are separate new-construction changes. Recipe knowledge
has no renamed entity definition to alias. Generated native runtime recipe
names/character knowledge require native fixture verification; the map records
embedded definitions rather than inventing runtime recipe identifiers.

There are no B47 custom tiledefinition binaries in baseline or current source.
All listed sprites are existing vanilla tiles. No numeric tile-ID remapping,
sprite overwrite, chunk rewrite or renamed alias is introduced. Numeric IDs
must still be recorded from the actual old/new runtime fixture: vanilla IDs
across game versions cannot be certified from a textual sprite-name comparison.
Damaged/broken variants are not separately declared in this released file.
Unrecognized objects and unexplained sprites are left intact. In particular,
an unlabelled IsoObject post cannot establish B47 ownership from a vanilla sprite.

## Deserialization, state and authority

[VERIFIED source] native IsoThumpable.load reads persisted north/open/locked,
health/maxHealth, sprite IDs, corner/door/pass-through/hoppable/block-all flags,
table/modData, sounds and other object state. Existing entity/sprite definitions
are retained, so this supported identity map requests no replacement at load.
It does not call OnCreate for legacy objects, rescale health, reset sounds,
change direction, alter attachments or reorder square object lists.

The compatibility strategy is deliberately a no-op: native deserialization
retains existing instances, including square/XYZ, orientation, damage, locks,
modData and attached objects. There is no client migration, custom command,
scan, migration marker, save-schema increment or new replication/persistence
path. It applies equally to subsequently loaded chunks because definitions
remain available throughout the session. Repeated loads have no new mod-side
migration effect. These are source properties, not a native save-safety PASS.
No meaningful configurable migration behavior is introduced; identity retention
is a correctness invariant, not a sandbox option.

Important boundary: the already-shipped post converter still replaces eligible
IsoThumpable posts with nonblocking IsoObject posts, removes the original first,
and does not transfer health/name/entity/modData. It is preserved under the
user's proven-post-behavior constraint; this is NOT an acceptable template for
a new migration. Custom-state preservation for unconverted legacy posts is
BLOCKED until an authorized bounded conversion redesign and native verification.
Converted posts are retained without a new compatibility scan. Do not claim
that every legacy post's custom state is preserved by the whole mod.

Stored legacy sounds/health/flags remain stored. Current OnCreate material audio
and sandbox health affect new construction only. The audit cannot promise old
objects acquire every new behavior. In-place audio/state synchronization would
need a separately verified authoritative design; no guessed update is sent.

## Collision and cutaway

[VERIFIED source] all 17 legacy faces/sprites retain their axes and properties;
W->WallW and N->WallN regression checks remain active. No replacement, wall
direction change, blocking-post regression or global sprite patch is introduced.
Physical movement, hopping, line of sight, zombie attacks, barricades/sheets
where applicable and client agreement remain native gates.

Wooden premature fade/cutaway is still unresolved in this repository. The
handoff's description of a previously solved cutaway issue is not current
runtime proof. This change neither fixes nor certifies it; compare map and
constructed objects as described in TESTING.md before implementing a patch.

## Runtime failure and source fix

[TESTED user-supplied PZ log] prototype startup FAIL at shared
B47_CohesiveCursor.lua:6: ISBuildIsoEntity is nil after failed BuildingObjects
requires. The supplied log does not print the selected mod path/version;
local deployed metadata is dev.4, not proof of the running file's exact version.
This error plausibly interrupts other mod initialization, including the test kit.

[VERIFIED native source] LuaManager.LoadDirBase adds a Lua directory to require
paths only when that phase begins, and runs vanilla files before mod files.
GameWindow loads shared/client; GameLoadingState loads server Lua for the world.
ISBuildIsoEntity and ISBuildingObject belong to that server directory. The fix
moves cursor wrappers there and defers client presentation to OnGameStart.
Installation is idempotent across repeated game-start events. A successful
installation prints the actual selector version. Native confirmation is pending.
For any later authorized deployment, remove the obsolete shared
`B47_CohesiveCursor.lua` from the managed test copy; copying the new server file
over an old installation without removing that file would preserve the crash.
The test-kit menu itself remains the ground right-click option
`b47fencetestkit (DEV / RUNTIME TESTING ONLY)` in the isolated overlay.

## Native fixture and acceptance procedure

No game/server was launched and no native save was created. On a backed-up
disposable save using untouched Workshop 1.0.37, construct every face in the
identity table, separated by four squares. Include straight/end/corner/post
runs, a perpendicular neighbor, chunk boundaries and separate remote chunks.
Record XYZ, object class/index, entity/name, sprite name/numeric ID, north,
health/maxHealth, flags, sounds, modData and applicable attachments/ownership.
Include pristine, partly damaged and damaged/broken cases where native behavior
supports them. Save, exit, and preserve an immutable copy before updating.

Load a COPY with this candidate. Compare each recorded field and object count
before interaction, after save/reload and after a second load. Check no missing,
duplicate or moved pieces; test collision/hopping/vision, wooden cutaway and
new construction independently. Converted/unconverted posts must be distinguished
and their conversion limitation recorded explicitly. Unknown variants must stay
unchanged. No admin command, manual rebuild or new-save requirement is introduced.

Repeat with listen server and dedicated server plus two clients; reconnect,
restart and visit previously unloaded chunks. Capture complete logs and exact
loaded mod path/version for each environment. Two clients must agree on object
counts, positions, orientation, state and collision. G6 native NOT TESTED,
G7 BLOCKED / NOT TESTED, G8 BLOCKED. No SAVE-SAFE or release-ready claim.

## Exact offline commands

Run from the workspace root with the bundled Python executable:

```powershell
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' B47ANCEDBuildableFences\scripts\audit_legacy.py
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s B47ANCEDBuildableFences\tests -p test_legacy_compatibility.py -v
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' B47ANCEDBuildableFences\scripts\validate.py
```

Current source and the clean local test copy are dev.5. The prior dev.4
deployment/hash record remains historical evidence. See DEPLOYMENT_DEV5.md for
the separately authorized deployment; no publication occurred. Stable target
remains 1.1.0; dev.5 is a compatible
PATCH-style fix/audit within that existing unreleased MINOR release plan.
