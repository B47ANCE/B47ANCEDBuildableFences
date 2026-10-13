# Wrought-iron sprite audit

Project Version: 1.1.0-dev.6

[VERIFIED] Vanilla Build 42.21 media/newtiledefinitions.tiles.txt and
tiledefinitions_noiseworks.patch.tiles.txt. Complete property records and SHA256
source hashes: evidence/vanilla_tiles.json. Texture source: Tiles2x.pack,
extracted using the independently inspected native TexturePackDevice format.
Visual role was checked against extracted art; wall axes come from metadata.

| Role | Face | Sprite | Wall metadata | Climb / collision edge metadata | Sound |
|---|---|---|---|---|---|
| Plain | W | fencing_01_66 | WallWTrans, wall | TallHoppableW | ZombieThumpMetalPoleFence |
| Plain | N | fencing_01_65 | WallNTrans, wall | TallHoppableN | ZombieThumpMetalPoleFence |
| Post-ended | W | fencing_01_67 | WallWTrans, wall | TallHoppableW | ZombieThumpMetalPoleFence |
| Post-ended | N | fencing_01_64 | WallNTrans, wall | TallHoppableN | ZombieThumpMetalPoleFence |
| Corner | S | fencing_01_68 | WallNWTrans, wall; CornerNorthWall=64, CornerWestWall=67 | TallHoppableN and W | ZombieThumpMetalPoleFence |
| Standalone post | S | fencing_01_69 | No wall flag / no WallSE | No edge or hoppable flags | No tile ThumpSound |

All six use Material MetalBars, CanScrap, CanAttachAnimal, HitByCar and
SpearOnlyAttackThrough. BurntTile maps sequentially to fencing_burnt_01_56–61;
SnowTile maps to object_snow_overlay_01_224–229. CloseSneakBonus=250 on sections
and corner, absent on post. Sections/corner have FenceTypeHigh=MetalGate.
No explicit BreakSound or HitSound is declared on these tiles. Runtime object
break behavior is the native material resolver documented in the sound audit.

[VERIFIED] tileGeometry.txt marks each iron tile Translucent=true. There is no
explicit added cutaway flag in the text definitions; native wall-transparency
metadata and renderer provide the presentation path. We do not change tile
geometry, cut flags, sprite properties, or their global tile type.
Wall metadata defines the edge model; collision behavior after construction is
[RUNTIME GATE], not inferred into a PASS. Standalone post enters the existing
nonblocking replacement path because native entity construction makes an
IsoThumpable even for its nonwall sprite. No replacement sequence is rewritten.

![Audited vanilla iron art](evidence/wrought_sprites.png)

Choosing plain sections inside a run and post-ended sections at exposed ends
avoids intentional duplicated end posts. Corners and standalone posts remain
manual choices. Automatic adjacent-variant switching is not implemented.
