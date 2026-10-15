# Fence and gate catalog

Project Version: 1.1.0-dev.14

Scope: intact fence sections, their paid corners/posts and gates without vanilla
recipes. This is a PATCH correction to the unpublished 1.1.0 catalog expansion;
the overall PR remains a compatible MINOR feature within the unreleased series.
Display name: B47ANCE'd Fences & Gates. No package/deploy/upload/game launch.

## Follow-up vanilla recipe audit

See [VANILLA_RECIPE_AUDIT.md](VANILLA_RECIPE_AUDIT.md) for the broader per-entity,
all-script, skill/learning, Lua-route and identical-art comparison. None of the
30 planned parts duplicates exact vanilla recipe art or a pixel-identical alias.
The scoped list is unchanged. Vanilla has equivalent mechanical fence/gate
functions in different styles; the additions supply unavailable artwork.

## Inventory and exclusions

[VERIFIED installed source/art] Steam build 25485521; full runtime version UNKNOWN.
The expansion has 30 separately paid entities in 13 grouped menu entries.
The original 21 fences and iron gate, their recipes/costs and automatic junction
behavior remain unchanged. Vanilla recipe artwork, including corner/post helpers
and implicit double-gate opening states, is excluded from new recipes.

Architectural railings, stair fragments, handrails, stone balustrades, loose
nonfunctional wire, gabion baskets and crowd-control barriers are out of scope.
They have no new runtime entity, menu entry, callback policy or translation key.
The earlier 151-entry catalog was never packaged, deployed or published.
Burnt/damaged scenery is also excluded. Four textureless fencing_01_116-119
entries remain blocked. Military-top-bar and razor-topped gate art was not found;
no substitute artwork is invented. Existing vanilla chain-link gates remain.

catalog/vanilla-availability.json keeps the broader inspected tile inventory for
explicit disposition accounting: vanilla recipe, original mod, new fence/gate,
out of scope, or missing art. Excluded inventory entries are evidence, not
shipped content. Exact vanilla entity-script paths and SHA-256 fingerprints,
tile/atlas fingerprints and native builder fingerprints are retained.

| Menu group | New parts | Skill |
|---|---:|---|
| Ornamental iron fence | 3 | MetalWelding 3 |
| White picket fence | 3 | Woodwork 2 |
| Post and wire fence | 2 | Woodwork 2 |
| Short chain-link fence | 2 | MetalWelding 3 |
| Low wooden fence | 4 | Woodwork 3 |
| Sheet-metal panel fence | 4 | MetalWelding 5 |
| Tall chain-link fence | 2 | MetalWelding 3 |
| Razor-wire coil | 1 | MetalWelding 4 |
| Round-top picket fence | 3 | Woodwork 2 |
| Ornamental iron gate | 2 | MetalWelding 5 |
| White picket gate | 1 | Woodwork 4 |
| Tall wooden gate (both fence tops) | 2 | Woodwork 4 |
| Green field gate | 1 | MetalWelding 5 |

## Authoring and recipe invariants

catalog/vanilla-expansion.json is the reviewed source for new faces, materials,
skills, time and health. scripts/generate_expanded_catalog.py renders separate
entity/skin/Lua files and 29 English-fallback translation maps. Default mode
checks drift. --write updates only those outputs and removes the explicitly
listed retired labels; unknown/custom labels are preserved. The generator
rejects non-fence/gate families, decorative components and railing textures.
Scope regressions also enforce the exact approved family set and asset exclusions.

Each part retains an independent paid recipe. Wood uses a reusable hammer,
planks/nails; post-and-wire adds wire. Metal/wire uses native torch/rod uses,
pipes and scrap/wire. Gates add hinges and doorknobs. Wide gates and two-edge
corners use twice the corresponding single section material quantities.
Supports use smaller paid quantities. No original mod or vanilla cost is changed.
Item identities are checked against installed definitions. New balance still
requires playtesting. catalog/existing-contracts.json fingerprints original
recipes/callbacks independently of the project version.

Configuration assessment: recipe identity and native footprint define content,
not hidden behavioral options. Existing server ConstructionHealthPercent applies
to new sections/gates with its existing bounds and default. Posts keep their
baseline health. Existing corner-post options apply only to their original four
families; new families use their paid explicit corners/posts. No microsettings,
new art, custom geometry or client preferences affect shared state.

## Authority, persistence and compatibility

[VERIFIED source] Only the existing vanilla builder and BuildLogic perform
recipe validation, item payment and placement. The custom model selects exact
ObjectInfo/recipe/face records; it sends no custom commands. ISBuildIsoEntity
processes recipe consumption before iterating the chosen face tiles; the same
native path creates and normally transmits every tile, including multi-tile
gates. New OnCreate code runs server/SP only, checks class plus exact name,
sprite and orientation, and applies sounds and bounded health settings. It
changes no sprite, door/collision flag, inventory, topology or other object.
Missing/wrong objects and client calls do nothing. No runtime test/debug helpers.

No per-tick scans, retrofits, schema, migrations, permanent custom markers or
custom synchronization are added. Existing saves are untouched until a paid
object is built. Native objects own persistence and late-join synchronization;
these paths are source-verified, but actual engine behavior remains untested.
Downgrading cannot be assumed to remove placed objects or preserve unfamiliar
entity definitions; use backed-up disposable test saves. Old packages/provenance
remain protected; future authorized output is dist/full-catalog-development-current.

## Validation and native gates

Exact offline commands/results are in TESTING.md. Tests cover scope rejection,
retired label removal in 29 languages, complete inventory dispositions, vanilla
recipe exclusion, real paid inputs, native double-gate layout, both-axis cycling,
affordability/action freeze, exact server callback validation and unchanged
original contracts. Tests use Python/Lupa mocks, not the game engine.

[RUNTIME GATE] New fences: placement, orientation, collision/hopping, costs,
tool use, cancellation, skills, damage and health settings. Single/wide gates:
clearance, all leaves opening/closing, locks, damage/dismantling, occupied squares
and both axes. SP save/reload plus dedicated two-client build visibility,
join/rejoin, duplicate prevention, persistence and restart remain required.
G6 SP NOT TESTED; G7 dedicated BLOCKED / NOT TESTED; stable G8 BLOCKED.
