# B47ANCE'd Buildable Fences

Project Version: 1.1.0-dev.7

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
