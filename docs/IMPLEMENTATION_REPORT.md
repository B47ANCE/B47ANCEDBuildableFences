# Implementation report

Project Version: 1.1.0-dev.6

Current dev.4 replaces the isolated Wrought Iron topology overlay with the
player-selected piece/recipe overlay documented
in COHESIVE_PROTOTYPE_REPORT.md and corrects the Privacy Fence reference audit.
The production expansion/skill implementation described below is unchanged.
Current offline verification includes corrected variant and isolated runtime-kit tests;
native SP/save/MP remains untested. See FENCE_TEST_KIT.md for command details.

Date: 2026-10-02. Baseline: downloaded Workshop 3810187215, mod.info 1.0.37.
Source recovery and bounded development only. Installed Workshop copy untouched.
Stable target is 1.1.0; no downgrade or released-version relabeling.

Current checkpoint also includes the nine-entry skill-only rebalance documented
in SKILL_REBALANCE_REPORT.md. Straight Top requires Carpentry 4; Sloped Top
Carpentry 7; Security/Razor Welding 4; Military Welding 7; Wrought Iron Welding 7
unchanged. The prior dev.1 report/results are archived with their actual version.

## Delivered changes

- Four wrought-iron pieces bring the source collection from 17 to 21. Verified
  vanilla W/N plain=66/65, post-ended=67/64, corner=68, post=69. Four menu icons
  come from those vanilla sprites; no Badlands art or definitions are copied.
- Six Security/Razor recipes replace two/three Scrap Metal with one/two mixed
  Concrete Uses. Skill, pipes, torch/rod uses and Razor wire remain as requested.
  Actual B42.21 mixed items are BucketConcreteFull/BucketCarvedConcreteFull;
  Base.Concrete is not defined. See CONCRETE_RECIPE_AUDIT.md for the full table.
- The server-side native OnCreate callback initializes per-object material
  thump fallback and break behavior before normal transmission. No global
  sprite flags or sound registry changes. Existing saved objects are not
  rewritten. Audio correctness remains untested in PZ.
- One server sandbox integer controls new section/corner health, 10â€“500%,
  default 100. Invalid input restores 100; converted posts are excluded.
- All 21 menu names and sandbox name/tooltip have complete English fallback
  values in all 29 vanilla language folders. Existing vanilla tooltips are reused.
- Both post allowlists gain the iron name and sprite. The entire existing
  client/server replacement sequence and request-validation logic are unchanged.
- Canonical version inventory, current headers/docs/Workshop metadata and
  changelog synchronized. Workshop ID remains 3810187215; Mod ID unchanged.

## Exact files

Modified relative to recovered B47 baseline:

1. src/B47ANCEDBuildableFences/42/mod.info
2. src/B47ANCEDBuildableFences/42/README.txt
3. src/B47ANCEDBuildableFences/42/media/scripts/generated/entities/walls/entity_b47_buildable_fences.txt
4. src/B47ANCEDBuildableFences/42/media/scripts/entities/walls/entity_b47_buildable_fences_xuiSkin.txt
5. src/B47ANCEDBuildableFences/42/media/lua/client/B47_NonBlockingPosts_Client.lua
6. src/B47ANCEDBuildableFences/42/media/lua/server/B47_NonBlockingPosts_Server.lua

Added runtime files: media/lua/server/B47_FenceConstruction.lua,
media/sandbox-options.txt, four media/textures/Build_WroughtIronFence_*.png and
58 translation JSON files (IG_UI.json and Sandbox.json in each of the 29 folders).
The exact expanded filename list is evidence/CHANGED_FILES.md; the complete
scoped text diff is evidence/source-diff.txt. No unrelated project/runtime files
are edited. Baseline poster/17 icons remain unchanged.

Project support added: VERSION, version-inventory.json, README.md, CHANGELOG.md,
WORKSHOP_CHANGE_NOTE.txt, workshop-update.properties; docs/ARCHITECTURE.md,
ROADMAP.md, TESTING.md, VERSION_POLICY.md, VERSIONING.md, WORKSHOP_DESCRIPTION.md,
this report, BADLANDS_FENCE_REFERENCE_AUDIT.md, MATERIAL_BEHAVIOR_AUDIT.md,
WROUGHT_IRON_SPRITE_AUDIT.md and CONCRETE_RECIPE_AUDIT.md; scripts/check_versions.py
(framework tool), audit_tiles.py, inspect_wrought_sprites.py,
prepare_development.py, record_evidence.py, validate.py; tests/test_fences.py; optional
research/compare_cutaway.lua. Evidence includes baseline/source/reference hash
records, six extracted iron images plus contact sheet, offline validation logs
and independently decompiled vanilla classes. Research files are not mod source
and must never be shipped. No third-party source is stored in the mod.

## Cutaway and cohesive architecture

BADLANDS_FENCE_REFERENCE_AUDIT.md supplies the requested A/B/C/D architectural
comparison and identifies Privacy Gate as Badlands' wooden KNX_GatePrivacy.
Its source shows native closed/open faces, not general automatic neighbor
selection. Automatic connections, corner insertion and a gate feature are
not added to B47 in this slice.

[UNKNOWN] A construction-specific wooden cutaway root cause was not established.
The same vanilla wall sprites drive native rendering, and changing an object's
type would mutate its shared sprite type. No collision-compromising type
replacement, axis reversal, global flags or alpha workaround is applied.
**Wooden cutaway correction is not implemented.** A read-only diagnostic and
paired runtime comparison are provided in TESTING.md to establish a safe fix.
This blocker prevents claiming the full requested implementation complete.

## Validation and authority

[TESTED: offline Windows/Python/Lupa] 17 regression tests PASS. They verify all
21 entities and style/icon/localization coverage; existing 17 entity blocks
unchanged except sound/config callback, six intended input replacements and
the nine approved skill thresholds;
metadata-correct wall axes; exact post implementation preservation; executed
authority-side callback material/default/config validation; client mutation
rejection; executed server replacement/rejection/duplicate handling; MP detector
intent with no local mutation; concrete use syntax; Lua syntax/brace structure;
and unchanged installed baseline hashes. New tests compare all source files
against dev.1 and prove only nine entity lines changed, with no duplicate/alternate
recipes or unrelated runtime edits. Exact commands are in TESTING.md.

[VERIFIED] W/N source mappings and baseline post sequences are preserved.
[RUNTIME GATE] Actual player collision is NOT TESTED for this candidate.
Corners, connected runs, nonblocking persistence, audio and concrete use cannot
be marked PASS by these tests. Native script engine loading is also untested.

[VERIFIED] Native construction remains authoritative; the callback runs only
on authority and lets native replication send one complete object. No added
client gameplay state or networking. Post conversion retains source-validated
baseline trust boundaries. Dedicated behavior, late join, reconnect and restart
remain [RUNTIME GATE]. See ARCHITECTURE.md for preserved baseline limitations
and sandbox/save behavior.

[TESTED: offline] Baseline version checker passed before implementation and
the final declared-current inventory passes after edits. --release is NOT RUN:
there is no current artifact and G8 is blocked. Complete current mirror inventory
is version-inventory.json. Historical baseline claims/versions are retained;
version synchronization does not refresh their runtime validity.

## Remaining known issues and verdict

- Accepted baseline same-tile standalone-post depth ordering remains.
- Wooden native-equivalent cutaway is unresolved; G3 is partial/blocked.
- Exact loaded tile sounds and weapon-impact material selection need runtime
  evidence; the native 42.21 melee switch has gaps documented in the sound audit.
- Existing saved object sound fields are not migrated by the construction hook.
- Baseline post request-cache/retry and conversion state-transfer limitations
  are preserved, not newly certified.
- No client or dedicated runtime test, second-client proof, reconnect/restart
  proof or current candidate log audit has been performed.
- Engine optional animation-directory scan spam is intentionally not patched.
  BrokenFences registration warnings remain separate from per-object audio.

Verdict: **SAFE EXPANSION IMPLEMENTED â€” WOODEN CUTAWAY BLOCKED;
RUNTIME VALIDATION REQUIRED.** G6 BLOCKED / NOT TESTED,
G7 BLOCKED / NOT TESTED, G8 BLOCKED. No release-ready or full completion claim.
No game/server launch, live deployment, staging, ZIP or publication.

Current follow-up: see LEGACY_COMPATIBILITY.md for exact identity retention,
startup failure/source fix, post-state limitation and remaining native gates.
