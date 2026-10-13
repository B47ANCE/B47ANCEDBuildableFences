-- B47ANCE'd Buildable Fences v1.1.0-dev.6
-- UI selection model only. No topology, world scans or permanent state writes.
B47Cohesive = B47Cohesive or {}
local V=B47Cohesive
V.names={"B47_WroughtIronFence_PlainSection","B47_WroughtIronFence_PostEndedSection",
         "B47_WroughtIronFence_Corner","B47_WroughtIronFence_Post"}
V.gateName="B47_WroughtIronGate"
V.variantNames={}
for i,name in ipairs(V.names) do V.variantNames[name]=i end
function V.cursor(cursor)
    local name=cursor and cursor.objectInfo and cursor.objectInfo:getName()
    return name and (V.variantNames[name] or name==V.gateName) or false
end
function V.states(gate)
    local result={}
    local names=gate and {V.gateName} or V.names
    -- Native nSprite WNES -> native face indices NWSE. Enumerate only faces
    -- that actually exist, never synthesize a corner or E/S orientation.
    local indices={1,0,3,2}
    for _,name in ipairs(names) do
        local info=SpriteConfigManager.GetObjectInfo(name)
        if not info or not info:getRecipe() then return nil end
        for nSprite,index in ipairs(indices) do
            local face=info:getFace(index)
            if face then
                result[#result+1]={info=info,nSprite=nSprite,face=face,
                    recipe=info:getRecipe():getCraftRecipe()}
            end
        end
    end
    return #result>0 and result or nil
end
function V.nextState(cursor,delta)
    local states=V.states(cursor.objectInfo:getName()==V.gateName)
    if not states then return nil end
    for i,state in ipairs(states) do
        if state.info==cursor.objectInfo and state.nSprite==cursor.nSprite then
            return states[((i-1+delta)%#states)+1]
        end
    end
    return states[1]
end
function V.pin(cursor,nSprite)
    cursor.B47ChosenFace=nSprite
    cursor.nSprite=nSprite
    cursor.nSpriteCache=-1
    cursor:getSprite()
end
