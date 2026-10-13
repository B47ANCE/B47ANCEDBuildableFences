# Material behavior audit before implementation

Date: 2026-10-02. [VERIFIED] Installed vanilla Build 42.21, identified by
Core's static GameVersion initialization in projectzomboid.jar. This is source
inspection; no runtime audio result is asserted.

Primary sources under installed `media/`: newtiledefinitions.tiles.txt,
tiledefinitions_noiseworks.patch.tiles.txt, lua/server/Items/BrokenFences.lua,
lua/server/BuildingObjects/ISBuildIsoEntity.lua and ISBuildUtil.lua,
scripts/generated/sounds/zombies/sounds_zombie_foley.txt. Decompiled vanilla
IsoThumpable.getThumpSound/getBreakSound/GetBreakFurnitureSound/getMeleeHitSurface
and BrokenFences.addBrokenTiles/destroyFence were also inspected.
Tile source hashes and complete properties are in evidence/vanilla_tiles.json.

## Verified material matrix

| B47 family | Material / vanilla reference | Tile thump | Map destruction / native constructed break | Open/close |
|---|---|---|---|---|
| Tall Wooden | Wood, fencing_01_8–12 and 72/73/75; Wood_Solid | ZombieThumpWood | ZombieThumpWoodCollapse via BrokenFences; native wood-wall entities explicitly use the same collapse sound | N/A |
| Wrought Iron | MetalBars, fencing_01_64–68; FenceTypeHigh MetalGate | ZombieThumpMetalPoleFence | Map BrokenFences defaults to BreakObject; native GetBreakFurnitureSound selects metal furniture break from FenceTypeHigh | N/A |
| Military | MetalWire, fencing_01_48–52; FenceTypeHigh Metal | **Absent** on exact tiles; closest equivalent wire fence 80–84 uses ZombieThumpChainlinkFence | Native GetBreakFurnitureSound selects metal furniture break; no vanilla breakable registration found for 48–52 | N/A |
| Security | MetalWire, fencing_01_80–84; FenceTypeHigh Metal | ZombieThumpChainlinkFence | Map BrokenFences defaults to BreakObject; native GetBreakFurnitureSound selects metal furniture break | N/A |
| Razor Security | MetalWire, fencing_01_88–92; FenceTypeHigh Metal | ZombieThumpChainlinkFence | Map BrokenFences defaults to BreakObject; native GetBreakFurnitureSound selects metal furniture break | N/A |
| Future wooden gates (reference only) | fixtures_doors_fences_01_12–15, Material Door / Wood, DoorSound WoodGate | No tile ThumpSound; constructed IsoThumpable retains generic fallback unless explicitly assigned | Vanilla gate entity BreakDoor | WoodGate prefix + Open/Close, separate from thumping |
| Future metal gates (reference only) | Vanilla MetalPoleFenceGate entity uses fixtures_doors_fences_01_24–27, DoorSound MetalGate | No tile ThumpSound; native door-prefix fallback returns ZombieThumpChainlinkFence | Vanilla entity BreakDoor | MetalGate prefix + Open/Close, separate from thumping |

These are actual source values or explicit absence, not placeholders. The
native constructed break uses the engine's verified GetBreakFurnitureSound
method rather than a guessed event. No gate is added in this development slice.
The vanilla entity's name MetalPoleFenceGate does not establish a MetalPoleGate
sound prefix: its selected 24–27 tiles actually specify MetalGate. Separately,
20–23 specify MetalPoleGate and native prefix fallback selects
ZombieThumpMetalPoleFence; 16–19 explicitly specify ZombieThumpChainlinkFence.
Do not infer configuration from entity names or nearby patch entries.
Standalone posts become nonblocking IsoObjects through the preserved path;
they are not ordinary thumpable sections after conversion. Posts 13, 53, 69,
74 lack the family thump properties. Do not make them blocking/thumpable just
to satisfy an audio scenario that does not apply to their runtime type.

No explicit HitSound exists on the audited fence tiles. Native melee impact
selects ParameterMeleeHitSurface from tile ThumpSound for nondoor objects;
otherwise it uses DoorSound prefix, whose fallback is WoodDoor. In 42.21 the
switch covers ZombieThumpChainlinkFence and ZombieThumpWood but does not list
ZombieThumpMetalPoleFence. Thus a per-object thump fallback fixes zombie audio
without proving weapon-impact surface correctness. Military and iron melee
impact correctness remains [UNKNOWN]/[RUNTIME GATE]; no shared vanilla tile
mutation or native interception is introduced on this evidence alone.

## Root cause and scope

[VERIFIED] IsoThumpable.getThumpSound first reads sprite ThumpSound. If absent,
recognized door prefixes have special cases; otherwise it returns stored
thumpSound, initialized to ZombieThumpGeneric. B47's baseline never sets family
thump fallback. Vanilla ISBuildUtil only sets ZombieThumpMetal if modData
contains use:Base.BlowTorch; DontRecordInput explicitly avoids recording inputs.
[INFERRED] This is a credible cause of inappropriate military thumps, not proof
that all reported door-like sounds have the same cause. Exact sound-patched
Security and Razor sprites should already inherit chainlink audio when the
patch is loaded. Their reported runtime discrepancy needs comparison against
loaded sprite properties and native equivalents.

Planned original B47 fix: authority-only SpriteConfig OnCreate callback sets
per-object fallback wood/iron/chainlink sounds by exact entity/sprite pair;
wood uses vanilla wood collapse; metal uses the native material break resolver.
Sprite properties still take precedence. This occurs before native complete
object transmission and persists via IsoThumpable fields. No new audio network
protocol, DoorSound override, global sound replacement or animation asset.
Existing saved objects are not rewritten; testing must build fresh candidate
pieces and separately identify any old-save remediation need.

## BrokenFences log issue

[VERIFIED] vanilla lua/server/Items/BrokenFences.lua registers intact and damaged
sprite variants independently of B47 construction. BrokenFences.addBrokenTiles
logs missing ThumpSound whenever a registered sprite lacks the property; it
does not require a B47 instance. Registration is global, so the message cannot
be attributed to B47 construction merely from its appearance in a modpack log.
It checks the sprite, not the object's stored fallback; an OnCreate fallback
will not silence that registration message. No registration or sprite sound
mutation is added by this implementation.

The exact sound patch supplies wood/iron/security/razor properties but not
military 48–52. [UNKNOWN] Server patch load order, exact installed server build,
other mods' sprite modifications/registrations and a vanilla-only dedicated
reproduction have not been supplied. The available Windows client console
includes B47 loading and optional AnimSets/actiongroups scan exceptions;
it supplies no current candidate audio validation. Dedicated log excerpts in
the handoff are user-reported history, not a full paired reproduction.
No optional animation directories or dummy definitions are added.

## Badlands and Privacy Gate

See BADLANDS_FENCE_REFERENCE_AUDIT.md. [VERIFIED] inspected Badlands private fence
and gate tile definitions contain no ThumpSound assignment and fence-specific
Lua does not set sounds. They are not vanilla sound-patch names, so inheritance
of those vanilla patches cannot be assumed. KNX_GatePrivacy is wooden, sets
BreakDoor, lacks explicit DoorSound/ThumpSound on its four private tiles, and
uses native open/close mechanics. Its exact heard sound remains untested.
It is not evidence for a metal gate's correct sound configuration.

## Runtime gate

For every family, compare fresh construction against matching vanilla map
objects: zombie thump, player weapon impact, repeated damage, destruction,
client and dedicated audio. Check both clients, reconnect/restart, and logs.
For future gates separately test closed thumping, opening/closing, open state,
damage and destruction. Offline source inspection cannot pass these gates.
