-- B47ANCE'd Buildable Fences v1.1.0-dev.3
-- Independent edge topology. No world writes or client commands.
B47Cohesive = B47Cohesive or {}
local C = B47Cohesive
C.fenceName = "B47_WroughtIronFence_PlainSection"
C.gateName = "B47_WroughtIronGate"
C.marker = "B47CohesiveIron"
C.sprites = { W = {plain="fencing_01_66", ending="fencing_01_67"},
              N = {plain="fencing_01_65", ending="fencing_01_64"} }
C.gateSprites = { W={closed="fixtures_doors_fences_01_20", open="fixtures_doors_fences_01_22"},
                  N={closed="fixtures_doors_fences_01_21", open="fixtures_doors_fences_01_23"} }
function C.key(x,y,z) return x .. ":" .. y .. ":" .. z end
function C.finish(edge)
    return edge.x + (edge.axis == "N" and 1 or 0), edge.y + (edge.axis == "W" and 1 or 0)
end
function C.incident(edges,x,y,z)
    local found = {}
    for _,e in ipairs(edges) do
        local ex,ey = C.finish(e)
        if e.z == z and ((e.x == x and e.y == y) or (ex == x and ey == y)) then
            found[#found+1] = e
        end
    end
    table.sort(found,function(a,b)
        return C.key(a.x,a.y,a.z) .. a.axis < C.key(b.x,b.y,b.z) .. b.axis
    end)
    return found
end
-- A gate keeps its native art, state and axis. Fence end art owns a post at
-- its starting vertex. A vertex with no such owner uses one nonblocking post.
function C.vertex(edges,x,y,z)
    local incident = C.incident(edges,x,y,z)
    if #incident == 0 then return nil,false end
    local straight = #incident == 2 and incident[1].axis == incident[2].axis
    if straight then return nil,false end
    for _,e in ipairs(incident) do
        if e.kind == "gate" then return nil,false end -- native gate art supplies posts
    end
    for _,e in ipairs(incident) do
        if e.x == x and e.y == y and (e.managed ~= false or e.hasPost) then return e,false end
    end
    return nil,true
end
function C.sprite(edge,edges)
    if edge.kind == "gate" then return C.gateSprites[edge.axis].closed end
    local owner = C.vertex(edges,edge.x,edge.y,edge.z)
    return C.sprites[edge.axis][owner == edge and "ending" or "plain"]
end
function C.readObject(obj)
    if not obj or not instanceof(obj,"IsoThumpable") then return nil end
    local sq, spr = obj:getSquare(),obj:getSprite()
    if not sq or not spr then return nil end
    local name, sprite = obj:getName(),spr:getName()
    local axis = obj:getNorth() and "N" or "W"
    local kind
    if name == C.fenceName or name == "B47_WroughtIronFence_PostEndedSection" then
        local s = C.sprites[axis]
        if sprite ~= s.plain and sprite ~= s.ending then return nil end
        kind = "fence"
    elseif name == C.gateName then
        local s = C.gateSprites[axis]
        if sprite ~= s.closed and sprite ~= s.open then return nil end
        kind = "gate"
    else return nil end
    local marker = obj:getModData()[C.marker]
    -- Existing manual fences are read-only connection anchors. Their health,
    -- name, sprite and save schema are never migrated by this prototype.
    local managed = type(marker) == "table" and marker.schema == 1 and marker.axis == axis
    return {x=sq:getX(),y=sq:getY(),z=sq:getZ(),axis=axis,kind=kind,obj=obj,managed=managed,
            hasPost=kind == "fence" and sprite == C.sprites[axis].ending}
end
function C.collect(x,y,z,radius)
    local edges = {}
    for xx=x-radius,x+radius do
        for yy=y-radius,y+radius do
            local sq = getCell():getGridSquare(xx,yy,z)
            if sq then
                local objects = sq:getObjects()
                for i=0,objects:size()-1 do
                    local edge = C.readObject(objects:get(i))
                    if edge then edges[#edges+1] = edge end
                end
            end
        end
    end
    return edges
end
function C.vertexLoaded(x,y,z)
    -- All possible incident edge squares must be loaded before committing.
    return getCell():getGridSquare(x,y,z) ~= nil
       and getCell():getGridSquare(x-1,y,z) ~= nil
       and getCell():getGridSquare(x,y-1,z) ~= nil
end
function C.cursor(cursor)
    return cursor and cursor.objectInfo and
        (cursor.objectInfo:getName() == C.fenceName or cursor.objectInfo:getName() == C.gateName)
end
