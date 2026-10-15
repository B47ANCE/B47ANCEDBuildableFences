# B47ANCE'd Fences & Gates

Project Version: 1.1.0-dev.13

Standalone Build 42 mod, technical ID B47ANCEDBuildableFences, Workshop ID
3817174798. Editable source is `src/B47ANCEDBuildableFences/42`.
Recovered from the downloaded Workshop baseline at the user's direction on
2026-10-02. Installed Workshop files are not edited or deployed automatically.

Baseline file hashes: docs/evidence/baseline-1.0.37/hashes.json.
This establishes file provenance, not new runtime proof. User-provided collision
evidence for the baseline remains historical. Dedicated multiplayer evidence is
still required for the development candidate.

The development overlay in prototypes/cohesive/42 consolidates all six fence
families into one build-menu entry each. Q/E and controller bumpers select
individual parts and orientations, retaining every part's original recipe,
materials, skills and construction time. The iron gate remains separate.
The source/overlay composition is unchanged from dev.6. See
[family selectors](docs/FAMILY_SELECTORS.md) for implementation and validation.
Native collision/save/dedicated testing is pending.

The development source defines 21 buildable pieces, including four wrought-iron
variants. Security and Razor recipes consume mixed concrete uses rather than
Scrap Metal. Material fallback/break initialization runs on the construction
authority. All 29 language folders have English fallback names and sandbox text.

Construction requirements apply to every variant in each family:

| Family | Required skill |
|---|---|
| Tall Wooden Straight Top (fence, corner, post) | Carpentry 4 |
| Tall Wooden Sloped Top (post-ended, continuous, corner, post) | Carpentry 7 |
| Security (plain, post-ended, corner) | Welding 4 |
| Razor-Wire Security (plain, post-ended, corner) | Welding 4 |
| Military (plain, post-ended, corner, post) | Welding 7 |
| Wrought Iron (plain, post-ended, corner, post) | Welding 7, unchanged |

The earlier skill checkpoint changed nine construction skill requirements. Materials,
XP rewards, health fields and runtime behavior code are preserved. See
[skill rebalance report](docs/SKILL_REBALANCE_REPORT.md) for exact changes.

Wooden cutaway has no proven root cause or applied fix. Audio correctness,
collision, partial concrete use and dedicated persistence remain runtime gates.
This candidate is not release-ready. An explicitly untested Workshop package
has been prepared at the user's request for dedicated-server testing. See
[test release record](docs/WORKSHOP_DEV5_TEST_RELEASE.md).

See [legacy compatibility audit](docs/LEGACY_COMPATIBILITY.md) for the exact
17 retained 1.0.37 identities and source-only startup fix. Native save safety
is untested. Local test-copy state is historical; this checkpoint updates Workshop only. See [deployment report](docs/DEPLOYMENT_DEV5.md).

See [implementation report](docs/IMPLEMENTATION_REPORT.md),
[testing handoff](docs/TESTING.md), [architecture](docs/ARCHITECTURE.md),
[sprite audit](docs/WROUGHT_IRON_SPRITE_AUDIT.md),
[concrete audit](docs/CONCRETE_RECIPE_AUDIT.md), and
[sound audit](docs/MATERIAL_BEHAVIOR_AUDIT.md).

## Prior dev.6 checkpoint

The developer test kit was removed from the active overlay: no kit menu, slash
command, spawn handler or kit translation keys ship. Earlier kit instructions
and native evidence describe historical dev.5 only. Construction, recipes,
selector/gate behavior and authority are retained. G6/G7 NOT TESTED; G8 BLOCKED.

## Prior dev.6 checkpoint

The developer test kit is removed: no kit menu, command, spawn handler or kit
translation keys ship. Earlier kit instructions describe historical dev.5.
Fence construction and the selector/gate are unchanged. G6/G7 NOT TESTED; G8 BLOCKED.

## Workshop preparation

The current version-driven entry point is `scripts/prepare_workshop.py`.
Run it without arguments for a read-only shipped-content preflight. After the
intended release inputs are committed and pushed, `--prepare` creates an
unpublished candidate under `dist/workshop-candidates/<VERSION>` and its ZIP
under `dist/development-current`. See [preparation](docs/WORKSHOP_PREPARATION.md).
Offline tests stay in `tests/`; they are never included in the mod payload.
Earlier version-pinned scripts remain historical checkpoint tools, not current
build/deploy commands. No diagnostic startup print or test-only tooltip export
is shipped. Required native and dedicated checks still block stable publication.

## Wrought-iron corner connections (dev.9)

New matching perpendicular wrought-iron sections can add a native junction post
included in their existing section cost. Server sandbox WroughtIronCornerPosts
defaults on; disabling affects future generation only. No existing objects are
scanned or rewritten. See docs/WROUGHT_IRON_CONNECTIONS.md for authority, configuration,
regressions and native limitations. Future packages use the inventory-declared
dist/corner-development-current directory; old dev.8 artifacts remain historical.

## Additional fence-family connections (dev.10)

Extends the dev.9 server-only native corner wrapper to military (post53),
sloped-top wood (post13) and straight-top wood (post74), all fencing_01 sprites.
Only exact same-family perpendicular sections connect; the two wooden styles
remain separate. Server sandbox MilitaryCornerPosts, SlopedWoodCornerPosts and
StraightWoodCornerPosts default true, independently of the existing iron option.
Missing old-save options default true; invalid values disable future generation.
All paid recipes, costs, skills, time, health and gates remain unchanged.
Security and razor-wire stay unchanged by explicit user choice: their vanilla
sets have no standalone post85/93; wall corners84/92 are not substitute posts.
No old-save scan, retrofit, orphan cleanup, custom commands or client writes.
49 available offline tests pass; five original-baseline checks remain blocked.
G6 SP NOT TESTED; G7 dedicated BLOCKED / NOT TESTED; stable G8 BLOCKED.
See WROUGHT_IRON_CONNECTIONS.md for native authority and runtime test matrix.

## Expanded intact vanilla catalog (dev.12)

The current catalog adds 151 entries in 28 groups only where no vanilla recipe
supplies that art. The original six families and iron gate retain their recipes.
Vanilla gates/fences are not duplicated. New shared wooden gates serve both tall
wood styles. Decorative stair components retain their original native flags.
Four textureless fencing_01_116-119 definitions remain explicitly blocked.
See docs/VANILLA_CATALOG.md (VANILLA_CATALOG.md within docs) for scope, costs,
source fingerprints, authority and required native SP/dedicated testing.

## Display-name update (dev.13)

The next authorized upload is titled B47ANCE'd Fences & Gates. The mod.info name
is authoritative for future Workshop title metadata and the sandbox page uses
the same display name. Technical ID B47ANCEDBuildableFences, Workshop item
3817174798, repository and source directories remain unchanged. Existing manual
artwork is preserved. This metadata change does not publish or deploy anything.
