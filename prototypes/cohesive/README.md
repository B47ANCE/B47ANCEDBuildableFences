# Cohesive family selector overlay

Project Version: 1.1.0-dev.12

See docs/FAMILY_SELECTORS.md for the current six-family design, native authority,
recipe preservation, configuration decision and runtime gates. The overlay is
composed with production src/ as in the existing dev.6 test candidate.

All 21 fence definitions and their original costs/skills persist. One menu
entry per family cycles each real part/face; iron gate remains separate.
No shared state, recipe, collision, migration or post-conversion rewrite.

Next: native SP and dedicated two-client validation. G7 BLOCKED / NOT TESTED;
G8 BLOCKED. Historical checkpoint reports retain their original versions.

---

## Historical dev.6 notes

The following is retained for provenance, not current instructions or dev.7
validation. Current family selection and test gates are described above and
in docs/FAMILY_SELECTORS.md.

# Isolated Wrought Iron piece-selection source overlay

Historical Project Version: 1.1.0-dev.6

CORRECTED COHESIVE VARIANT PROTOTYPE IMPLEMENTED â€” RUNTIME VALIDATION REQUIRED

ONE iron fence menu entry; Q/E selects Plain W/N, Post-Ended W/N, Corner S,
Post S, each with its existing recipe. All original variants stay accessible.
No automatic neighbor selection/rewrites or generated posts. Gate is a separate
W/N entry with native open/close behavior. Other families are not generalized.

42/ overlays a PRIVATE COPY of src/B47ANCEDBuildableFences/42 for an explicitly
authorized runtime test. It is not a separate Mod ID. Keep the source copy's
common folder/metadata; replace its 29 IG_UI.json files with overlay versions.
Load ONE B47 copy and use a disposable save. A clean dev.5 local test copy is
now deployed; native retest remains manual. See ../../docs/DEPLOYMENT_DEV5.md.

Old dev.3 topology source/tests/evidence are archived under
../../docs/evidence/history/1.1.0-dev.3, outside the active mod tree. Preserve
historical experimental saves; dev.4 performs no automatic cleanup/migration.

Runtime developer kit `/b47fencetestkit` remains available via MP admin chat
or same-name SP context option. Exclude B47_FenceTestKit*.lua and
IGUI_B47_TestKit* translations from any production promotion unless requested.
See ../../docs/FENCE_TEST_KIT.md and ../../docs/COHESIVE_PROTOTYPE_REPORT.md.

Dev.5 moves cursor hooks into server Lua and defers client UI installation to
OnGameStart after a user-supplied startup failure. Native retest pending.
Local test copy now contains dev.5. Full game restart required; runtime
initialization has not yet been verified.

## Current dev.6 checkpoint

The developer test kit is removed: no kit menu, command, spawn handler or kit
translation keys ship. Earlier kit instructions describe historical dev.5.
Fence construction and the selector/gate are unchanged. G6/G7 NOT TESTED; G8 BLOCKED.

## Wrought-iron corner connections (dev.9)

New matching perpendicular wrought-iron sections can add a native junction post
included in their existing section cost. Server sandbox WroughtIronCornerPosts
defaults on; disabling affects future generation only. No existing objects are
scanned or rewritten. See WROUGHT_IRON_CONNECTIONS.md for authority, configuration,
regressions and native limitations. Future packages use the inventory-declared
dist/corner-development-current directory; old dev.8 artifacts remain historical.

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

## Expanded intact vanilla catalog (dev.12)

The current catalog adds 151 entries in 28 groups only where no vanilla recipe
supplies that art. The original six families and iron gate retain their recipes.
Vanilla gates/fences are not duplicated. New shared wooden gates serve both tall
wood styles. Decorative stair components retain their original native flags.
Four textureless fencing_01_116-119 definitions remain explicitly blocked.
See docs/VANILLA_CATALOG.md (VANILLA_CATALOG.md within docs) for scope, costs,
source fingerprints, authority and required native SP/dedicated testing.
