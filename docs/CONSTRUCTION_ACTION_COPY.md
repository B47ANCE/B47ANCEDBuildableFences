# Construction action-copy investigation

Project Version: 1.1.0-dev.19

## Report and evidence limits

An external Workshop report forwarded on 2026-11-02 says each attempted build
adds two errors and the save is now broken. The exact game version, SP/client/
dedicated context, mod list, first exception and meaning of "broken" are UNKNOWN.
No reporter console or save was supplied. The available developer console is
dated October 24, predates the dev.18 upload, and is not this reproduction.
No save or remote server has been opened, rewritten, repaired or tested.

[VERIFIED distribution] Dev.18 was uploaded to existing item 3817174798 on
2026-11-01 after PR #8 merged at 21002592932b3700bc0fdf331fe0771d7fe896e8.
The public description and unchanged thumbnail were checked after upload.
That establishes distribution, not successful SP or dedicated acceptance.

## Confirmed source defect and falsifiable hypothesis

[VERIFIED source] Installed ISBuildingObject:tryBuild recursively copies its
placement cursor with copyTable(self) before creating ISBuildAction. The
dev.18 presentation wrapper stores B47BuildPanel on that cursor. The panel
stores the same cursor in buildEntity, making a direct table-value cycle.
The cursor also carries a tooltip UI table, needlessly adding its graph to the
action copy. Neither reference belongs to gameplay or saved world state.

Native copyTable recursively copies table values and does not memoize visited
tables. Existing read-only decompiled evidence was checked against the currently
installed LuaManager.class byte-for-byte; they match. Lua exposure is established
by the installed vanilla call, not inferred from a native method name.

[TESTED Windows offline Python/Lupa] Running the installed vanilla tryBuild
function with opaque engine-object fakes and a bounded recursive-copy model
rejects the cycle for all 47 panel recipes before the fix. It passes after it.
The bounded detector reports the cycle rather than deliberately overflowing the
host stack. This is not execution of PZ's native copyTable or an observed native
StackOverflowError. It does not reproduce the reporter's exact two errors.

[INFERRED] This defect plausibly explains failed construction through the
construction window. The defect existed before dev.18's visibility change;
it was omitted by the old cursor-selection-only mocks. The supplied report does
not establish that this is its only cause or that any saved data is corrupt.
A reporter stack showing copyTable/tryBuild would corroborate the hypothesis;
a different primary stack requires further investigation.

## Fix and invariants

Client-local weak-key maps now hold panel and tooltip associations by cursor.
No UI table is attached to the copied cursor. Deactivation removes its tooltip
once and clears both associations; the native panel wrapper reattaches when
reusing a cursor. The primitive chosen-face value is still copied by vanilla.
No generic copyTable override, custom action or broad error suppression ships.

Every recipe, part cost, requirement, timed action, saved entity identity and
server construction callback is preserved. Native BuildLogic remains the shared
action authority and the existing in-progress selection freeze stays intact.
No new network messages, client inventory/world writes, save scan or migration.
These UI lifetime references are implementation structure, not configurable
gameplay; no new sandbox setting is justified. Existing server settings remain.

Six regression methods cover all 47 recipes at build start, rendered panel and
context cursors, unrelated native cursors, the copied recipe/face and shared
native logic, frozen active selection, and repeated deactivate/reuse cleanup.
The test fixture now mirrors vanilla's persistent panel cursor flags. It treats
engine-object fakes as opaque, matching native userdata rather than reporting
cycles introduced solely by fake recipe/info links.

## Installed evidence

Steam build 25485521; full game version UNKNOWN. Reviewed 2026-11-02.
Portable paths and SHA-256 fingerprints:

| Evidence | SHA-256 |
|---|---|
| media/lua/server/BuildingObjects/ISBuildingObject.lua (tryBuild, lines 176-209) | 0055ef5e0054a7b7b4faa5cdfea4eca8fa0920691e62c4456fbe6dd119d3f152 |
| media/lua/server/BuildingObjects/ISBuildIsoEntity.lua (cursor construction) | 6f485b0a90b9b8583fc8112aeddcb3f50a50bf7d1c0c6bc369138ee781deda38 |
| media/lua/client/Entity/ISUI/BuildRecipe/ISBuildPanel.lua (lines 310-343) | 2b4bb8908dbf0158f68bc0a9c05b6d338fc1695d6fc9897b78e22010c342e05d |
| zombie/Lua/LuaManager.class inside projectzomboid.jar (copyTable implementation) | dcaad0082ca27a15550c7d0a6e14b3aeb71f634a14f32123dec620df180c646d |

Only vanilla implementation was inspected for this fix. No third-party mod
implementation or private diagnostics are copied into the repository.

## Runtime gate and next reproduction

[RUNTIME GATE] On a disposable test world or backed-up copy, open construction,
preview and build a fence, change its selected part, complete/cancel and build
again. Repeat from the context menu and with a vanilla recipe. Confirm materials
are charged exactly once and an active build cannot change recipes. Save, quit
and reload. Dedicated testing additionally needs two-client synchronization,
join/rejoin and server restart. Preserve the first complete exception and its
preceding messages if any step fails. Do not use the original reported save for
experiments or claim that disabling/removing the mod repairs it.

G6 SP NOT TESTED. G7 dedicated BLOCKED / NOT TESTED. Stable G8 BLOCKED.
This source iteration does not package, deploy, publish or restart Steam.
