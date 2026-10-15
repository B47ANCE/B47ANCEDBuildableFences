# Expanded intact vanilla fence catalog

Project Version: 1.1.0-dev.13

Compatible MINOR feature within the unreleased 1.1.0 development series.
User scope: all intact fences, railings and gates, but only assets that do not
already have vanilla recipes. No deployment, package, upload or game launch.

## Inventory and exclusion

[VERIFIED installed source/art, Steam build 25485521; full runtime version UNKNOWN]
The bounded collections are fencing_01, fixtures_railings_01 and
fixtures_doors_fences_01. Burnt/damaged sets are excluded. Existing mod art and
vanilla recipe art are excluded from additions. The snapshot
catalog/vanilla-availability.json records exact vanilla entity-script paths and
SHA-256 fingerprints, tile/atlas fingerprints and every asset disposition.
Vanilla corner/post helpers and implicit double-gate opening states are counted
as already supplied. No base-game files are changed.

Four fencing_01_116-119 definitions have no matching texture name in any
installed texture pack: [UNKNOWN artwork], blocked from construction. No
placeholder or invisible build recipe substitutes for them. No matching
military-top-bar or razor-coil gate artwork exists in the inspected gate sheet;
no invented variants are added. Vanilla chain-link gates remain available.

The new catalog has 151 separately paid entities in 28 grouped menu entries,
including small support and stair components, not 151 full fence styles.
The original 21 fence entities and iron gate remain unchanged. Native wooden,
wire and pole gate recipes remain untouched and are not cloned. New single gates
supply W/N closed/open faces; wide gates reuse the verified vanilla four-tile
layout and DoubleDoor sprite offsets. All 106 intact railing entries are
accounted for. Stair fragments and loose wire without complete barrier flags
are labelled decorative components, retain vanilla geometry and require manual
placement. No automatic stair assembly or extra collision is promised.

| Menu group | Added parts | Skill |
|---|---:|---|
| Ornamental iron fence | 3 | MetalWelding 3 |
| White picket fence | 3 | Woodwork 2 |
| Post and wire fence | 2 | Woodwork 2 |
| Short chain-link fence | 2 | MetalWelding 3 |
| Low wooden fence | 4 | Woodwork 3 |
| Sheet-metal panel fence | 4 | MetalWelding 5 |
| Tall chain-link fence | 2 | MetalWelding 3 |
| Stone balustrade | 3 | Masonry 5 |
| Razor-wire coil | 3 | MetalWelding 4 |
| Crowd-control barrier | 2 | MetalWelding 3 |
| Round-top picket fence | 3 | Woodwork 2 |
| Military gabion barrier | 8 | MetalWelding 4 |
| Slim wooden railing | 8 | Woodwork 2 |
| Slim metal stair railing | 8 | MetalWelding 3 |
| Wooden baluster railing | 7 | Woodwork 2 |
| Slim wooden level railing | 3 | Woodwork 2 |
| Slim metal level railing | 3 | MetalWelding 3 |
| Brown wooden handrail | 18 | Woodwork 2 |
| White baluster railing | 15 | Woodwork 2 |
| Dark wooden handrail | 13 | Woodwork 2 |
| White slim railing | 8 | MetalWelding 3 |
| White panel railing | 4 | MetalWelding 3 |
| Dark panel railing | 4 | MetalWelding 3 |
| White wooden handrail | 15 | Woodwork 2 |
| Ornamental iron gate | 2 | MetalWelding 5 |
| White picket gate | 1 | Woodwork 4 |
| Tall wooden gate (both fence tops) | 2 | Woodwork 4 |
| Green field gate | 1 | MetalWelding 5 |

## Authoring and recipes

catalog/vanilla-expansion.json is the reviewed source for new parts, faces,
materials, skills, time and health. scripts/generate_expanded_catalog.py renders
only the separate overlay entity/skin/catalog files and 29 IG_UI fallback maps.
Its default mode checks drift; --write updates those declared outputs. It never
builds a package, connects to Steam or touches installed mods. Existing manual
poster/branding are preserved; menu icons reuse the verified fallback icon.

New wood recipes use a reusable hammer, planks and nails; metal/wire recipes use
native torch/rod uses, pipes and scrap/wire. Stone uses a reusable mason's trowel,
stone blocks and mixed concrete uses. Gates add hinges and doorknobs; wide gates
cost twice the single-sized material quantities. Smaller posts/decorative pieces
have smaller paid material requirements. Post-and-wire uses wood, nails and wire. Paid two-edge corners cost twice the
straight section materials. Gabions consume torch/rod uses, wire, sheets, a sack
and appropriate fill uses (empty versions have no fill). Item identities and
consumable forms are checked against installed item definitions. Balance is an
initial proposal requiring playtesting; no old recipe cost/skill/time/health is
changed. catalog/existing-contracts.json fingerprints existing recipes/callbacks
independently of the version header.

Configuration assessment: parts are explicit build choices; recipes, material
identity and footprint are fixed content rather than hidden behavioral options.
The existing server ConstructionHealthPercent setting applies to new sections,
gates and barriers with the existing bounds/default; standalone supports keep
their declared health, matching current post policy. No per-sprite microsettings
are added. Existing automatic junction settings apply only to their original
four families; expansion pieces use paid explicit corners and posts.

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

## Validation and remaining runtime gates

Exact commands and current offline results are recorded in TESTING.md.
Offline Python/Lupa tests execute selection and callback behavior, check all
new recipes/labels, prevent vanilla duplicates, verify double-gate layouts and
fingerprint old recipes. Mock objects are not PZ physics or multiplayer proof.

[RUNTIME GATE] All new styles: placement/orientation, native recipe payment and
cancellation, skill/tool restrictions and health settings. Level/stair railings:
correct height/alignment, collision/hopping, supports and placement near stairs.
Single/wide gates: both axes, clearance, complete open/close, all leaves, locks,
damage, dismantling and occupied-square rejection. Gabions and wire components:
footprint, fill use accounting and collision. SP save/reload and dedicated
two-client placement, visibility, join/rejoin, duplication, persistence and
restart testing remain required. G6 SP NOT TESTED; G7 dedicated BLOCKED /
NOT TESTED; stable-release G8 BLOCKED. No stable/readiness claim.
