# Badlands Privacy Fence functional reference audit

Date: 2026-10-02. [VERIFIED, source] BADLANDS Furniture 0.8.12, Workshop
3804156157, technical Mod ID FullBookcases; native PZ 42.21. No runtime test.
Prior audit preserved in evidence/history/1.1.0-dev.2/docs.

The Privacy Fence presentation reference is: ONE
Privacy Fence entry and ONE Privacy Gate entry, placement rotation, linked art
and automatic posts. The previous recommendation to retain manual B47 variants
did not address that target. Absence of custom Lua does not imply absence of
automatic construction: Privacy Fence delegates to the native entity builder.

Reference root: E:/Program Files (x86)/Steam/steamapps/workshop/content/108600/3804156157/mods/FullBookcases/42.
Native root: E:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid.
SOURCE CODE COPIED: NO. IMPLEMENTATION DERIVED FROM REFERENCE CODE: NO.
Functionality is the reference; B47 topology is independently implemented using
its own baseline and vanilla art. No private art, code, balance or dependency.

## Actual construction path

Badlands `media/scripts/entities/knx_fences.txt:52` defines KNX_FencePrivacy;
`knx_fences_xuiSkin.txt` supplies ES_KNX_FencePrivacy. One recipe uses W
badlands_fencing_01_10, N _8, corner _13. KNX_GatePrivacy is a separate entity
with its own closed/open W/N faces. No privacy plain/end/corner/post recipes.

Native `media/lua/client/Entity/ISUI/ISEntityBuildMenu.lua` createMenu,
buildCategoryMenu and onBuildEntity enumerate ObjectInfo and construct the
cursor. `Entity/ISUI/BuildRecipe/ISBuildPanel.lua` refreshList and
createBuildIsoEntity use BuildLogic's recipe-to-entity lookup and the same
ISBuildIsoEntity cursor. These are two menu paths, both checked.

`media/lua/server/BuildingObjects/ISBuildIsoEntity.lua` new stores objectInfo,
nSprite and getCornerSprite; rotateKey/getFace choose native W/N faces and
cacheSprites/render draw them. `media/lua/client/BuildingObjects/TimedActions/
ISBuildAction.lua` start invokes createBuildAction with placement/cursor intent;
clients wait and do not construct in perform. Native ISBuildIsoEntity.create/
setInfo on authority consumes recipe, selects face, creates IsoThumpable,
derives wall/door flags, initializes health/entity state, adds the world object,
calls buildUtil.checkCorner, then OnCreate and complete-object transmission.

`media/lua/server/BuildingObjects/ISBuildUtil.lua` checkCorner/addCorner is the
automatic post mechanism. For north, it checks (x+1,y-1); for west (x-1,y+1),
looking for an opposite-north IsoThumpable in special objects. It inserts an
extra corner at (x+1,y) or (x,y+1) unless getWallFull exists there. addCorner
creates an IsoThumpable with `_13`, setCorner(true), adds/recalculates/transmits
it. This extra post does not rotate the requested section. It is not restricted
to Privacy identity and does not replace neighboring sections' sprites.

## Sixteen requested questions

| Question | Source finding and limit |
|---|---|
| One item/multiple configurations | Single entity W/N faces plus separate native corner post; not four variant recipes |
| Rotation | rotateKey traverses WNES, getFace maps native NWSE indices and skips missing faces. One ROTATE_BUILDING keyboard binding found; reverse controller LBumper/RBumper exists. Two native Q/E keyboard bindings not established |
| W/N | Selected nSprite determines face and north. W tile WallW, N WallN |
| Neighbor detection | Native diagonal-square opposite-axis checkCorner path above |
| Texture links | Repeated section art plus automatic junction post. User-observed cohesion is the target; no local overlap/depth runtime measurement |
| Corners | Extra corner/post object _13, not NW section replacing player's edge |
| End posts | Embedded section art; no terminal detection/rewrite routine found |
| Intermediate posts | Repeated art and eligible checkCorner insertions; no explicit spacing/deduplication routine found |
| Neighbor recalculation | RecalcAllWithNeighbours updates square properties/collision/render state, not proof of neighboring sprite rewrite. No such Privacy rewrite found |
| Removal/destruction | No Privacy-specific topology/removal handler found in Lua or inspected native construction methods. Resulting post removal/reconfiguration [UNKNOWN]/[RUNTIME GATE] |
| Gate adjacency | Separate native gate placed in run; no family-aware gate-neighbor mutation found |
| Preview | Native selected face ghost; inspected render has no extra checkCorner ghost/neighbor prediction |
| Collision | WallW/WallN/native flags and isCorner extra object established; walking/hopping/junction collision [RUNTIME GATE] |
| Cutaway | Private tile metadata and native IsoThumpable renderer; no custom Privacy alpha/type handler found. B47 wooden fault not explained |
| Save/load | Native sprites, flags, health and door state serialized; exact restored layout [RUNTIME GATE] |
| MP equality | Native authoritative creation/full-object and door replication. Late join/reconnect/identical views [RUNTIME GATE] |

Classification: selected predefined W/N faces, posts embedded in art, separate
native junction object. No evidence for general family-aware variant/neighbor
rewrite or Privacy-specific attached sprites. The rejected dev.3 B47 topology
extension is archived; dev.4 follows player-selected existing pieces instead.

## Gate and cutaway

Privacy Gate uses badlands_gates_01_12/13 closed,14/15 open, dontNeedFrame and
BreakDoor. Native IsoThumpable ToggleDoorActual, TestCollide/TestPathfindCollide,
save/load and syncIsoObjectSend/Receive own interaction/collision/persistence/
sync. No custom locking choice found. This wooden reference does not establish
metallic gate sound behavior.

Private tile file `media/badlands_bookcase_01.tiles.txt`: _8 WallN/TallHoppableN,
_10 WallW/TallHoppableW, both wall/Wood/Wood_Solid; _13 WallSE/NoWallLighting,
without WallW/WallN. These are registered private tiles. No proven constructor-
only explanation for B47 premature wooden disappearance. Paired loaded-object
renderer evidence remains required; no global type/alpha/cutaway changes.

## Equivalent B47 architecture

Re-audit for the corrected request: Privacy Fence's native nSprite/getFace
sequence selects W/N textures of ONE entity and ONE fixed CraftRecipe. It does
not demonstrate switching Plain/Corner/Post recipes with different costs.
The selected face supplies render/cacheSprites and create/setInfo's tile;
ISBuildAction carries the chosen cursor state to authority. The installed
reference has no private Q/E recipe-switching hook; one native keyboard rotate
binding was found, not independent Q/E actions. No Badlands code/art is copied.

Corrected isolated B47 architecture extends native face selection to existing
entity selection: Plain W/N -> Post-Ended W/N -> Corner S -> Post S. Q reverses;
each state uses its original ObjectInfo and CraftRecipe. Native rendering and
server construction remain the execution path. Live UI requirements come from
that selected recipe. Corners and standalone posts remain actual selectable
assets; no generated posts, topology scans/repairs or neighbor sprite writes.
Gate stays separate and cycles only closed placement faces. No generalization
until native/dedicated tests pass. See COHESIVE_PROTOTYPE_REPORT.md.
