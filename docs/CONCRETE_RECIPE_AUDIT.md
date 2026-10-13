# Concrete item and recipe audit

Project Version: 1.1.0-dev.6

[VERIFIED] Installed Build 42.21 has no item named Base.Concrete in its script
inventory. Mixed concrete is Base.BucketConcreteFull or
Base.BucketCarvedConcreteFull in scripts/generated/items/drainable.txt. Both
are base:drainable, UseDelta 0.25, UseWhileEquipped false and replace on depletion
with Base.Bucket / Base.BucketCarved. Four uses per full container. ConcretePowder
is a normal unmixed input; MakeBucketOfConcrete in generated/recipes/recipes_buckets.txt
uses powder plus water and a bucket to produce the full mixed-concrete item.
Do not accept clay cement just because it shares the broad concrete tag.

[VERIFIED] InputScript.isUsesPartialItem detects drainable inputs unless
ItemCount, keep or destroy changes semantics. CraftRecipeData.getInputCraftCount
uses getCurrentUses for normal inputs; processDestroyAndUsedItems passes the
remaining requested count to ItemUser.UseItem and synchronizes server item stats.
The original vanilla syntax therefore supports:

```
item 1 [Base.BucketConcreteFull;Base.BucketCarvedConcreteFull] flags[DontRecordInput],
item 2 [Base.BucketConcreteFull;Base.BucketCarvedConcreteFull] flags[DontRecordInput],
```

Only one line is used per recipe. Neither ItemCount nor mode:destroy is set.
DontRecordInput keeps concrete out of recorded dismantling inputs, matching the
existing torch/rod consumed-use pattern. [INFERRED] A fresh full bucket retains
three uses after a straight piece or two after a corner; native tally supports
multiple partial containers. [RUNTIME GATE] Actual inventory selection,
split-container use, depletion replacement, cancellation and server/client
inventory must be tested. Offline syntax checks do not prove observed use.

All six Security/Razor recipes require Welding 4 (`MetalWelding:4`) after the
skill-only rebalance. Concrete and all other material inputs remain unchanged.

| Piece | Before | After |
|---|---|---|
| Security Plain | 5 Blowtorch Uses, 5 Pipes, 2 Scrap Metal, 5 Rod Uses | 5 Blowtorch Uses, 5 Pipes, 1 Concrete Use, 5 Rod Uses |
| Security Post-Ended | 5 Blowtorch Uses, 5 Pipes, 2 Scrap Metal, 5 Rod Uses | 5 Blowtorch Uses, 5 Pipes, 1 Concrete Use, 5 Rod Uses |
| Security Corner | 7 Blowtorch Uses, 7 Pipes, 3 Scrap Metal, 7 Rod Uses | 7 Blowtorch Uses, 7 Pipes, 2 Concrete Uses, 7 Rod Uses |
| Razor Plain | Security Plain + 2 Barbed Wire | New Security Plain + 2 Barbed Wire |
| Razor Post-Ended | Security Post-Ended + 2 Barbed Wire | New Security Post-Ended + 2 Barbed Wire |
| Razor Corner | Security Corner + 3 Barbed Wire | New Security Corner + 3 Barbed Wire |

Mixed-concrete identity differs from the handoff's literal Base.Concrete; using
that nonexistent name would make recipes invalid. This implementation preserves
the requested mixed-concrete intent and verified partial-use semantics.
