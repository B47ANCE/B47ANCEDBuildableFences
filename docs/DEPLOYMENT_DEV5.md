# Local test deployment and manual native retest

Project Version: 1.1.0-dev.5

1.1.0-dev.5 DEPLOYED TO TEST COPY — NATIVE RETEST REQUIRED

Subsequently the user explicitly authorized an untested Workshop distribution
for dedicated testing. See WORKSHOP_DEV5_TEST_RELEASE.md. The filesystem
deployment observations below remain historical facts; they do not prove any
native result or publication outcome.

[VERIFIED filesystem] destination:
`C:\Users\willi\Zomboid\mods\B47ANCEDBuildableFences`.
Existing metadata was recorded as dev.4 before the complete managed tree was
archived outside the active mod search path. A clean tree was assembled from
production 42 source plus the isolated cohesive 42 overlay and installed.
All 97 file hashes match that composition, with no stale extra files.
The empty common directory remains for Build 42 discovery.

The old shared cursor is absent. The intended replacement is present at:
`42\media\lua\server\B47_CohesiveCursor.lua`.
Metadata is dev.5. Test-kit files and 29-language fallback translations remain.
The active cohesive Lua contains no operational topology scans, endpoint
ownership, generated-post management, neighbor rewrites or repair/removal
queues. Existing production post conversion remains unchanged.

[TESTED Windows offline] 36 tests PASS; version consistency PASS. The tests
retain every released 1.0.37 identity and verify iron menu filtering, both Q/E
directions, native entity/recipe selection, face axes, gate placement and
staged initialization. These are not native PASS results.

## Evidence

- `docs/evidence/test-deployment-dev.5.json`: destination, dev.4/dev.5 metadata,
  exact archive/log paths and 97 installed SHA-256 hashes.
- `docs/evidence/test-install-backups/1.1.0-dev.4-20261003T070602Z`: complete
  previous test copy, outside the active tree.
- `docs/evidence/pre-dev5-console-20261003T070602Z.txt`: pre-deployment log
  snapshot; historical, not dev.5 runtime evidence.
- `docs/evidence/offline-tests.txt` and `version-check.txt`: exact commands/results.
- Current native console: `C:\Users\willi\Zomboid\console.txt`.

The game process was already running during filesystem deployment. No process
was launched, killed or controlled for this deployment. The user requested no
computer use, so all native interaction remains manual. The earlier computer-use
attempt was stopped by the user before deployment; it established no dev.5
runtime result. Fully quit/restart PZ before loading a disposable test save.
Existing in-memory Lua cannot be treated as the newly deployed version.

Downloaded Workshop 1.0.37 was not modified. No Workshop staging, publication,
stable promotion, recipe edit, save edit or world-object migration occurred.

## Required results (not yet native tested)

| Gate | Result / evidence |
|---|---|
| Exact installed version/path | dev.5 at the destination above, filesystem verified |
| Exact loaded runtime version/path | UNKNOWN; restart and identify selected local mod path |
| Startup | NOT TESTED; no new dev.5 session/log |
| B47 errors/warnings | UNKNOWN for dev.5; previous shared-cursor failure is historical |
| Test kit | NOT TESTED; use SP ground context fallback or authorized MP admin slash command |
| Six-state Q/E sequence | NOT TESTED native; offline verified |
| Preview/recipe synchronization | NOT TESTED native |
| Per-state build/material consumption | NOT TESTED |
| Collision | NOT TESTED |
| Post conversion/render depth | NOT TESTED; existing state-transfer limitation retained |
| Gate interactions/audio | NOT TESTED |
| Save/reload twice | NOT TESTED |
| Dedicated two-client MP/reconnect/late join | NOT TESTED; G7 BLOCKED |
| Native regressions | UNKNOWN |
| Release | G8 BLOCKED; not release-ready or SAVE-SAFE |

## Manual retest order

1. Fully exit and restart PZ. Enable the local dev.5 copy, with only one selected
   B47 Mod ID. Load a disposable test save. Check the current console for:
   `[B47ANCEDBuildableFences] cohesive selector 1.1.0-dev.5 initialized`.
   Confirm the selected mod path is the local destination above. STOP if
   BuildingObjects requires fail, the cursor indexes nil or any B47 prototype
   initialization exception occurs; preserve the complete log.
2. If initialization passes, right-click ground and use
   `b47fencetestkit (DEV / RUNTIME TESTING ONLY)`. Where supported use
   `/b47fencetestkit`, or Lua-console fallback
   `B47FenceTestKit.request(getSpecificPlayer(0))`. Expect Hammer, Welding Mask
   and active BlowTorch in inventory, recipe-derived materials on the current
   square. The kit grants no skill or Creative Mode. Stop and capture the log
   if the kit fails.
3. Select ONE Wrought Iron Fence entry. E cycles Plain W 66, Plain N 65,
   Post-Ended W 67, Post-Ended N 64, Corner 68, Post 69, then wraps. Q reverses
   it. Compare preview, selected recipe/materials and Welding 7 each time.
   Stop if preview/recipe disagree. The trailing numbers are fencing_01 sprite
   suffixes; balance remains derived from actual entity definitions.
4. Build all states with a legitimate suitably skilled test character. Record
   before/after materials, exact sprite/identity/face, health, collision and
   sounds. Walk all sides; verify nonblocking post conversion and depth issue.
   Attempt Q/E during queued/running action: selected recipe/cost/face must
   remain frozen until completion/cancellation.
5. Gate remains separate: test W/N closed placement, open/walk/close,
   restored collision, audio and break behavior. Open sprites are not placement
   states. Save/reload twice, checking counts, state and orientation.
6. Only after SP passes, test dedicated two-client authority, construction,
   costs, post/gate agreement, reconnect, late join and server restart.
   Before stable release, separately run the untouched 1.0.37 old-save fixture
   from LEGACY_COMPATIBILITY.md. Wooden cutaway remains unresolved and unchanged.

## Exact deployment command

```powershell
& .\B47ANCEDBuildableFences\scripts\Deploy-Dev5-Test.ps1
```

This bounded script requires the old dev.4 metadata and refuses to overwrite
an existing deployment record. Do not rerun it as a generic update command.
