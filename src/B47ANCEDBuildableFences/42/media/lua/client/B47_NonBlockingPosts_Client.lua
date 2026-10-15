-- B47ANCE'd Buildable Fences v1.1.0-dev.14
-- MP client detector for standalone posts.
-- In multiplayer the client never mutates authoritative world objects. It asks
-- the server to perform the same replacement proven by v1.0.33/v1.0.35.
-- In single-player we retain the exact known-good local replacement path.

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
local requested = {}
local tick = 0

local function spriteName(obj)
    local spr = obj and obj:getSprite()
    return spr and spr:getName() or nil
end

local function isPost(obj)
    if not obj or not instanceof(obj, "IsoThumpable") then return false end
    return POST_NAMES[obj:getName()] == true and POST_SPRITES[spriteName(obj)] == true
end

local function keyFor(obj)
    local sq = obj:getSquare()
    if not sq then return nil end
    return tostring(sq:getX())..":"..tostring(sq:getY())..":"..tostring(sq:getZ())..":"..tostring(spriteName(obj))
end

local function convertSinglePlayer(obj)
    local sq = obj:getSquare()
    local spr = spriteName(obj)
    if not sq or not spr then return end
    -- Exact known-good v1.0.35 operation. Do not add wall type/depth flags here.
    sq:transmitRemoveItemFromSquare(obj)
    local replacement = IsoObject.new(sq, spr)
    sq:AddTileObject(replacement)
end

local function handle(obj)
    if not isPost(obj) then return end
    local sq = obj:getSquare()
    if not sq then return end

    if not isClient() then
        convertSinglePlayer(obj)
        return
    end

    local key = keyFor(obj)
    if not key or requested[key] then return end
    requested[key] = true
    sendClientCommand("B47ANCEDBuildableFences", "ReplacePost", {
        x = sq:getX(), y = sq:getY(), z = sq:getZ(),
        sprite = spriteName(obj), name = obj:getName(),
    })
end

local function scan(player)
    tick = tick + 1
    if tick % 30 ~= 0 then return end
    player = player or getPlayer()
    if not player then return end
    local cell = getCell()
    local px, py, pz = math.floor(player:getX()), math.floor(player:getY()), player:getZ()
    for x = px-10, px+10 do
        for y = py-10, py+10 do
            local sq = cell:getGridSquare(x,y,pz)
            if sq then
                local objects = sq:getObjects()
                for i = objects:size()-1, 0, -1 do
                    handle(objects:get(i))
                end
            end
        end
    end
end

Events.OnPlayerUpdate.Add(scan)
