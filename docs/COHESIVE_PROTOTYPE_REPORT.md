# Corrected Wrought Iron variant-selection prototype

Project Version: 1.1.0-dev.6

CORRECTED COHESIVE VARIANT PROTOTYPE IMPLEMENTED â€” RUNTIME VALIDATION REQUIRED

Only Wrought Iron is consolidated. Other families retain their current menus
until this prototype passes native/dedicated tests. Public source recipes and
gameplay remain dev.2; current version headers advance. Mod ID, Workshop ID,
21 definitions/assets, collision fixes and post conversion are preserved.
No launch, deployment, package or publication occurred.

## Rejected work preserved

Before replacement, all active dev.3 overlay files, tests, reports, metadata
and proof records were archived to docs/evidence/history/1.1.0-dev.3.
The complete old overlay is automatic-topology-overlay/42 there. Its tests
retain original dev.3 evidence, not current validation. Archive is outside the
active mod tree. Model, cursor, presentation and authority files were replaced;
no old topology is loaded. Native gate/test-kit research and source are reused.

Removed from active behavior: endpoint ownership, generated posts, neighbor
scans, sprite rewrites, marker schema, repair/removal queues and post cleanup.
No existing built object is migrated or mutated by the new selector. Disposable
test saves are still appropriate; old dev.3 generated posts are historical test
objects, not silently deleted or converted by dev.4.

## Exact selection and recipe sequence

E advances through this loop; Q traverses it backward:

| State | Existing entity | Face/sprite | Own recipe inputs | Welding | Base health / skillBaseHealth | Time / XP |
|---|---|---|---|---:|---|---|
| 1 | B47_WroughtIronFence_PlainSection | W / fencing_01_66 | Torch5 uses, Pipes5, Scrap2, Rods5 uses | 7 | 2500 /250 | 200 /70 |
| 2 | Same Plain entity | N / fencing_01_65 | Same Plain recipe | 7 | 2500 /250 | 200 /70 |
| 3 | B47_WroughtIronFence_PostEndedSection | W / fencing_01_67 | Torch5 uses, Pipes5, Scrap2, Rods5 uses | 7 | 2500 /250 | 200 /70 |
| 4 | Same Post-Ended entity | N / fencing_01_64 | Same Post-Ended recipe | 7 | 2500 /250 | 200 /70 |
| 5 | B47_WroughtIronFence_Corner | S / fencing_01_68 | Torch7 uses, Pipes7, Scrap3, Rods7 uses | 7 | 2500 /250 | 250 /70 |
| 6 | B47_WroughtIronFence_Post | S / fencing_01_69 | Torch2 uses, Pipe1, Scrap1, Rods2 uses | 7 | 1250 /125 | 100 /20 |

These are documentation values read from existing entities, not a second
balance table. Native skill bonuses/server health option still apply. Corner S
is the existing entity's single face for its actual WallNW asset; it is not an
invented cardinal collision direction. Post S is its preserved post asset.
No unsupported E/S straight face or extra corner orientation is invented.

Gate remains a separate entry: W fixture20 and N21 closed placement faces;
Q/E switches them. OPEN22/23 are never placement selection states. Native
interaction controls open/close after construction. Its original prototype
recipe/assets and gate-only sound/health initialization remain unchanged.

## Exact active implementation

All files below live in prototypes/cohesive/42, not public src/:

- shared B47_CohesiveModel.lua: existing iron entity IDs and enumeration of
  real ObjectInfo faces/recipes. No gameplay costs, health or skill table.
- server B47_CohesiveCursor.lua: scoped native cursor wrappers; actual selected
  face supplies sprite/north. Q/E/controller/native rotate dispatch selects
  states, held mouse cannot override choice. Placement checks selected native
  recipe availability without bypassing native server recipe validation.
- client B47_CohesivePresentation.lua: filter three iron submenu entries from
  context menu and Build window; recreate native cursor when entity changes,
  or pin chosen face. Build window logic.setRecipe updates native requirement
  widgets. A live placement tooltip always reads the selected recipe, including
  skill, input quantities, tool-keep flags, piece and face.
- server B47_CohesiveAuthority.lua: gate initialization ONLY. It does not wrap
  B47Fence.OnCreate or mutate neighbors. Fence variants use existing callback.
- existing gate entity/style and three developer test-kit files are retained.
- all 29 overlay translations include selected-piece/control/recipe labels.

Support changes: variant_checkpoint.py archival/version transition,
record_cohesive_evidence.py translations/hashes/inventory, new
tests/test_variant_selection.py (old topology test archived), corrected Badlands
audit and current docs/changelog/evidence. Production entity file is unchanged.
Current offline results are in evidence/offline-tests.txt. Dev.4 user-supplied
startup trace FAILED during shared cursor loading; dev.5 moves that cursor
to server Lua and defers client presentation to OnGameStart. Native retest
is pending. Historical dev.4/deployment proofs remain unchanged.

The context family entry remains selectable even without Plain materials, so
the player can cycle to cheaper Post. Each resulting placement still checks
its own recipe. Native Build window refresh retains recipe-to-entity lookup
for hidden internal definitions and only filters the visible list. Switching
recipes updates native widget events; the extra placement tooltip supplies
the current costs even from the context path.

## Preview, action ownership and multiplayer

State selects actual ObjectInfo/CraftRecipe plus existing native nSprite. The
native render/cacheSprites renders that selected entity's face directly; there
is no inferred topology sprite or generated-post ghost. getSprite returns the
same face tile for native action intent. Selected face is pinned so native
held-mouse/auto-rotation fallback cannot choose another face behind the UI.

Native ISBuildingObject.tryBuild copies cursor fields but shares BuildLogic;
therefore Q/E/controller cycling is frozen while that logic has a queued or
in-progress craft action. Completion/cancel re-enables cycling. This protects
the action's recipe as well as the native copied entity/face. No parallel
client-defined recipe/material protocol is introduced.

createBuildAction transmits selected entity/native face. Server reconstructs
the native entity cursor, validates placement/current recipe, consumes its
actual materials and creates original entity components. Native OnCreate
initializes material audio and server health scaling; native complete-object
transmission/save/load owns the result. Clients never calculate permanent
variants. Gate object retains native door state/synchronization. Posts still
take the exact preserved client/server nonblocking conversion path.

Configuration assessment: sequence/order and key adapter are UI correctness,
not gameplay balance alternatives. No new sandbox setting or mutable recipe
table. Existing server health sandbox and native construction bonus remain.

## Source evidence and validation

[VERIFIED, source] original iron W/N art matches WallWTrans/WallNTrans;
corner68 is original WallNW; post69 is original standalone art. Original
21 entity costs/skills/times/XP/health/hooks stay unchanged. Badlands Privacy
uses one native entity with W/N faces and one fixed recipe; it does NOT prove
switching distinct piece recipes. B47 extends native face selection to actual
entity selection without copying reference code/art. Exact path is in
BADLANDS_FENCE_REFERENCE_AUDIT.md.

[TESTED, Windows offline Python/Lupa] Corrected tests execute forward/reverse
six-state reachability, entity/recipe/time/declared-health agreement, live
cost/skill tooltip, Build window recipe selection, action freeze, native ghost
face pin, unavailable selected-recipe rejection, one menu entry, closed-only
gate cycle, all reachable straight-axis metadata, 29-language coverage and
absence of topology writes/events in active files. Existing production and
test-kit suites rerun. Offline mocks do not execute native consumption/network.

Exact current commands/output: evidence/offline-tests.txt and version-check.txt;
active overlay hashes: cohesive-hashes.json. Focused command:

```powershell
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s B47ANCEDBuildableFences\tests -p test_variant_selection.py -v
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' B47ANCEDBuildableFences\scripts\validate.py
```

[RUNTIME GATE] G6 native NOT TESTED; G7 dedicated BLOCKED / NOT TESTED; G8
BLOCKED. Actual per-state material consumption, collision, dynamic health,
heard sound, post conversion, save/reload and second-client equality NOT TESTED.
Native UI signals/filter refresh and queued-action freeze also need runtime
checks. Wooden premature cutaway remains separate and unfixed. No release or
generalization readiness claim.

## Required runtime matrix

1. Select ONE Wrought Iron Fence entry in context menu and Build window.
2. E through all six states; Q backward. Compare exact entity name/face,
   preview, costs and Welding7 against the table. Enter with insufficient Plain
   materials and cycle to cheaper Post; availability must follow selected cost.
3. Build EVERY state without Creative Mode. Confirm exact consumed uses/items,
   final sprite, axis/corner collision, health/skill bonus and material sounds.
   Post must become nonblocking through unchanged conversion.
4. Change selection beside existing fences: no neighbor sprite/object changes,
   no generated posts or repaired topology. Q/E during queued/running action
   must not change the recipe charged for that action.
5. Repeat gate W/N preview/build/open/close; opening state is native interaction.
6. Save/reload all pieces/gate; dedicated server, second client, late join and
   reconnect. All clients must receive same entity/face and post conversion.
7. Generalize Tall Wooden7 pieces, Military4, Security3 and Razor3 only AFTER
   this iron matrix and dedicated G7 pass. Current other-family menus stay intact.

## Current dev.6 checkpoint

The developer test kit is removed: no kit menu, command, spawn handler or kit
translation keys ship. Earlier kit instructions describe historical dev.5.
Fence construction and the selector/gate are unchanged. G6/G7 NOT TESTED; G8 BLOCKED.
