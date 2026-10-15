# Vanilla fence and gate recipe re-audit

Project Version: 1.1.0-dev.14

[VERIFIED installed source/art, 2026-10-15] Steam build 25485521; full game version UNKNOWN.
[TESTED offline source/atlas comparison] No exact sprite-ID or identical-visible-art match
was found for any of the 30 planned parts. No recipe removal is required by this audit.
This is source availability evidence, not an in-game/SP/dedicated PASS.

## Scope and method

Fences and gates only. The 13 groups in vanilla-expansion.json stay unchanged.
No railings, stairs, balustrades, gabions, decorative loose wire or crowd barriers.
No game/server launch, package, deploy, Workshop update or gameplay change.
Project version stays dev.14 because this commit adds audit tooling, tests and
documentation; no runtime payload or construction recipe changes.

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
whole-source index fingerprints. New/unclassified literal Lua routes, missing
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
| Low wooden fence | Plain Section | No exact/identical-art vanilla match |
| Low wooden fence | Post-Ended Section | No exact/identical-art vanilla match |
| Low wooden fence | Corner | No exact/identical-art vanilla match |
| Low wooden fence | Standalone Post | No exact/identical-art vanilla match |
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
| Tall wooden gate (both fence tops) | Wide double gate | No exact/identical-art vanilla match |
| Green field gate | Wide double gate | No exact/identical-art vanilla match |

## Similar function versus duplicate artwork

Vanilla already supports low wooden fences, pole/wire fences and single/wide
wooden/metal gates. Those capabilities are not new. The proposed picket, ornate,
panel and tall-wood styles use artwork without a native recipe. Short/tall
chain-link plain sections and their native posts remain excluded; only their
missing post-ended sections and explicit corner pieces are added. The new brown
tall wooden wide gate is a different asset set from the vanilla DoubleDoor.

This comparison establishes exact/identical-art uniqueness. It does not prove
that every variant is mechanically different or that a player needs every
cosmetic variant. Those are design decisions, not missing-recipe findings.

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
