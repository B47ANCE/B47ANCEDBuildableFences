# Architecture

Project Version: 1.1.0-dev.14

See FAMILY_SELECTORS.md for the current six-family design, native authority,
recipe preservation, configuration decision and runtime gates. The overlay is
composed with production src/ as in the existing dev.6 test candidate.

All 21 fence definitions and their original costs/skills persist. One menu
entry per family cycles each real part/face; iron gate remains separate.
No shared state, recipe, collision, migration or post-conversion rewrite.

Next: native SP and dedicated two-client validation. G7 BLOCKED / NOT TESTED;
G8 BLOCKED. Historical checkpoint reports retain their original versions.

---

## Historical dev.6 notes

The following is retained for provenance, not current instructions or dev.7
validation. Current family selection and test gates are described above and
in docs/FAMILY_SELECTORS.md.

# Architecture

Historical Project Version: 1.1.0-dev.6

The active overlay contains a corrected variant-selection Wrought Iron source overlay outside
src/. The production architecture below retains dev.2 behavior. Overlay state
ownership, native orientation request/replication, marker persistence and
runtime gates are documented in COHESIVE_PROTOTYPE_REPORT.md. Archived dev.3
topology is not loaded. Q/E selects actual entity/recipe/face, not neighbors. It adds no
client authority and is not enabled or generalized in this candidate.

## Authority and persistence

[VERIFIED] Native ISBuildAction.start uses createBuildAction and clients wait
for accepted/rejected action state. Its perform method returns on clients;
construction occurs on server/SP through ISBuildIsoEntity.create. The native
builder creates the IsoThumpable, assigns entity components/health, adds it to
the square, calls SpriteConfig OnCreate, recalculates neighbors and transmits
the complete item. CraftRecipeData processes partial uses through ItemUser and
sends item stats from the server. This is the reused authority/sync path.
No new build command or client-owned inventory consumption is introduced.

[VERIFIED] B47Fence.OnCreate is in server Lua and refuses isClient(). It checks
actual IsoThumpable type and an exact name/sprite pair before setting per-object
sound fields and interpreting the server sandbox value. Returning nil preserves
the native one-object transmission path. IsoThumpable save/load includes health,
thumpSound and breakSound; settings are evaluated at construction, not on load.
No global sprite property/type, north flag, block-all flag or object replacement
is touched by this callback. Default health causes no health writes.

[VERIFIED] Standalone-post handling is the exact recovered baseline sequence,
with only iron name/sprite added to each allowlist. Clients detect nearby
eligible IsoThumpables, send intent, never remove objects in MP. Server checks
sender, coordinates, same Z/proximity, actual square/class/name/sprite, removes
the object, creates/adds an IsoObject and transmits it. Repeat requests see a
non-IsoThumpable and cannot duplicate conversion. Single-player retains the
same local sequence. No post health/material inventory is stored separately.

Baseline caveats retained: client request cache has no retry until reload;
server name and sprite allowlists are independent sets, not exact pairs;
replacement does not transfer custom entity/name/modData state. This development
slice does not rewrite the user-proven conversion. [RUNTIME GATE] Dedicated
save/restart/late join, interrupted conversion and two-client collision must
prove continued correctness. Source inspection cannot certify those outcomes.

## Configuration candidates

| Candidate | Decision and rationale |
|---|---|
| Fence durability | One server sandbox ConstructionHealthPercent, integer 10Ã¢â‚¬â€œ500, step 1, default 100; scales newly constructed section/corner health |
| Recipe materials, uses, skill and time | Exact requested recipe contract and preserved B47 baseline; no per-input micro-settings. Runtime script recipes are shared server content |
| Native construction bonus | Existing vanilla ConstructionBonusPoints is still interpreted by the native builder; B47 multiplier applies afterward |
| Sprite axes, post conversion, material audio | Correctness invariants and material metadata, not gameplay alternatives; no disabling setting |
| Detection interval, scan/proximity limits, protocol names | Preserved technical safety/implementation limits; not gameplay balance settings |
| Wooden fade | Native local presentation; no arbitrary alpha or divergent gameplay state |

Option identifier is B47ANCEDBuildableFences.ConstructionHealthPercent, grouped
on B47's sandbox page with localized name/tooltip in all 29 folders. Authority
rejects nonnumbers/NaN/out-of-range values to 100, floors fractional input to the
integer format and never creates zero-health objects. Existing saves lacking
the setting get 100; existing objects are not resized. Converted posts are
excluded. Defaults preserve health behavior and schema compatibility.

## Compatibility and scope

The skill-only checkpoint changes three Straight Top requirements to Woodwork:4
and six Security/Razor requirements to MetalWelding:4. Sloped Top, Military and
Wrought Iron remain at 7. Recipe skill checks reuse the existing native build
authority; no custom client-only eligibility or sandbox override is added.
Exact progression tiers are the user-specified shared recipe contract, not
new configurable per-variant knobs. Current IDs, persistence, synchronization,
materials, XP and health configuration/code remain unchanged.

Mod ID and Workshop ID remain unchanged. No required dependencies, custom Java,
custom animations, gate entities, automatic neighbor rewriting or third-party
tile assets. Iron recipes/health reuse the user's own military family template
as the conservative initial B47 balance, not Badlands balance. New functionality
is a compatible MINOR expansion targeting stable 1.1.0 after gates, with current
development version recorded above. Wooden cutaway remains a separate blocker.

## Current dev.6 checkpoint

The developer test kit was removed from the active overlay: no kit menu, slash
command, spawn handler or kit translation keys ship. Earlier kit instructions
and native evidence describe historical dev.5 only. Construction, recipes,
selector/gate behavior and authority are retained. G6/G7 NOT TESTED; G8 BLOCKED.

## Current dev.6 checkpoint

The developer test kit is removed: no kit menu, command, spawn handler or kit
translation keys ship. Earlier kit instructions describe historical dev.5.
Fence construction and the selector/gate are unchanged. G6/G7 NOT TESTED; G8 BLOCKED.

## Wrought-iron corner connections (dev.9)

New matching perpendicular wrought-iron sections can add a native junction post
included in their existing section cost. Server sandbox WroughtIronCornerPosts
defaults on; disabling affects future generation only. No existing objects are
scanned or rewritten. See WROUGHT_IRON_CONNECTIONS.md for authority, configuration,
regressions and native limitations. Future packages use the inventory-declared
dist/corner-development-current directory; old dev.8 artifacts remain historical.

## Additional fence-family connections (dev.10)

Server-owned native junction posts now support military (fencing_01_53),
sloped-top wood (fencing_01_13) and straight-top wood (fencing_01_74), alongside
wrought iron. Only exact same-family perpendicular sections connect; the two
wood styles remain separate. Independent server options MilitaryCornerPosts,
SlopedWoodCornerPosts and StraightWoodCornerPosts default true. Missing old-save
values use true; malformed values disable generation. All paid recipes, costs,
skills, time, health and gates remain unchanged. Security and razor-wire remain
unchanged by explicit user choice: neither has a matching vanilla standalone
post. No retrofit, world scan, orphan cleanup or new client commands.
49 available offline tests pass; five baseline checks remain blocked.
G6 SP NOT TESTED; G7 dedicated BLOCKED / NOT TESTED; stable G8 BLOCKED.
See docs/WROUGHT_IRON_CONNECTIONS.md (WROUGHT_IRON_CONNECTIONS.md within docs)
for native authority and required runtime tests.

## Fence-and-gate expansion (dev.14)

The current catalog adds 30 paid fence and gate entries in 13 groups only where
no vanilla recipe supplies the artwork. Original mod families, costs and server
authority remain unchanged. Shared wooden gates serve both tall fence styles.
Architectural/stair railings, balustrades, loose decorative wire, gabion baskets
and crowd-control barriers are excluded. The earlier broad catalog was never
published or deployed. Four textureless fence definitions remain blocked.
See docs/VANILLA_CATALOG.md (VANILLA_CATALOG.md within docs) for the current
inventory, recipe costs, exclusions, source fingerprints and runtime gates.
