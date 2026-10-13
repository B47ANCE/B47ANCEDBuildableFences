-- B47ANCE'd Buildable Fences v1.1.0-dev.3
-- DEV / RUNTIME TESTING ONLY. Exclude B47_FenceTestKit* when promoting overlay.
B47FenceTestKit = B47FenceTestKit or {}
local K = B47FenceTestKit
K.constructions = 24 -- bounded test fixture, not a gameplay balance option
function K.family(name)
    if name == "B47_WroughtIronGate" then return "WroughtIronGate" end
    if name:find("^B47_TallWoodenFence_") then
        return name:find("StraightTop",1,true) and "WoodStraight" or "WoodSloped"
    end
    return name:match("^B47_(.-Fence)_") or name
end
local function choose(input)
    local items = input:getPossibleInputItems()
    local names = {}
    for i=0,items:size()-1 do names[#names+1] = items:get(i):getFullName() end
    table.sort(names)
    -- Prefer the standard hammer from the resolved base:hammer tag, if allowed.
    for _,name in ipairs(names) do if name == "Base.Hammer" then return name end end
    return names[1] -- deterministic allowed alternative, not both charged twice
end
function K.plan(infos)
    if isClient() then error("authority only") end
    local families,kept,consumedTools,recipes = {},{},{},0
    for i=0,infos:size()-1 do
        local info = infos:get(i)
        local name = info:getName()
        if name:find("^B47_") and info:getRecipe() then
            recipes = recipes+1
            if recipes>40 then error("recipe bound") end
            local family = K.family(name)
            families[family] = families[family] or {}
            local perRecipe = {}
            local inputs = info:getRecipe():getCraftRecipe():getInputs()
            for n=0,inputs:size()-1 do
                local input = inputs:get(n)
                if input:getResourceType() ~= ResourceType.Item then error("unsupported resource") end
                local itemType = choose(input)
                if not itemType then error("unresolved recipe input") end
                -- A resolved tag alternative may not be in InputScript.items;
                -- that overload returns 1. Preserve the declared tag budget too.
                local amount = math.max(input:getAmount(itemType),input:getAmount())
                if not amount or amount~=amount or amount<=0 or amount>100 then error("input bound") end
                local sample = instanceItem(itemType)
                if not sample then error("missing item " .. itemType) end
                if input:isKeep() then
                    kept[itemType] = math.max(kept[itemType] or 0,math.ceil(amount))
                else
                    local capacity = 1
                    if not input:isItemCount() and instanceof(sample,"DrainableComboItem") then
                        capacity = sample:getCurrentUses()
                    end
                    if capacity<1 then error("empty sample " .. itemType) end
                    local entry = perRecipe[itemType] or {amount=0,capacity=capacity}
                    entry.amount = entry.amount+amount
                    perRecipe[itemType] = entry
                    -- Charged tool: one active tool in inventory, spare full units
                    -- on ground as consumed fuel capacity, never bulk inventory.
                    if sample:getScriptItem():getDisplayCategory() == "Tool" then consumedTools[itemType] = true end
                end
            end
            for itemType,entry in pairs(perRecipe) do
                local current = families[family][itemType]
                if not current or entry.amount>current.amount then families[family][itemType] = entry end
            end
        end
    end
    if recipes==0 then error("no B47 recipes") end
    local uses,capacities,familyCount = {},{},0
    for _,inputs in pairs(families) do
        familyCount=familyCount+1
        for itemType,e in pairs(inputs) do
            uses[itemType]=(uses[itemType] or 0)+e.amount*K.constructions
            capacities[itemType]=e.capacity
        end
    end
    if familyCount>10 then error("family bound") end
    local plan={inventory=kept,ground={},uses=uses,recipes=recipes,families=familyCount}
    for itemType,amount in pairs(uses) do
        local count=math.ceil(amount/capacities[itemType])
        if consumedTools[itemType] then
            plan.inventory[itemType]=(plan.inventory[itemType] or 0)+1
            count=count-1
        end
        if count>0 then plan.ground[itemType]=count end
    end
    -- PPE supplement: current B47 inputs/BuildPoleFence do not require a mask.
    -- Include one verified native mask for the welding test session anyway.
    plan.inventory["Base.WeldingMask"] = math.max(plan.inventory["Base.WeldingMask"] or 0,1)
    local total=0
    for _,count in pairs(plan.ground) do total=total+count end
    if total>2500 then error("world item bound") end
    plan.worldCount=total
    return plan
end
