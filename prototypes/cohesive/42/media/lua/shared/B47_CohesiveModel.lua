-- B47ANCE'd Buildable Fences v1.1.0-dev.15
-- UI selection model only. No topology, world scans or permanent state writes.
require "B47_ExpandedCatalog"
B47Cohesive = B47Cohesive or {}
local V=B47Cohesive
-- Group identifiers are UI membership only; recipes remain owned by ObjectInfo.
V.families={
    {"B47_TallWoodenFence_StraightTop","B47_TallWoodenFence_StraightTopCorner","B47_TallWoodenFence_StraightTopPost"},
    {"B47_TallWoodenFence_PostEnded","B47_TallWoodenFence_Continuous","B47_TallWoodenFence_Corner","B47_TallWoodenFence_Post"},
    {"B47_MilitaryFence_PlainSection","B47_MilitaryFence_PostEndedSection","B47_MilitaryFence_Corner","B47_MilitaryFence_Post"},
    {"B47_SecurityFence_PlainSection","B47_SecurityFence_PostEndedSection","B47_SecurityFence_Corner"},
    {"B47_RazorWireSecurityFence_PlainSection","B47_RazorWireSecurityFence_PostEndedSection","B47_RazorWireSecurityFence_Corner"},
    {"B47_WroughtIronFence_PlainSection","B47_WroughtIronFence_PostEndedSection","B47_WroughtIronFence_Corner","B47_WroughtIronFence_Post"},
}
if B47ExpandedCatalog then
    for _,family in ipairs(B47ExpandedCatalog.families) do V.families[#V.families+1]=family end
end
V.names=V.families[6] -- retained iron alias for existing integrations
V.gateName="B47_WroughtIronGate"
V.variantNames={}; V.familyByName={}; V.roots={}; V.hidden={}
for _,family in ipairs(V.families) do
    V.roots[family[1]]=true
    for i,name in ipairs(family) do
        V.variantNames[name]=i
        V.familyByName[name]=family
        if i>1 then V.hidden[name]=true end
    end
end
function V.cursor(cursor)
    local name=cursor and cursor.objectInfo and cursor.objectInfo:getName()
    return name and (V.variantNames[name] or name==V.gateName) or false
end
function V.states(selection)
    local result={}
    local names
    if selection==true or selection==V.gateName then names={V.gateName}
    elseif type(selection)=="string" then names=V.familyByName[selection]
    else names=V.names end
    if not names then return nil end
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
    local states=V.states(cursor.objectInfo:getName())
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
