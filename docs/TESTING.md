# Current validation

Project Version: 1.1.0-dev.13


## dev.13 rename validation

[TESTED Windows offline Python/Lupa, 2026-10-15] Metadata-only PATCH iteration:
59 available regressions PASS; five missing original-baseline checks BLOCKED.
`python scripts/test_current.py --available`,
`python scripts/generate_expanded_catalog.py`,
`python scripts/check_versions.py --root .` and
`python scripts/prepare_workshop.py` (read-only preflight) all PASS.
Native SP/dedicated evidence remains absent.
The dev.12 record below is historical at its tested version. G6 NOT TESTED;
G7 dedicated BLOCKED / NOT TESTED; stable G8 BLOCKED. No packaging or upload.


## dev.12 current validation

[TESTED Windows offline Python/Lupa, 2026-10-15] 59 available tests PASS,
including ten catalog regressions over all 151 new entries. Five missing
original-installed-baseline methods remain explicitly BLOCKED, not PASS.
Coverage: no vanilla recipe duplicates; complete bounded asset disposition;
real item IDs and paid inputs; generated entity/skin/Lua/29-language parity;
family cycling both directions; recipe/action freeze and affordability;
closed/open and native double-gate layout; exact server name/sprite/orientation
validation, client/malformed-object rejection, health bounds/defaults and
unchanged original recipe/callback fingerprints. Offline mocks are not PZ.

Exact commands from repository root (local Python/Lupa):
```
python -m unittest discover -s tests -p test_expanded_catalog.py -v
python scripts/test_current.py --available
python scripts/generate_expanded_catalog.py
python scripts/check_versions.py --root .
python scripts/prepare_workshop.py
```
All PASS. Read-only preparation checks 100 runtime files, no shipped tests,
diagnostics or custom Java/JAR; case/require and source composition checks PASS.
Version check defers absent new packages. No package, deploy, game/server launch
or Workshop upload. G6 SP NOT TESTED; G7 dedicated BLOCKED / NOT TESTED;
stable-release G8 BLOCKED. Native matrix: VANILLA_CATALOG.md.

## Historical validation from earlier iterations

The observations below retain their original scope and are not dev.12 proof.

[TESTED Windows offline Python/Lupa, 2026-10-14] 49 available tests PASS.
Five original-installed-baseline methods are explicitly BLOCKED because the
old Workshop 3810187215 download is absent. They are not silently marked PASS.
The full suite is not claimed to pass. Fresh-clone users need Python with Lupa;
local .test-dependencies is ignored and is not a runtime mod dependency.

Commands from repository root:
```powershell
$env:PYTHONPATH=(Resolve-Path .test-dependencies).Path
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -m unittest discover -s tests -p test_family_selectors.py -v
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' scripts/test_current.py --available
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' scripts/check_versions.py --root .
```

Seven new tests execute Lua with source-derived recipes: six menu roots plus gate,
all real parts/faces in both directions, per-part cost/skill/time/health, live
Build-window selection, action freeze, selected-part rejection, controllers,
missing-info handling, affordable-secondary context-menu access and fallback translation keys. Existing authority,
concrete semantics, axes, legacy boot and kit-removal tests remain active.
Mocks do not execute engine physics, native UI rendering or network actions.

Native APIs/hashes, authority, configuration assessment and required runtime
matrix are in FAMILY_SELECTORS.md. G6 SP NOT TESTED; G7 dedicated MP BLOCKED /
NOT TESTED; G8 BLOCKED. No build/package, deployment, publication or native
launch was performed. Release artifact/version validation is deferred until
an explicitly authorized package is built after required gates; existing
published dev.6 files remain historical, untouched and not current proof.

---

## Historical dev.6 notes

The following is retained for provenance, not current instructions or dev.7
validation. Current family selection and test gates are described above and
in docs/FAMILY_SELECTORS.md.

# Testing and operator handoff

Historical Project Version: 1.1.0-dev.6

Date: 2026-10-02. Environment: Windows offline Python/Lupa, installed vanilla
42.21 source/bytecode. No Project Zomboid or server launched by this task.

dev.4 tests the corrected variant-selection overlay with executed Lua fake-world
tests. See COHESIVE_PROTOTYPE_REPORT.md for its required native A/B matrix.
G6 native SP NOT TESTED, G7 dedicated BLOCKED / NOT TESTED, G8 BLOCKED.

## Offline commands

From `C:/Users/willi/Desktop/Repositories/Project Zomboid`, use:

```powershell
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s B47ANCEDBuildableFences\tests -v
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' B47ANCEDBuildableFences\scripts\check_versions.py --root B47ANCEDBuildableFences
```

Final recorded run uses the same commands through the offline wrapper:

```powershell
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' B47ANCEDBuildableFences\scripts\validate.py
```

It preserves commands, exit codes and full outputs in evidence/offline-tests.txt
and evidence/version-check.txt. It never runs game/server or produces a package.

Audit reproduction (read-only to installed game):

```powershell
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' B47ANCEDBuildableFences\scripts\audit_tiles.py
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' B47ANCEDBuildableFences\scripts\inspect_wrought_sprites.py
```

Version checker also ran successfully on recovered baseline 1.0.37 before
runtime edits. No --release check can PASS until authorized current artifacts
exist after runtime gates. prepare_development.py is the guarded one-time
recovery transformation, not a build/deployment command; do not rerun implementation
over edited source. Source-contract tests compare current installed baseline
against its recorded hashes first so a Workshop update cannot silently become
the regression baseline. Lua tests execute in Lupa against engine mocks; no
native script parser, actual physics, persistence or sound emitter is exercised.

## Gates

| Gate | State | Evidence / reason |
|---|---|---|
| G0 requirements | PASS | Three user handoffs, IDs/invariants retained, sandbox/authority assessed |
| G1 reconnaissance | PASS with explicit unknowns | Source/bytecode/sprite audits; cutaway cause and loaded sound state unknown |
| G2 design | PASS for bounded slice | Native construction, same post sequence, no connection rewrite |
| G3 implementation | PARTIAL / BLOCKED | Safe expansion implemented; wooden cutaway correction lacks proven cause |
| G4 static | PASS offline | Inventory, brace/source contracts, axes/properties and localization |
| G5 offline | PASS offline | Executed regression suite; final results in IMPLEMENTATION_REPORT.md |
| G6 actual PZ SP | BLOCKED / NOT TESTED | Operator runtime evidence required |
| G7 dedicated MP | BLOCKED / NOT TESTED | Two clients, late join/reconnect and restart required |
| G8 release | BLOCKED | G3/G6/G7 outstanding; no package or --release proof |

## Runtime setup and evidence

### Skill rebalance threshold matrix â€” NOT TESTED in PZ

Turn build cheat/debug bypass off and supply all unchanged materials/tools so
skill is the only failed prerequisite. Test every listed variant, including
corners/posts, in SP and on a dedicated server. Native internal skill names
are Woodwork (Carpentry) and MetalWelding (Welding).

| Skill level | Expected behavior |
|---|---|
| Carpentry 3 | Cannot build any Straight Top piece |
| Carpentry 4 | Can build all three Straight Top pieces; cannot build any Sloped Top piece |
| Carpentry 6 | Still cannot build any Sloped Top piece |
| Carpentry 7 | Can build all four Sloped Top pieces |
| Welding 3 | Cannot build any Security/Razor piece |
| Welding 4 | Can build all six Security/Razor pieces; cannot build any Military piece |
| Welding 6 | Still cannot build any Military piece |
| Welding 7 | Can build all four Military pieces |

Wrought Iron remains Welding 7 and is not rebalanced. Record both menu
eligibility and accepted/rejected construction, including server enforcement,
for each variant. Skill-slice G3 is complete; G6 and G7 remain BLOCKED / NOT
TESTED. The separate wooden cutaway bug is reported premature disappearance;
this skill-only pass does not implement or validate its pending correction.

Human operator must explicitly authorize any test deployment or launch. Use an
isolated save and exactly this candidate revision; record candidate hashes,
client/server build, mods enabled and sandbox values. Do not overwrite a live
save or installed Workshop baseline. No test deployment is performed by this
task. Test vanilla-only and candidate-only where practical to separate other
mods' sprite/property interference.

For all 21 menu entries, record construction, sprite and orientation. For each
straight variant, test W and N independently: physical edge blocks movement,
perpendicular/adjacent unrelated paths remain clear, no visible-axis mismatch.
Test every corner for collision, construction and phantom neighboring edges.
For all four standalone posts, confirm conversion, remaining tile traversal,
visible sprite, save/reload and no duplicate/disappearing object. Accepted
same-tile player/post depth ordering is not a collision failure.

Compare tall wooden sloped/straight-top sections, corners/posts and connected
runs against the same vanilla map sprites. Record player north/south/east/west
and same tile where relevant, renderer configuration and screenshots/video.
Use the optional read-only `research/compare_cutaway.lua` console diagnostic
on both objects to record actual loaded flags, class, north/block-all and sound
state. Do not alter sprite flags to manufacture a visual match. A safe targeted
cutaway patch requires evidence from this paired comparison first.

For each Security/Razor plain, post-ended and corner recipe: exactly enough
concrete; insufficient uses; partially used bucket; two partially used buckets;
metal and carved containers; final-use depletion returning the correct empty
container; exactly enough/partial torch; rods/pipes; Razor wire; zero Scrap
Metal; cancellation. Record before/after concrete/torch uses on authority and
both clients. Straight/end consume one concrete use, corner two. Full bucket
must not vanish after a single-use construction.

For wood, iron, military, Security and Razor: zombie thump, weapon impact,
repeated damage and destruction, compared to equivalent vanilla objects.
Record client A/B audio and verify no inappropriate door-like metal thump.
The per-object fallback is not proof of loaded vanilla sound patch correctness
or melee-hit surface correctness. Converted posts are nonthumpable and should
not be made blocking to run an inapplicable attack test.

Dedicated server + A constructs every modified piece; B observes and tests
collision independently. Test late join, reconnect of both clients, restart
server, persistence and duplicate conversion. Test ConstructionHealthPercent
at default 100 and bounds 10/500: new sections/corners change health; existing
pieces and converted posts stay unchanged; clients obey server setting.

Audit both client console.txt and dedicated console for B47, B47ANCED,
B47ANCEDBuildableFences, ERROR, Exception, Tried to call nil, stack traceback,
IsoThumpable, IsoObject, OnClientCommand and OnServerCommand. Distinguish known
optional AnimSets/actiongroups engine scan messages and global BrokenFences
registration from candidate regressions. Preserve complete logs and record
reproduction with/without other mods. No audio/runtime gate may PASS from
script compilation, SP alone or a mocked engine.

## Legacy and initialization gate

See LEGACY_COMPATIBILITY.md for the exact 17-entity identity map and full
old-save fixture procedure. The supplied dev.4-like prototype startup log
FAILS at shared cursor initialization. Dev.5 source fixes phase ordering;
native retest, old-save SP/listen/dedicated/restart/late-chunk validation are
NOT TESTED. Existing post-conversion custom-state limitations block blanket
state-preservation claims. Current offline counts are in evidence/offline-tests.txt.

## Current dev.6 checkpoint

The developer test kit is removed: no kit menu, command, spawn handler or kit
translation keys ship. Earlier kit instructions describe historical dev.5.
Fence construction and the selector/gate are unchanged. G6/G7 NOT TESTED; G8 BLOCKED.

## Current dev.8 cleanup verification

The offline suite is retained. Tooltip assertions now inspect the rendered
placement tooltip rather than a test-only exported function. Workshop preparation
checks source composition, absence of runtime diagnostics/test hooks, case
collisions and custom require casing, unexpected overrides, ZIP membership,
path traversal, CRC and source/stage/archive parity. No historical test result
is relabelled as dev.8 evidence. See WORKSHOP_PREPARATION.md for this iteration.

## Current corner-connection coverage

Seven new tests execute vanilla corner helpers plus the server-only wrought-iron
wrapper. See WROUGHT_IRON_CONNECTIONS.md for exact commands, authority/config
contract, known native limitations and required SP/dedicated matrix. 44 runnable
tests PASS; five missing-original-baseline gates remain BLOCKED.

## dev.10 validation

[TESTED Windows offline Python/Lupa, 2026-10-14] 49 available tests PASS,
including 12 connection tests (five added for family expansion).
Five original-installed-baseline comparisons remain BLOCKED; no runtime proof.
Exact commands from repository root (Python/Lupa available):
```
python -m unittest discover -s tests -p test_wrought_iron_connections.py -v
python scripts/test_current.py --available
python scripts/check_versions.py --root .
python scripts/prepare_workshop.py
```
All PASS; prepare_workshop is a read-only preflight reporting 95 runtime files,
no shipped tests/diagnostics/Java/JAR. New package absent/deferred. No package,
deploy, game/server launch or Workshop upload for this iteration.
