-- B47ANCE'd Buildable Fences v1.1.0-dev.3
require "B47_CohesiveModel"
require "B47_FenceConstruction"
local C = B47Cohesive
local dirty = {}
local busy = false
local postMarker = "B47CohesiveIronPost"
function C.queue(x,y,z)
    if isClient() then return end
    dirty[C.key(x,y,z)] = {x=x,y=y,z=z}
end
local function queueObject(obj)
    if isClient() or busy or not obj then return end
    local sq = obj:getSquare()
    if sq and (C.readObject(obj) or obj:getModData()[C.marker] or obj:getModData()[postMarker]) then
        C.queue(sq:getX(),sq:getY(),sq:getZ())
    end
end
local function reconcilePost(x,y,z,wanted)
    local sq = getCell():getGridSquare(x,y,z)
    if not sq then return end
    local posts = {}
    local objects = sq:getObjects()
    for i=0,objects:size()-1 do
        local obj = objects:get(i)
        if obj:getModData()[postMarker] == 1 and not instanceof(obj,"IsoThumpable")
            and obj:getSprite() and obj:getSprite():getName() == "fencing_01_69" then
            posts[#posts+1] = obj
        end
    end
    for i=#posts,(wanted and 2 or 1),-1 do sq:transmitRemoveItemFromSquare(posts[i]) end
    if wanted and #posts == 0 then
        -- Reuse the proven baseline's final nonblocking object type directly.
        local obj = IsoObject.new(sq,"fencing_01_69")
        obj:getModData()[postMarker] = 1
        sq:AddTileObject(obj)
        if isServer() then obj:transmitCompleteItemToClients() end
    end
end
function C.recalculate(x,y,z,newObject)
    if isClient() or busy then return end
    busy = true
    local edges = C.collect(x,y,z,2)
    local vertices = {}
    -- Clear orphan posts even when the last adjacent section has gone.
    for xx=x-1,x+1 do for yy=y-1,y+1 do
        vertices[C.key(xx,yy,z)] = {xx,yy}
    end end
    for _,e in ipairs(edges) do
        if math.abs(e.x-x)<=1 and math.abs(e.y-y)<=1 and e.managed then
            local ex,ey = C.finish(e)
            vertices[C.key(ex,ey,z)] = {ex,ey}
            if C.vertexLoaded(e.x,e.y,z) and e.kind == "fence" then
                local wanted = C.sprite(e,edges)
                if e.obj:getSprite():getName() ~= wanted then
                    e.obj:setSpriteFromName(wanted) -- also updates native closedSprite
                    e.obj:getSquare():RecalcAllWithNeighbours(true)
                    if isServer() and e.obj ~= newObject then e.obj:transmitUpdatedSpriteToClients() end
                end
            end
        end
    end
    for _,v in pairs(vertices) do
        if C.vertexLoaded(v[1],v[2],z) then
            local _,wanted = C.vertex(edges,v[1],v[2],z)
            local owned = false
            for _,e in ipairs(C.incident(edges,v[1],v[2],z)) do
                if e.managed then owned = true end
            end
            reconcilePost(v[1],v[2],z,wanted and owned)
        end
    end
    busy = false
end
local originalCreate = B47Fence.OnCreate
function B47Fence.OnCreate(params)
    if isClient() then return end
    originalCreate(params) -- family health and sounds assigned before topology
    local obj = params and params.thumpable
    local edge = C.readObject(obj)
    if edge and obj:getName() == C.fenceName then
        obj:getModData()[C.marker] = {schema=1,axis=edge.axis}
        C.recalculate(edge.x,edge.y,edge.z,obj)
        C.queue(edge.x,edge.y,edge.z)
    end
    -- nil preserves native full-object transmission with final sprite/modData.
end
function C.OnCreateGate(params)
    if isClient() then return end
    local obj = params and params.thumpable
    local edge = C.readObject(obj)
    if not edge or edge.kind ~= "gate" then return end
    obj:setThumpSound("ZombieThumpMetalPoleFence")
    obj:setBreakSound("BreakDoor")
    local opts = SandboxVars and SandboxVars.B47ANCEDBuildableFences
    local percent = opts and tonumber(opts.ConstructionHealthPercent) or 100
    if not percent or percent ~= percent or percent<10 or percent>500 then percent=100 end
    percent = math.floor(percent)
    if percent ~= 100 then
        local hp = math.max(1,math.floor(obj:getMaxHealth()*percent/100+0.5))
        obj:setMaxHealth(hp); obj:setHealth(hp)
    end
    obj:getModData()[C.marker] = {schema=1,axis=edge.axis}
    C.recalculate(edge.x,edge.y,edge.z,obj)
    C.queue(edge.x,edge.y,edge.z)
end
function C.tick()
    if isClient() then return end
    local batch = {}
    for key,v in pairs(dirty) do
        batch[#batch+1] = v; dirty[key] = nil
        if #batch == 8 then break end
    end
    for _,v in ipairs(batch) do C.recalculate(v.x,v.y,v.z) end
end
function C.loadSquare(sq)
    if isClient() or not sq then return end
    -- A previously unavailable incident square becoming loaded can complete
    -- the neighborhood even when that new square is empty.
    local x,y,z = sq:getX(),sq:getY(),sq:getZ()
    for xx=x-1,x+1 do for yy=y-1,y+1 do
        local nearby = getCell():getGridSquare(xx,yy,z)
        if nearby then
            local objects = nearby:getObjects()
            for i=0,objects:size()-1 do
                local obj = objects:get(i)
                if obj:getModData()[C.marker] or obj:getModData()[postMarker] then
                    C.queue(xx,yy,z)
                end
            end
        end
    end end
end
-- Removal runs AFTER the event: native OnObjectAboutToBeRemoved forbids
-- removing its argument, and the event fires before actual world removal.
Events.OnObjectAdded.Add(queueObject)
Events.OnObjectAboutToBeRemoved.Add(queueObject)
Events.OnDestroyIsoThumpable.Add(queueObject)
Events.LoadGridsquare.Add(C.loadSquare)
Events.OnTick.Add(C.tick)
