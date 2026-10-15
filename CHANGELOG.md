# Changelog

## [1.1.0-dev.14]

- Audit-only follow-up: compare all 30 additions against all installed construction scripts, Lua routes and pixel-identical art aliases. No duplicate recipe art found; add repeatable checker and regressions. Runtime payload and recipes unchanged.

Compatible PATCH correction to the unpublished expansion: restrict new content
to 30 fence/gate parts in 13 groups. Remove architectural/stair railings,
balustrades, decorative loose wire, gabion baskets and crowd-control barriers,
including generated definitions, menu membership and stale labels. Add explicit
out-of-scope inventory accounting and regression guards. Preserve the Fences &
Gates display name, all original recipes, server authority and native gates.
No package, deploy or upload; no new native runtime evidence.

## [1.1.0-dev.13]

Compatible PATCH metadata iteration: rename the displayed project to B47ANCE'd
Fences & Gates in mod.info, the sandbox page, current README and future Workshop
metadata. Workshop preparation derives the title from the reviewed mod.info
name, including it in the upload VDF. Technical Mod ID, Workshop ID, repository,
existing art, recipes, save identity and gameplay remain unchanged. No upload.

## [1.1.0-dev.12]

Compatible MINOR-scope expansion within the unreleased 1.1.0 series: add 151
construction entries across 28 groups for intact vanilla fence, railing and gate
art that has no vanilla recipe. Existing vanilla recipes, prior mod recipes,
server construction and automatic junction behavior are retained. Each part has
its own paid recipe. Decorative railing fragments retain native geometry; four
tile definitions with missing textures are explicitly blocked. Runtime untested.

## [1.1.0-dev.11]
- Add user-supplied fallback icon/thumbnail; preserve manually supplied artwork. Asset-only iteration; gameplay unchanged.
- Offline branding/version checks only; earlier validation remains historical at 1.1.0-dev.10. No new SP/dedicated MP evidence.

## [1.1.0-dev.10]

Compatible MINOR-scope expansion within the 1.1.0 prerelease series: extend
server-owned vanilla junction posts to straight-top wood, sloped-top wood and
military fences using their own vanilla post sprites. Preserve all paid recipes,
costs, health and iron configuration. Separate server sandbox toggles default on.
Security and razor-wire stay unchanged by user choice: no matching standalone
vanilla post exists in their sets. SP and dedicated MP remain NOT TESTED.

## [1.1.0-dev.9]

Compatible MINOR-scope addition in the 1.1.0 prerelease series: server-owned,
vanilla-style wrought-iron junction posts included in the unchanged section
costs. Exact family/orientation checks and duplicate prevention; server sandbox
option defaults on. Existing objects/recipes remain unchanged. Runtime untested.


## [1.1.0-dev.8]

Compatible PATCH-scope Workshop preparation: remove runtime diagnostic logging
and test-only tooltip export, retain offline regressions, and add version-driven
package preparation with an explicit shipped-file manifest. No balance, save,
recipe or authority change. G6/G7 NOT TESTED; stable G8 BLOCKED.


## [1.1.0-dev.7]

Compatible MINOR-scope UI expansion within the existing 1.1.0 prerelease series:
consolidate all six fence families while retaining original part entities, costs,
skills and native server construction. Gate remains separate. Runtime untested.


## [1.1.0-dev.6]

Removed developer test-kit Lua and translations from the active overlay.
Compatible PATCH-scope cleanup within the existing 1.1.0 development series.
Construction, recipes, authority and selector/gate behavior unchanged.
G6/G7 NOT TESTED; stable G8 BLOCKED.


## [1.1.0-dev.6]

Removed the optional developer test kit and its translations from the active overlay.
Compatible PATCH-scope cleanup within the existing 1.1.0 development series;
fence construction, authority, recipes and selector/gate behavior unchanged.
Native SP and dedicated MP remain NOT TESTED; stable G8 BLOCKED.


## [1.1.0-dev.5]

Explicitly authorized untested Workshop prerelease for dedicated-server testing:
production source plus corrected iron selector/gate overlay and developer kit.
Native SP/MP/save gates remain untested; no stable promotion or readiness claim.

Compatible startup fix for the isolated selector: defer client hooks until
OnGameStart and load cursor hooks in the native server Lua phase. Audit
downloaded 1.0.37 save identities with an explicit unchanged-definition map;
no world-object replacement or save edits. Native migration gates untested.

## [1.1.0-dev.4]

Corrected isolated Wrought Iron variant-selection prototype: Q/E reaches all
original pieces/faces using their own recipes. Automatic topology archived
and removed from active overlay. Public source gameplay remains unchanged.
Native collision/save/dedicated gates remain untested.

## [1.1.0-dev.3]

Developer-only prototype runtime kit command b47fencetestkit: loaded-recipe
discovery, tools to inventory, bounded ordinary material drops at player feet,
authority admin checks. Test infrastructure stays isolated; no stable bump.

Isolated Wrought Iron cohesive construction prototype; production recipe/gameplay
files retain dev.2 behavior. One fence entry, Q/E intent, native gate, authority-only
topology and decorative posts. Offline evidence only; G7/G8 remain blocked.

## [1.1.0-dev.2]

Skill-only compatible rebalance: Straight Top Carpentry 7 to 4; Security
and Razor Welding 7 to 4. Sloped Top, Military and Wrought Iron remain at 7.
All materials, XP rewards, health fields, sprites, cutaway, sound and
networking behavior are preserved. No deployment or runtime claim.

## [1.1.0-dev.1]

Compatible minor development expansion from the downloaded baseline.
Adds four wrought-iron variants, concrete-use Security/Razor recipes and
material sound initialization. Wooden cutaway correction remains blocked
pending a proven runtime root cause. No release artifacts or deployment.

## [1.0.37]

Downloaded baseline recovery. Preserves the existing straight collision axes
and server-validated nonblocking standalone-post conversion. This record does
not add or reinterpret historical runtime evidence.
