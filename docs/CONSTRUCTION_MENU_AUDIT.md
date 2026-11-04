# Construction menu visibility audit

Project Version: 1.1.0-dev.20

[VERIFIED source / TESTED Windows offline Python+Lupa, 2026-11-01]
Installed Steam build 25485521; full game version UNKNOWN.
The development source contains 47 paid recipes: 41 fence parts and 6 gates.
All are covered by 19 normal grouped construction entries. Q/E and controller
bumpers select each family's parts/orientations with their own paid recipe.
This report does not claim that all 47 appear as separate menu rows.

## Finding and bounded fix

The old construction-tab refresh unconditionally removed every non-root part.
An offline case returning only RazorWireSecurityFence_PostEndedSection produced
zero visible entries; the same problem reproduced for the other grouped parts.
That is a confirmed filter defect under partial native lists. It is NOT a
confirmed reproduction of the Workshop reporter's engine/session conditions.

The tab now prefers the normal root only when that recipe is actually in the
native list. Otherwise the first native-supplied member represents its family.
It never inserts a recipe missing from the native list, changes native eligibility
filters, rewrites recipe identity, or removes/reorders unrelated mod/vanilla
entries. Empty native lists remain empty. Native reselection is retained.

All ObjectInfo/CraftRecipe registrations remain intact. Material/tool inputs,
skill/learning conditions, native BuildLogic validation, payment, server-owned
construction, health settings, saves and synchronization are unchanged.
This is a compatible PATCH UI correction, with no new gameplay setting needed.

## Full source inventory

Every recipe has UiConfig, SpriteConfig and CraftRecipe components, category
Fences, a valid skin/display-name binding in all 29 composed language maps,
positive paid inputs and an explicit Carpentry/Welding requirement. None has
an additional learned-recipe or OnAddToMenu gate. All 47 are exercised through
the construction-panel cursor and retain their own recipe and construction time.

| Construction entry | Recipes | Parts selectable in this entry | Skill |
|---|---:|---|---|
| Tall Wooden Fence (Straight Top) | 3 | Tall Wooden Fence (Straight Top); Tall Wooden Fence (Straight Top Corner); Tall Wooden Fence (Straight Top Post) | Carpentry 4 |
| Tall Wooden Fence (Sloped Top) | 4 | Tall Wooden Fence (Sloped Top); Tall Wooden Fence (Sloped Top); Tall Wooden Fence (Sloped Top Corner); Tall Wooden Fence (Sloped Top Post) | Carpentry 7 |
| Military Fence | 4 | Military Fence; Military Fence (Post-Ended Section); Military Fence (Corner); Military Fence (Post) | Welding 7 |
| Security Fence | 3 | Security Fence; Security Fence (Post-Ended Section); Security Fence (Corner) | Welding 4 |
| Razor-Wire Security Fence | 3 | Razor-Wire Security Fence; Razor-Wire Security Fence (Post-Ended Section); Razor-Wire Security Fence (Corner) | Welding 4 |
| Wrought Iron Fence | 4 | Wrought Iron Fence; Wrought Iron Fence (Post-Ended Section); Wrought Iron Fence (Corner); Wrought Iron Fence (Post) | Welding 7 |
| Ornamental iron fence - Plain Section | 3 | Ornamental iron fence - Plain Section; Ornamental iron fence - Corner; Ornamental iron fence - Standalone Post | Welding 3 |
| White picket fence - Plain Section | 3 | White picket fence - Plain Section; White picket fence - Corner; White picket fence - Standalone Post | Carpentry 2 |
| Post and wire fence - Plain Section | 2 | Post and wire fence - Plain Section; Post and wire fence - Corner | Carpentry 2 |
| Short chain-link fence - Post-Ended Section | 2 | Short chain-link fence - Post-Ended Section; Short chain-link fence - Corner | Welding 3 |
| Sheet-metal panel fence - Plain Section | 4 | Sheet-metal panel fence - Plain Section; Sheet-metal panel fence - Window Section; Sheet-metal panel fence - Corner; Sheet-metal panel fence - Standalone Post | Welding 5 |
| Tall chain-link fence - Post-Ended Section | 2 | Tall chain-link fence - Post-Ended Section; Tall chain-link fence - Corner | Welding 3 |
| Razor-wire coil - Plain Section | 1 | Razor-wire coil - Plain Section | Welding 4 |
| Round-top picket fence - Plain Section | 3 | Round-top picket fence - Plain Section; Round-top picket fence - Corner; Round-top picket fence - Standalone Post | Carpentry 2 |
| Ornamental iron gate - Single gate | 2 | Ornamental iron gate - Single gate; Ornamental iron gate - Wide double gate | Welding 5 |
| White picket gate - Single gate | 1 | White picket gate - Single gate | Carpentry 4 |
| Tall wooden gate (both fence tops) - Single gate | 1 | Tall wooden gate (both fence tops) - Single gate | Carpentry 4 |
| Green field gate - Wide double gate | 1 | Green field gate - Wide double gate | Welding 5 |
| Wrought Iron Gate | 1 | Wrought Iron Gate | Welding 7 |

The barbed-wire-topped tall set is named **Razor-Wire Security Fence** and needs
Welding 4. Its post-ended piece and corner use the same grouped selector.
No dedicated razor-wire gate is implemented. All six implemented gates above
are tested; this audit does not invent a seventh gate or duplicate native
learned gate recipes.

## Workshop report versus current source

At the time of the dev.18 audit, public item 3817174798 advertised 1.1.0-dev.10. Its installed
files contain the three razor-wire recipes and the single wrought-iron gate;
they do not contain the 25-part expansion. Versions dev.17 and dev.18 are source
iterations, not evidence of successful Workshop distribution. No upload or
local deployment occurs during this audit. The pending SteamCMD authentication
issue is separate from this source fix.

Subsequent distribution [VERIFIED Steam upload/API, 2026-11-01]: dev.18 was
published after PR #8 merged. The prior paragraph describes pre-upload evidence,
not the current public version. The dev.19 build-start investigation is recorded
separately in CONSTRUCTION_ACTION_COPY.md; it does not change the menu filter.

The reporter's game version, SP/MP context, filters and runtime logs are unknown.
The developer's available local console is dated October 24 and was not treated
as a reproduction of this external report. No failure is attributed to another
mod without reproduction evidence.

## Installed environment and clean-room boundary

The source game build remains 25485521. The old full-suite fingerprint failed
because the installed Lua set now contains 1,409 files rather than 1,407.
Developer-local pzopt overlay files have newer timestamps. Review found only
the Lua count/index fields changed in the generated report; recipe scripts,
recorded build-menu source hashes, tile/atlas hashes and candidate findings were
unchanged. The environment snapshot was refreshed explicitly, not skipped.
No external mod implementation was copied or used to design this fix. See
THIRD_PARTY_RESEARCH.md for the bounded observation and unresolved provenance.

## Validation and remaining runtime gate

New tests: tests/test_construction_menu_visibility.py. Seven test methods check
all registrations/translations, 19 roots and all 47 selectable recipes, every
recipe in isolation, secondary-only lists, absent roots, native order, unrelated
recipes and empty lists. Before the fix, 30 subcases failed; afterward all seven
methods PASS. The existing 68-test suite remains applicable; current aggregate
results and exact commands are recorded in TESTING.md.

[UNKNOWN / RUNTIME GATE] Actual construction-window rendering/filter behavior,
mouse/keyboard/controller use, building/payment/cancellation, and SP/dedicated
validation remain untested in PZ. This source and mock audit is not an in-game
visibility guarantee. G6 SP NOT TESTED; G7 dedicated and stable G8 BLOCKED.
