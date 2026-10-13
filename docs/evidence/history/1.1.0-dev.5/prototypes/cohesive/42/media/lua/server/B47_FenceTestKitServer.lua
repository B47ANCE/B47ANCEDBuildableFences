-- B47ANCE'd Buildable Fences v1.1.0-dev.5
-- DEV / RUNTIME TESTING ONLY. Never include in a production promotion.
require "B47_FenceTestKitPlan"
local K=B47FenceTestKit
function K.authorized(player)
    if isClient() or not player then return false end
    if not isServer() then return true end -- isolated single-player test overlay
    local role=player:getRole()
    return role and string.lower(role:getName()) == "admin"
        and role:hasCapability(Capability.AddItem) or false
end
local function reply(player,key,count)
    if isServer() then
        sendServerCommand(player,"B47FenceTestKit","result",{key=key,count=count or 0})
    elseif K.show then K.show(player,key,count or 0)
    else print(getText(key,count or 0)) end
end
function K.spawn(player)
    if isClient() then return false end
    if not K.authorized(player) then
        if player then reply(player,"IGUI_B47_TestKitDenied") end
        return false
    end
    local sq=player:getSquare()
    if not sq then reply(player,"IGUI_B47_TestKitFailed"); return false end
    -- Complete discovery and item creation before touching inventory/world.
    local ok,prepared=pcall(function()
        local plan=K.plan(SpriteConfigManager.GetObjectInfoList())
        local entries={inventory={},ground={},plan=plan}
        for _,destination in ipairs({"inventory","ground"}) do
            local names={}; for name in pairs(plan[destination]) do names[#names+1]=name end
            table.sort(names)
            for _,name in ipairs(names) do
                for i=1,plan[destination][name] do
                    local item=instanceItem(name)
                    if not item then error("missing item " .. name) end
                    entries[destination][#entries[destination]+1]=item
                end
            end
        end
        return entries
    end)
    if not ok then
        print("[B47 DEV test kit] preflight failed: " .. tostring(prepared))
        reply(player,"IGUI_B47_TestKitFailed"); return false
    end
    local inventory=player:getInventory()
    for _,item in ipairs(prepared.inventory) do
        inventory:AddItem(item)
        if isServer() then sendAddItemToContainer(inventory,item) end
    end
    for _,item in ipairs(prepared.ground) do
        -- Ordinary dropped item; native overload transmits on authority.
        sq:AddWorldInventoryItem(item,0.5,0.5,0)
    end
    print("[B47 DEV test kit] recipes=" .. prepared.plan.recipes ..
        " families=" .. prepared.plan.families .. " ground=" .. prepared.plan.worldCount)
    reply(player,"IGUI_B47_TestKitSpawned",prepared.plan.worldCount)
    return true
end
function K.onCommand(module,command,player,args)
    if module ~= "B47FenceTestKit" or command ~= "b47fencetestkit" then return end
    -- Ignore ALL request payload fields, including item IDs, counts/position/role.
    K.spawn(player)
end
Events.OnClientCommand.Add(K.onCommand)
