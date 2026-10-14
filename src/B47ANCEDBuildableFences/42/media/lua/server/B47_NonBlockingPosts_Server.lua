-- B47ANCE'd Buildable Fences v1.1.0-dev.7
-- Server-authoritative MP replacement for standalone B47 fence posts.
-- The server validates every request against the actual square/object before
-- changing world state. No client-supplied object is trusted.

if isClient() then return end

local POST_NAMES = {
    ["B47_TallWoodenFence_Post"] = true,
    ["B47_TallWoodenFence_StraightTopPost"] = true,
    ["B47_MilitaryFence_Post"] = true,
    ["B47_WroughtIronFence_Post"] = true,
}
local POST_SPRITES = {
    ["fencing_01_13"] = true,
    ["fencing_01_74"] = true,
    ["fencing_01_53"] = true,
    ["fencing_01_69"] = true,
}

local function spriteName(obj)
    local spr = obj and obj:getSprite()
    return spr and spr:getName() or nil
end

local function validPost(obj, expectedName, expectedSprite)
    if not obj or not instanceof(obj, "IsoThumpable") then return false end
    local name = obj:getName()
    local spr = spriteName(obj)
    if not POST_NAMES[name] or not POST_SPRITES[spr] then return false end
    if expectedName and expectedName ~= name then return false end
    if expectedSprite and expectedSprite ~= spr then return false end
    return true
end

local function replacePost(obj)
    local sq = obj:getSquare()
    local spr = spriteName(obj)
    if not sq or not spr then return false end

    -- Deliberately mirrors the v1.0.35 operation that removed the collision.
    -- v1.0.36's extra RemoveTileObject/indexed insertion path is not used.
    sq:transmitRemoveItemFromSquare(obj)
    local replacement = IsoObject.new(sq, spr)
    sq:AddTileObject(replacement)

    -- The replacement was added locally on the authority; explicitly replicate
    -- the completed plain object to connected clients.
    if isServer() then
        replacement:transmitCompleteItemToClients()
    end
    return true
end

local function onClientCommand(module, command, player, args)
    if module ~= "B47ANCEDBuildableFences" or command ~= "ReplacePost" then return end
    if not player or not args then return end
    local x, y, z = tonumber(args.x), tonumber(args.y), tonumber(args.z)
    if not x or not y or not z then return end

    -- Requests are only accepted near the requesting player; this prevents the
    -- command from being used as a general remote world-object deletion path.
    if math.abs(player:getX() - x) > 15 or math.abs(player:getY() - y) > 15 or player:getZ() ~= z then return end

    local sq = getCell():getGridSquare(x,y,z)
    if not sq then return end
    local objects = sq:getObjects()
    for i = objects:size()-1, 0, -1 do
        local obj = objects:get(i)
        if validPost(obj, args.name, args.sprite) then
            replacePost(obj)
            return
        end
    end
end

Events.OnClientCommand.Add(onClientCommand)
