-- B47ANCE'd Buildable Fences v1.1.0-dev.3
require "B47_CohesiveCursor"
require "Entity/ISUI/ISEntityBuildMenu"
require "Entity/ISUI/BuildRecipe/ISBuildPanel"
local C = B47Cohesive
local hidden = { B47_WroughtIronFence_PostEndedSection=true,
                 B47_WroughtIronFence_Corner=true, B47_WroughtIronFence_Post=true }
local function filterInfos(infos)
    local filtered = {}
    for _,info in ipairs(infos) do
        if not hidden[info:getName()] then filtered[#filtered+1] = info end
    end
    return filtered
end
local originalAll = ISBuildIsoEntity.GetAllBuildableEntities
function ISBuildIsoEntity.GetAllBuildableEntities() return filterInfos(originalAll()) end
local originalAvailable = ISBuildIsoEntity.GetBuildableEntities
function ISBuildIsoEntity.GetBuildableEntities(player)
    local infos,items = originalAvailable(player)
    return filterInfos(infos),items
end
-- The build window uses BuildLogic directly, independently of context menus.
-- Populate its native recipe lookup first, then filter by recipe identity.
function ISBuildPanel:refreshList()
    local all = self.logic:getAllBuildableRecipes()
    local excluded = {}
    for name in pairs(hidden) do
        local info = SpriteConfigManager.GetObjectInfo(name)
        if info and info:getRecipe() then excluded[info:getRecipe():getCraftRecipe()] = true end
    end
    local list = ArrayList.new()
    for i=0,all:size()-1 do
        local recipe = all:get(i)
        if not excluded[recipe] then list:add(recipe) end
    end
    self.logic:setRecipes(list)
    self:ReselectRecipeOrFirst(self.logic:getLastSelectedRecipe())
end
local originalRender = ISBuildIsoEntity.render
function ISBuildIsoEntity:render(x,y,z,square)
    if not C.cursor(self) or self.objectInfo:getName() == C.gateName then
        return originalRender(self,x,y,z,square)
    end
    self:ensureSquaresExist(x,y,z)
    self:getSprite() -- synchronize north with native selected face immediately
    self.isWallLike = true
    local valid = self:isValid(square)
    self:renderFloorGrid(x,y,z)
    local axis = self.north and "N" or "W"
    local edges = C.collect(x,y,z,2)
    local edge = {x=x,y=y,z=z,axis=axis,kind="fence",managed=true}
    edges[#edges+1] = edge
    local function ghost(name,gx,gy)
        local spr = self.spriteCache[name]
        if not spr then
            spr = IsoSprite.new(); spr:LoadSingleTexture(name); self.spriteCache[name] = spr
        end
        spr:RenderGhostTileColor(gx,gy,z,0,0,valid and 1 or 0.65,valid and 1 or 0.2,valid and 1 or 0.2,0.6)
    end
    ghost(C.sprite(edge,edges),x,y)
    local ex,ey = C.finish(edge)
    for _,v in ipairs({{x,y},{ex,ey}}) do
        local _,post = C.vertex(edges,v[1],v[2],z)
        if post then ghost("fencing_01_69",v[1],v[2]) end
    end
end
