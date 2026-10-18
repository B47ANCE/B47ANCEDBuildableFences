B47ANCE'd Fences & Gates — v1.1.0-dev.16

Standalone Project Zomboid Build 42 fence-building mod.

Includes 21 buildable pieces across tall wooden, military, security, razor-wire, and wrought-iron fence sets using vanilla Project Zomboid fence sprites.

Collision fixes
- Straight rotatable fence sections use corrected W/N sprite-axis mapping so their WallW/WallN direction agrees with the placed object orientation. This removes the invisible perpendicular wall produced by the original mappings.
- Standalone wooden and military posts are converted to non-blocking objects after placement, removing the invisible wall that otherwise extends from the post.

Known issue
Standalone posts currently have a rendering/depth-order issue: when the player occupies the same tile as a post, the post sprite may render over the player model. This is visual only; the post no longer creates the unwanted invisible movement wall.

Wooden cutaway parity with vanilla map-placed fences remains unverified. No speculative transparency or collision change is applied.

Multiplayer implementation (preserved from the historical v1.0.37 baseline)
In MP, clients do not directly replace world objects. They request the standalone-post conversion and the server validates and performs it authoritatively, then replicates the replacement. Dedicated-server runtime validation remains the final release gate.

Development expansion
- Wrought Iron: Plain Section, Post-Ended Section, Corner, Standalone Post.
- Security/Razor plain and post-ended recipes: 1 Concrete Use, 5 Blowtorch Uses, 5 Metal Pipes, 5 Welding Rods; Razor also uses 2 Barbed Wire.
- Security/Razor corners: 2 Concrete Uses, 7 Blowtorch Uses, 7 Metal Pipes, 7 Welding Rods; Razor also uses 3 Barbed Wire.
- Mixed concrete accepts vanilla metal or carved concrete buckets. A full bucket has four uses; the whole container is not consumed for one use.
- Material-specific construction sound initialization; runtime audio still requires comparison.
- Sandbox setting: Fence construction health (%), 10-500, default 100. Server authoritative, new sections/corners only. Existing fences and converted standalone posts remain unchanged.
- Complete English fallback translation coverage in 29 vanilla language folders.

Construction skill requirements (all variants in each family)
- Tall Wooden Straight Top: Carpentry 4 (Fence, Corner, Post).
- Tall Wooden Sloped Top: Carpentry 7 (Post-Ended, Continuous, Corner, Post).
- Security: Welding 4 (Plain, Post-Ended, Corner).
- Razor-Wire Security: Welding 4 (Plain, Post-Ended, Corner).
- Military: Welding 7 (Plain, Post-Ended, Corner, Post).
- Wrought Iron: Welding 7, unchanged (Plain, Post-Ended, Corner, Post).
Skill rebalance preserves materials, XP rewards, health fields, sprites and runtime logic.

Status: development source only. Wooden cutaway work is blocked pending paired runtime evidence. SP, dedicated two-client collision/audio/concrete tests, reconnect and restart are required. No release-ready claim, deployment or packaging.

Current development overlay adds missing intact vanilla fence and gate recipes only. Existing vanilla recipes are excluded. Native SP and dedicated MP validation is pending.
