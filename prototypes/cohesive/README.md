# Isolated Wrought Iron piece-selection source overlay

Project Version: 1.1.0-dev.6

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
