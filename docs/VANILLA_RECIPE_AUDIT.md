# Vanilla fence and gate recipe re-audit

Project Version: 1.1.0-dev.15

[VERIFIED installed source/art, 2026-10-15] Steam build 25485521; full game version UNKNOWN.
[VERIFIED installed source] The earlier exact-art audit was too narrow: different
artwork does not justify adding a practical duplicate. Preview parts 11-14 (all
four low wooden fence pieces) and 29 (wide wooden gate) are removed per user
correction. The expansion now contains 25 parts in 12 groups. Remaining exact-art
findings are source evidence, not a claim of exhaustive functional uniqueness.
No in-game/SP/dedicated PASS is claimed.

## Scope and method

Fences and gates only. No railings, stairs, balustrades, gabions, decorative loose
wire or crowd barriers. This compatible PATCH correction to the unpublished
expansion is dev.15; the overall feature remains a MINOR addition within 1.1.0.
No game/server launch, package, deploy or Workshop update.

The repeatable checker is scripts/audit_vanilla_recipes.py. It scans all 1,004
installed script text files, not just the generated fence directory. It binds
SpriteConfig and CraftRecipe per entity, including split component files, rather
than attributing every sprite in a shared file to every recipe. The scan finds
194 construction entities and 986 supplied sprite identities, including helper
posts/corners and implicit double-gate opening states. All corresponding artwork
is accounted for in Tiles2x.pack and Tiles2x.floor.pack. Visible RGBA comparisons
ignore transparent padding and detect identical art under different sprite names.

The checker also scans 1,407 Lua files. Fence/gate/railing asset literals occur
only in debug brush/scenario code and damage/bending tables. ISBuildMenu offers
ramps; ISInventoryBuildMenu handles inventory/build interactions such as fill
materials. ISEntityBuildMenu obtains buildables through native ISBuildIsoEntity.
The native GetAllBuildableEntities includes ObjectInfo records with a script and
recipe. No additional multistagebuild definitions were found in installed scripts.

Learned recipes and skill-gated building levels count as vanilla availability.
The absence of an option for an unskilled/untrained character is not justification
for cloning the recipe. Wooden fence callbacks select level 1 below Carpentry 5,
level 2 at 5-6 and level 3 at 7+. Existing fence/gate recipes and those callbacks
remain untouched. No claim is made about UI behavior beyond source inspection.

catalog/vanilla-recipe-audit.json records each candidate, exact/alias matches,
the 24 vanilla fence/gate/stake recipes, skill/menu conditions, source hashes and
whole-source index fingerprints. Reviewed functional exclusions are validated
by the generator and checker even when art differs. New/unclassified literal Lua routes, missing
art, changed source indexes, or candidate overlaps fail the check for review.

## Vanilla recipes excluded from the additions

These are source-defined vanilla recipes. A learned requirement or skill filter
does not turn a recipe into missing content.

| Vanilla entity | Skill declared | Learned recipe |
|---|---|---|
| BarbedWireFence | Carpentry 5 | No |
| BrickFenceLvl2 | Masonry 5 | No |
| DoubleDoor | Carpentry 4 | No |
| DoubleFenceGate | Welding 5 | Yes |
| DoubleWireGate | Welding 5 | Yes |
| LogFence | Not declared in this recipe | No |
| LogGate | Not declared in this recipe | No |
| MetalBigMetalFence | Welding 3 | Yes |
| MetalBigWireFence | Welding 3 | Yes |
| MetalFenceLvl1 | Welding 3 | Yes |
| MetalFenceLvl2 | Welding 5 | No |
| MetalPoleFenceGate | Welding 3 | Yes |
| MetalPoleFenceGateSmall | Welding 3 | Yes |
| MetalSmallPoleFence | Welding 3 | Yes |
| MetalSmallWireFence | Welding 3 | Yes |
| MetalWireFenceGate | Welding 3 | Yes |
| MetalWireFenceGateSmall | Welding 3 | Yes |
| StickFence | Not declared in this recipe | No |
| WoodFenceGate | Carpentry 3 | No |
| WoodFenceLvl1 | Carpentry 3 | No |
| WoodFenceLvl2 | Carpentry 5 | No |
| WoodFenceLvl3 | Carpentry 7 | No |
| WoodStake | Not declared in this recipe | No |

## Per-part results

Every entry below has no vanilla recipe for its exact artwork and no
pixel-identical alias among native construction art.

| Planned family | Part | Result |
|---|---|---|
| Ornamental iron fence | Plain Section | No exact/identical-art vanilla match |
| Ornamental iron fence | Corner | No exact/identical-art vanilla match |
| Ornamental iron fence | Standalone Post | No exact/identical-art vanilla match |
| White picket fence | Plain Section | No exact/identical-art vanilla match |
| White picket fence | Corner | No exact/identical-art vanilla match |
| White picket fence | Standalone Post | No exact/identical-art vanilla match |
| Post and wire fence | Plain Section | No exact/identical-art vanilla match |
| Post and wire fence | Corner | No exact/identical-art vanilla match |
| Short chain-link fence | Post-Ended Section | No exact/identical-art vanilla match |
| Short chain-link fence | Corner | No exact/identical-art vanilla match |
| Sheet-metal panel fence | Plain Section | No exact/identical-art vanilla match |
| Sheet-metal panel fence | Window Section | No exact/identical-art vanilla match |
| Sheet-metal panel fence | Corner | No exact/identical-art vanilla match |
| Sheet-metal panel fence | Standalone Post | No exact/identical-art vanilla match |
| Tall chain-link fence | Post-Ended Section | No exact/identical-art vanilla match |
| Tall chain-link fence | Corner | No exact/identical-art vanilla match |
| Razor-wire coil | Plain Section | No exact/identical-art vanilla match |
| Round-top picket fence | Plain Section | No exact/identical-art vanilla match |
| Round-top picket fence | Corner | No exact/identical-art vanilla match |
| Round-top picket fence | Standalone Post | No exact/identical-art vanilla match |
| Ornamental iron gate | Single gate | No exact/identical-art vanilla match |
| Ornamental iron gate | Wide double gate | No exact/identical-art vanilla match |
| White picket gate | Single gate | No exact/identical-art vanilla match |
| Tall wooden gate (both fence tops) | Single gate | No exact/identical-art vanilla match |
| Green field gate | Wide double gate | No exact/identical-art vanilla match |

## Reviewed functional overlaps

Low wooden fence pieces fencing_01_32-37 are excluded as practical equivalents
of vanilla WoodFenceLvl1/2/3, with Carpentry 3/5/7 respectively. The completed
level-3 fence uses carpentry_02_48/49 with corner 51 and consumes 2 planks and
2 nails with a reusable hammer. Its art differs from the removed proposal;
that difference is not grounds for reintroducing the user-excluded family.

The wide wooden gate fixtures_doors_fences_01_48-63 is excluded as a practical
equivalent of vanilla DoubleDoor. That native recipe needs Carpentry 4, a
reusable hammer, 8 planks, 8 nails, 4 hinges and 2 doorknobs. It uses the native
96-111 sprite block. The single tall wooden gate remains for both fence tops.

catalog/vanilla-expansion.json records excluded names and sprite identities,
with source-backed native entity identities. The generator rejects both reused
names and renamed recipes with those sprites. The audit binds each reviewed
exclusion to current native recipe proofs. vanilla-availability.json accounts
for these as functional equivalents, separate from exact vanilla sprite matches.
These are reviewed exclusions, not an automated semantic-equivalence detector.

## White picket fence recipe and paint check

[VERIFIED installed source] No native construction recipe supplies white picket
fence sprites fencing_01_4-7. The broad script scan includes skill/learning-gated
recipes. entity_wood_picket.txt defines WoodPicket as a marker post using
location_community_cemetary_01_31, one plank and one sheet rope; it is not a
white picket fence recipe. Its naming alone must not be treated as a match.

PaintingReference.lua has white tint for the crates painting category used by
native wooden fence sections, but no fencing_01 sprite conversion. ISPaintAction
selects a Painting sprite replacement or uses OtherPainting with setCustomColor
and transmitCustomColorToClients. A white tint does not create the specific
picket shape. No recipe or painting route to that fence set was found in the
installed evidence. The three white picket fence pieces remain planned.

The audit report fingerprints the marker, paint reference and paint action.
This is a source conclusion for Steam build 25485521; actual painting behavior
and construction in the game are NOT TESTED. Other proposed visual variants
still require design/runtime review; exact-art uniqueness alone is insufficient.

## Validation and remaining limits

Commands from repository root (Python with Pillow and Lupa for the full suite):
```
python scripts/audit_vanilla_recipes.py
python -m unittest discover -s tests -p test_vanilla_recipe_audit.py -v
python scripts/test_current.py --available
python scripts/check_versions.py --root .
python scripts/generate_expanded_catalog.py
python scripts/prepare_workshop.py
```

The audit uses source and atlas fingerprints for this exact installed build.
A game update requires a new audit. Raw vanilla code and atlas pixels are not
copied into the repository. Source records and hashes are not runtime evidence.
Placement, payment/cancellation, collision, gate operation, save/reload and
dedicated two-client synchronization, joins and restarts remain untested.
G6 SP NOT TESTED; G7 dedicated BLOCKED / NOT TESTED; stable G8 BLOCKED.
