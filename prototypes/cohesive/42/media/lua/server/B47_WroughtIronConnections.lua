-- B47ANCE'd Buildable Fences v1.1.0-dev.9
-- Newly constructed paid sections only. No scans, repairs or client commands.
if isClient() then return end
require "BuildingObjects/ISBuildUtil"
if B47IronCornerConnectionsInstalled then return end

local sections={
    B47_WroughtIronFence_PlainSection={west="fencing_01_66",north="fencing_01_65"},
    B47_WroughtIronFence_PostEndedSection={west="fencing_01_67",north="fencing_01_64"},
}
local junctionSprite="fencing_01_69"
local original=buildUtil.checkCorner

local function section(obj,north)
    if not obj or not instanceof(obj,"IsoThumpable") or obj:getNorth()~=north then return false end
    local definition=sections[obj:getName()]
    local sprite=obj:getSprite()
    return definition and sprite and sprite:getName()==definition[north and "north" or "west"]
end

function buildUtil.checkCorner(x,y,z,north,thumpable,item)
    -- Unrelated vanilla/mod objects keep their original helper chain.
    if not thumpable or not sections[thumpable:getName()] then
        return original(x,y,z,north,thumpable,item)
    end
    if isClient() or not section(thumpable,north) then return end
    local options=SandboxVars and SandboxVars.B47ANCEDBuildableFences
    local enabled=options and options.WroughtIronCornerPosts
    -- Missing saves use the default; malformed values fail closed.
    if enabled~=nil and enabled~=true then return end
    local cell=getCell()
    if not cell then return end
    local opposite=cell:getGridSquare(x+(north and 1 or -1),y+(north and -1 or 1),z)
    local target=cell:getGridSquare(x+(north and 1 or 0),y+(north and 0 or 1),z)
    if not opposite or not target or target:getWallFull() or target:isSolid() or target:isSolidTrans() then return end
    if target:getSpecialObjects():size()>0 then return end
    local connected=false
    local neighbors=opposite:getSpecialObjects()
    for i=0,neighbors:size()-1 do
        if section(neighbors:get(i),not north) then connected=true; break end
    end
    if not connected then return end
    local objects=target:getObjects()
    for i=0,objects:size()-1 do
        local obj=objects:get(i)
        local sprite=obj and obj:getSprite()
        -- Includes paid posts already converted to a plain IsoObject, native
        -- junctions, and explicit two-edge corner pieces. Never replace them.
        if sprite and (sprite:getName()==junctionSprite or sprite:getName()=="fencing_01_68") then return end
    end
    -- Reuse vanilla creation, square recalculation and complete-item sync.
    -- The post is bundled in the paid section recipe by explicit user choice.
    -- Use a separate descriptor: never mutate the native action/cursor.
    return original(x,y,z,north,thumpable,{corner=junctionSprite})
end
B47IronCornerConnectionsInstalled=true
