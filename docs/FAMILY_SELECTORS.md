# Fence family selectors

Project Version: 1.1.0-dev.7

Compatible MINOR-scope expansion within the current 1.1.0 prerelease series.
The composed development candidate has six fence entries: straight-top wood,
sloped-top wood, military, security, razor-wire security and wrought iron.
The wrought-iron gate stays separate. Every existing part/entity/recipe remains
registered. Q/E, the native rotate binding, or controller bumpers cycle actual
parts and their real available faces. No invented orientations or automatic
connection/post generation are added.

Implementation lives in prototypes/cohesive/42, composed with authoritative
src/B47ANCEDBuildableFences/42, as in dev.6. Source layout is unchanged.
The family map contains only existing identifiers, never copied cost/skill data.
The selected ObjectInfo supplies its CraftRecipe, health, time, tool choices and
face. Context and Build-window lists hide secondary parts, but native entity
lookup retains them. When vanilla returns only an affordable secondary part, it is represented by its
family root. The family entry stays accessible for selecting that cheaper part.
The native requirement widgets and placement tooltip follow the selected recipe.

[VERIFIED source] Installed vanilla ISBuildPanel.lua createBuildIsoEntity reads
getSelectedBuildObject/getRecipe, creates the matching native cursor, equips
recipe tools and evaluates canPerformCurrentRecipe. ISBuildAction.lua start
uses createBuildAction; perform returns on clients. ISBuildIsoEntity.lua create
uses the native construction/consumption path. No custom network messages,
client inventory mutations or shared gameplay state were added. Construction
callbacks, post conversion and recipes remain unchanged apart from version text.
Exact local evidence files and hashes are recorded below during validation.

Persistence and reconnect: selection is transient cursor/UI state, not world or
save data. Existing built objects and IDs are retained. Vanilla remains owner of
constructed objects and synchronization. [RUNTIME GATE] Dedicated two-client
construction, inventory rejection, reconnect/late join and restart remain untested.

Configuration assessment: family membership and real face enumeration are UI
structure, not gameplay tuning; no new sandbox setting is justified. Existing
server ConstructionHealthPercent continues unchanged. Existing recipes own
skills/materials. No duplication or migration protocol is introduced.

Localization: 29 existing language folders retain reviewed text and English
fallback for added part labels/controls. Tests assert actual key coverage, not
folder count alone. No custom Java/JAR dependency or engine changes are added.

Required native checks: both right-click and Build window show six family roots
plus gate; each part preview, materials, concrete uses, skill and tools match;
Q/E/custom rotate/controller controls work; unaffordable parts reject builds;
construction/cancellation cannot change an active recipe; existing saves/load,
post collision, gate, two clients, reconnect/late join and server restart pass.
G6 SP NOT TESTED; G7 dedicated BLOCKED / NOT TESTED; G8 BLOCKED.

No package was built, local mods deployed, Workshop item updated or game/server
launched. Existing dist/current dev.6 artifacts remain immutable historical
outputs. Any future authorized dev.7 packaging uses dist/development-current;
current output glob is declared in version-inventory.json. Fixed dev.5/dev.6
checkpoint scripts are historical and intentionally reject newer versions.

## Source evidence hashes (2026-10-14)

- media/lua/client/Entity/ISUI/BuildRecipe/ISBuildPanel.lua: `2b4bb8908dbf0158f68bc0a9c05b6d338fc1695d6fc9897b78e22010c342e05d`
- media/lua/server/BuildingObjects/ISBuildIsoEntity.lua: `6f485b0a90b9b8583fc8112aeddcb3f50a50bf7d1c0c6bc369138ee781deda38`
- media/lua/client/BuildingObjects/TimedActions/ISBuildAction.lua: `821c860dab239dcac22b507a5c90f2bcc888c64ce50896f81ff6d04a15ed0051`

Installed Steam build ID: 25485521. Exact loaded game version: UNKNOWN (not launched).

[TESTED Windows offline, 2026-10-14] scripts/test_current.py --available: 33
runnable tests PASS; five original-installed-baseline checks BLOCKED. Version
checker PASS. These results do not pass native G6/G7 or stable G8.
