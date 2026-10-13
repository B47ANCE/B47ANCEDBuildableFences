# Cohesive fence developer runtime test kit

Project Version: 1.1.0-dev.5

DEV / RUNTIME TESTING ONLY. Not a production feature. No launch, deployment,
package or Workshop publication performed. The utility was added within dev.3
without a stable bump; dev.4 retains it while correcting the piece-selection
prototype. No public compatibility/balance change. Production gameplay stays
unchanged; only current version headers/metadata advance.

## Command and exact Lua files

Type `/b47fencetestkit` in native chat, with no arguments. The prototype's
ISChat.onCommandEntered adapter catches only that exact command and submits
empty intent via sendClientCommand; other commands use the original handler.
SP without chat: right-click the world and choose `b47fencetestkit (DEV /
RUNTIME TESTING ONLY)`. Developer Lua console fallback:
`B47FenceTestKit.request(getSpecificPlayer(0))`.

Added under prototypes/cohesive/42:

- media/lua/shared/B47_FenceTestKitPlan.lua â€” authoritative recipe discovery/budget.
- media/lua/server/B47_FenceTestKitServer.lua â€” authorization, preflight and spawn.
- media/lua/client/B47_FenceTestKitClient.lua â€” slash/menu adapter and local feedback.

Changed support files: scripts/record_cohesive_evidence.py; 29 overlay IG_UI.json
fallback files; tests/test_fence_testkit.py; overlay README; changelog and this
report; version inventory and current hashes/validation records. Previous
29-test records are preserved in evidence/history/dev.3-before-testkit.

## Exact current kit

Loaded recipes can change this result; this table is the offline-derived
current dev.4 recipe result (unchanged quantities from dev.3), not a separately
maintained spawning list.

| Destination | Exact ID | Full item instances |
|---|---|---:|
| Inventory | Base.Hammer | 1 |
| Inventory | Base.WeldingMask | 1 |
| Inventory | Base.BlowTorch | 1 |
| Player current square | Base.Plank | 240 |
| Player current square | Base.Nails | 288 |
| Player current square | Base.MetalPipe | 792 |
| Player current square | Base.ScrapMetal | 192 |
| Player current square | Base.BarbedWire | 72 |
| Player current square | Base.BucketCarvedConcreteFull | 24 |
| Player current square | Base.WeldingRods | 40 |
| Player current square | Base.BlowTorch | 79 |
| Player current square | Base.Hinge | 48 |
| Player current square | Base.Doorknob | 24 |

Ground total: 1,799 ordinary items. Tools remain three inventory items; spare
full BlowTorches are consumed fuel capacity on the ground. Pick up a spare
after depletion; no extra spawning/refill recipe is required. This avoids
putting 80 charged torches in inventory. No custom containers or test objects.

## Discovery and quantity semantics

Server/SP reads SpriteConfigManager.GetObjectInfoList directly, not the
prototype's filtered player-facing list. It visits every B47_ entity with a
CraftRecipe, including all 21 existing definitions and the prototype gate.
For each input it resolves getPossibleInputItems (including hammer tags),
chooses one allowed item deterministically, and reads getAmount(fullType),
conservatively retaining declared getAmount() for resolved tag alternatives,
isKeep and isItemCount. Base.Hammer is preferred within its resolved tag.
Other alternatives sort by exact ID: BucketCarvedConcreteFull sorts before
BucketConcreteFull, so carved buckets are supplied, not both alternatives
double-counted. Both are valid current recipe inputs; Base.Concrete is never used.

For each family, the largest amount of each consumed input across its variants
is budgeted for 24 constructions, then family budgets are summed. Seven budgets:
Sloped Wood, Straight Wood, Military, Security, Razor Security, Wrought Iron,
and Wrought Iron Gate. Manual/prototype iron share the same family budget;
their identical plain recipe is not accidentally counted twice. The 24 iron
builds can be split between those A/B cases, or rerun the command for another
fresh kit. This covers arbitrary mixes of the family's variants at their
highest costs, rather than guessing a material list.

Fresh drainable sample getCurrentUses determines full-item capacity:
BlowTorch10, WeldingRods20, either concrete bucket4 (native UseDelta .1/.05/.25).
792 torch uses -> 80 full torches (1 inventory +79 ground);792 welding-rod uses
->40 full packs;96 concrete uses ->24 full buckets. No artificial extra charges.
Materials that are not drainable use ordinary individual item instances.
Native count/drop behavior is retained, including Nails' script count=5;
no fake InventoryItem count or compressed container is introduced. The inspected
AddWorldInventoryItem count overload loops individual world objects, so the
kit uses ordinary native drops and drainable-pack capacities rather than
inventing world-stack behavior that recipe consumption might not support.

Keep-mode reusable inputs go to inventory. BlowTorch is charged/consumed and
classified from its native Tool display category: one active tool goes to
inventory, reserves to ground. WeldingMask is an explicit native PPE supplement:
current fence recipes and BuildPoleFence timed action do not require one.
The timed-action CraftingWeldingTorch prop is animation presentation, not a
required inventory item. No skills, recipes, health, sandbox, fence logic,
item definitions or Creative Mode setting are changed by the command.

## Authorization and synchronization

SP: allowed only in the explicitly installed developer overlay, no debug or
Creative Mode needed. MP: server checks the authenticated requesting player's
native role name equals admin (case-insensitive) AND native Capability.AddItem.
Moderators/ordinary players or admins without the capability are denied before
discovery/item creation. Local client role claims never authorize spawning.
Client cannot call plan/spawn to commit world state. Payload IDs/counts/position/
target-player/role are ignored; only authority recipe metadata defines the kit.
Server obtains the player's current square at execution, not client coordinates.

Inventory uses AddItem plus sendAddItemToContainer, as native server item grants
do. Current-square AddWorldInventoryItem(InventoryItem,.5,.5,0) uses its normal
server complete-object replication. No client independently creates items.
Confirmation/denial is sent only to the requesting player and displayed locally.
Repeat execution creates a fresh kit and never deletes earlier items.

Full discovery/item creation preflight happens before inventory/world writes;
missing/unresolved inputs or resource/budget violations produce no kit. Bounds
(24 constructions,40 recipes,10 families,100 input amount,2500 world objects)
are test-fixture limits, not production gameplay options. Unsupported future
resources fail visibly instead of silently creating an incomplete kit. A failure
during native world insertion could leave a partial kit; runtime evidence is
required and no previous items are deleted as a workaround.

## Evidence and remaining runtime checks

[VERIFIED, source] native 42.21 Chat/ISChat.lua onCommandEntered;
ClientCommands.lua Capability.AddItem authorization and inventory grants;
InputScript.getAmount overloads and native HaloTextHelper.addText(IsoPlayer,String);
IsoGridSquare AddWorldInventoryItem creation/transmission; current entity
recipes and drainable definitions; BuildPoleFence timed-action props.

[TESTED, Windows offline Python/Lupa] seven added tests execute actual command
planning/spawning code against fake native APIs/current recipe inputs: exact
quantities/22 recipes, admin repeat, ordinary/moderator denial with zero items,
capability denial, client refusal, ignored forged payloads, SP allowance,
preflight failure atomicity, recipe-cost change propagation and exact slash
dispatch. Full regression and version consistency commands are recorded in
evidence/offline-tests.txt and evidence/version-check.txt.

Run from the workspace root:

```powershell
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s B47ANCEDBuildableFences\tests -p test_fence_testkit.py -v
& 'C:\Users\willi\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' B47ANCEDBuildableFences\scripts\validate.py
```

[RUNTIME GATE] Native SP/admin/dedicated spawning and ordinary-player denial
NOT TESTED. Native construction completeness NOT TESTED. Offline quantities
cover every current recipe, but a real runtime PASS still requires:

1. Invoke in SP and dedicated admin; confirm three inventory tools and ground
   materials on executing player's current square, visible to second client.
2. Try ordinary MP player and moderator, plus forged payload: clear denial,
   zero inventory/world changes. Repeat as admin: fresh kit, prior kit retained.
3. Without Creative Mode, use a character meeting Woodwork7/MetalWelding7;
   build Straight/Sloped wood, Security, Razor, Military, manual/prototype iron
   and prototype gate. This utility does not change skill thresholds.
4. Perform the corrected dev.4 piece/face matrix and manual/prototype comparison.
   Verify per-piece costs, intentional corner/post selection and no neighbor
   mutation. Pick up a spare
   torch when depleted. Any missing input/tool means the runtime kit fails.
5. Verify ground-material discovery range, mask/equip behavior, item charges,
   ordinary item persistence and dedicated server/container sync.

G6 native NOT TESTED; G7 BLOCKED / NOT TESTED; G8 BLOCKED. No runtime readiness
claim. Promotion MUST exclude all three B47_FenceTestKit*.lua files and the four
IGUI_B47_TestKit* keys; do not copy this utility into public production by default.

The supplied runtime log fails during shared cursor loading before normal
prototype startup. Dev.5 fixes phase ordering in source; native menu retest
is pending. The local test copy is now cleanly deployed dev.5; fully restart
the game before attempting this menu/command. See DEPLOYMENT_DEV5.md.
