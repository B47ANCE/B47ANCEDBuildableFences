# Skill requirement rebalance

Project Version: 1.1.0-dev.6

The skill-only implementation described below belongs to preserved dev.2.
dev.4 retains those exact production recipe requirements and adds a separate
cohesive prototype overlay; see COHESIVE_PROTOTYPE_REPORT.md. Historical dev.2
validation records are preserved under evidence/history/1.1.0-dev.2.

Scope: construction skill requirements only. Baseline is the local dev.1
candidate, recovered earlier from downloaded Workshop 3810187215. No installed
Workshop or live mod files are edited. Mod ID B47ANCEDBuildableFences and
Workshop ID remain unchanged. The separate pasted cutaway handoff identifies
premature disappearance, but is not implemented in this skill-only pass.

## Recipes/entities changed

| Entity | Before | After |
|---|---|---|
| B47_TallWoodenFence_StraightTop | Woodwork 7 | Woodwork 4 |
| B47_TallWoodenFence_StraightTopCorner | Woodwork 7 | Woodwork 4 |
| B47_TallWoodenFence_StraightTopPost | Woodwork 7 | Woodwork 4 |
| B47_SecurityFence_PlainSection | MetalWelding 7 | MetalWelding 4 |
| B47_SecurityFence_PostEndedSection | MetalWelding 7 | MetalWelding 4 |
| B47_SecurityFence_Corner | MetalWelding 7 | MetalWelding 4 |
| B47_RazorWireSecurityFence_PlainSection | MetalWelding 7 | MetalWelding 4 |
| B47_RazorWireSecurityFence_PostEndedSection | MetalWelding 7 | MetalWelding 4 |
| B47_RazorWireSecurityFence_Corner | MetalWelding 7 | MetalWelding 4 |

Player-facing skill names are Carpentry for Woodwork and Welding for
MetalWelding. All four Sloped Top entries stay Carpentry 7. All four Military
entries stay Welding 7. All four Wrought Iron entries stay Welding 7 and are
outside the requested rebalance. No new variants or alternate recipes are added.
Future Security/Razor variants inherit the requested Welding 4 design rule
unless explicitly designed otherwise.

## Exact files changed

Gameplay definition changed:
`src/B47ANCEDBuildableFences/42/media/scripts/generated/entities/walls/entity_b47_buildable_fences.txt`.
Exactly nine SkillRequired lines changed; every other byte in that file is
preserved from dev.1. Material quantities, timed actions, XP awards, health,
skillBaseHealth, sprites, entity/XUI IDs and OnCreate hooks are unchanged.

Documentation/content updates:
README.md; src/B47ANCEDBuildableFences/42/README.txt;
docs/CONCRETE_RECIPE_AUDIT.md; docs/WORKSHOP_DESCRIPTION.md;
WORKSHOP_CHANGE_NOTE.txt; docs/ROADMAP.md; docs/ARCHITECTURE.md;
docs/VERSIONING.md; docs/TESTING.md; docs/IMPLEMENTATION_REPORT.md; this report.
These show the current tier table or record scope/testing. Current
docs/WROUGHT_IRON_SPRITE_AUDIT.md changed only its project-version header.

Version metadata/header updates: VERSION; CHANGELOG.md; version-inventory.json;
workshop-update.properties; src/B47ANCEDBuildableFences/42/mod.info;
media/lua/client/B47_NonBlockingPosts_Client.lua;
media/lua/server/B47_NonBlockingPosts_Server.lua;
media/lua/server/B47_FenceConstruction.lua (the last four under the same source
42 folder). Lua implementation bytes are unchanged apart from version headers.

Regression/tooling: tests/test_fences.py updated; scripts/rebalance_skills.py
added as a guarded one-time edit. Evidence refreshed: docs/evidence/CHANGED_FILES.md,
development-hashes.json, source-diff.txt, offline-tests.txt and version-check.txt.
New exact task diff: docs/evidence/skill-only-diff.txt. Immutable dev.1 copies,
source snapshot/hashes and original validation/report are preserved under
docs/evidence/history/1.1.0-dev.1. Old evidence keeps its original version.

## Audit, authority and configuration

[VERIFIED] All current source entity/CraftRecipe definitions were inventoried:
21 unique B47 entities in one gameplay definition file; no duplicate or
alternate target recipe retains the old threshold. Tests check every entry.
Exact task diff and source hash regression prove no unrelated runtime changes.

[VERIFIED] Skill checks continue through native shared CraftRecipe and the
existing server construction path. No new client authority, networking,
persistence or join/reconnect state is introduced. No sandbox option is added:
the user explicitly specifies fixed shared progression tiers, and this pass
changes only those requirements. Existing health sandbox behavior is unchanged.

## Validation results

[TESTED: offline Windows/Python/Lupa] 17 regression tests PASS, including three
new checks: exact nine-line change; all 21 family thresholds and unique recipe
coverage; all other runtime files unchanged except version metadata. Existing
collision-axis, post-conversion, authority, materials and localization checks
remain passing. This does not exercise native skill eligibility or game physics.

Exact validation commands from workspace root:

```powershell
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s B47ANCEDBuildableFences\tests -p test_fences.py -v
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' B47ANCEDBuildableFences\scripts\record_evidence.py
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' B47ANCEDBuildableFences\scripts\validate.py
```

The wrapper records full test/version output and invokes check_versions.py
with --root pointing to this project. Pre-edit dev.1 version audit PASS;
post-edit dev.2 version audit PASS. Stable target stays 1.1.0; no --release
check, package, staging or publication is performed.

[RUNTIME GATE] PZ SP threshold matrix: NOT TESTED. Dedicated server/two-client
threshold enforcement: NOT TESTED. Requested Carpentry 3/4/6/7 and Welding
3/4/6/7 tests for every variant are listed in TESTING.md with cheat bypass off
and materials available. No runtime result is inferred from source tests.

Skill-slice implementation complete; runtime validation required.
G6 BLOCKED / NOT TESTED, G7 BLOCKED / NOT TESTED, G8 BLOCKED. The earlier
wooden cutaway correction remains a separate unresolved task.
