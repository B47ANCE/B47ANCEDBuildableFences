-- B47ANCE'd Buildable Fences v1.1.0-dev.19
-- Client files load before the native server-side cursor directory is available.
-- Install once after the complete world Lua load; never require it at boot.
local function installPresentation()
if B47Cohesive.presentationInstalled then return end
require "B47_CohesiveCursor"
require "Entity/ISUI/ISEntityBuildMenu"
require "Entity/ISUI/BuildRecipe/ISBuildPanel"
local V=B47Cohesive
-- Vanilla tryBuild recursively copies cursor table values into its action.
-- UI graphs contain cycles (panel.buildEntity points back to the cursor), so
-- keep them outside the cursor. Only primitive selection state travels with it.
local panels=setmetatable({},{__mode="k"})
local requirements=setmetatable({},{__mode="k"})
local function filtered(infos)
    local result,seen={},{}
    for _,info in ipairs(infos) do
        local family=V.familyByName[info:getName()]
        local entry=family and SpriteConfigManager.GetObjectInfo(family[1]) or info
        -- Native available lists can contain only an affordable post/corner.
        -- Represent that member by its root rather than dropping the family.
        if entry and not seen[entry:getName()] then
            seen[entry:getName()]=true
            result[#result+1]=entry
        end
    end
    return result
end
local originalAll=ISBuildIsoEntity.GetAllBuildableEntities
function ISBuildIsoEntity.GetAllBuildableEntities() return filtered(originalAll()) end
local originalAvailable=ISBuildIsoEntity.GetBuildableEntities
function ISBuildIsoEntity.GetBuildableEntities(player)
    local infos,items=originalAvailable(player)
    return filtered(infos),items
end
local originalTooltip=ISEntityBuildMenu.createToolTip
function ISEntityBuildMenu.createToolTip(option,player,info)
    local onSelect=option.onSelect
    local tooltip=originalTooltip(option,player,info)
    -- The family entry is access to cheaper pieces too. Missing Plain inputs
    -- must not prevent entering the selector to choose the Post recipe.
    if V.roots[info:getName()] then
        option.onSelect=onSelect
        option.notAvailable=false
    end
    return tooltip
end
function ISBuildPanel:refreshList()
    local all=self.logic:getAllBuildableRecipes() -- keep native entity lookup
    local present={}
    for i=0,all:size()-1 do present[all:get(i)]=true end
    local familyByRecipe,preferred={},{}
    for _,family in ipairs(V.families) do
        local root=family[1]
        for _,name in ipairs(family) do
            local info=SpriteConfigManager.GetObjectInfo(name)
            if info and info:getRecipe() then
                local recipe=info:getRecipe():getCraftRecipe()
                familyByRecipe[recipe]=root
                if name==root and present[recipe] then preferred[root]=recipe end
            end
        end
    end
    local list,seen=ArrayList.new(),{}
    for i=0,all:size()-1 do
        local recipe=all:get(i)
        local family=familyByRecipe[recipe]
        if not family then
            list:add(recipe) -- preserve unrelated vanilla/mod recipes verbatim
        elseif not seen[family] and (not preferred[family] or preferred[family]==recipe) then
            -- Without a native root, retain the first supplied member rather
            -- than hiding the whole family. Never inject a different recipe.
            list:add(recipe)
            seen[family]=true
        end
    end
    self.logic:setRecipes(list)
    self:ReselectRecipeOrFirst(self.logic:getLastSelectedRecipe())
end
local function inProgress(cursor)
    return cursor.buildPanelLogic and cursor.buildPanelLogic:isCraftActionInProgress()
end
local function equip(cursor)
    local function tool(input)
        if not input then return nil end
        local items=input:getPossibleInputItems()
        local inventory=cursor.character:getInventory()
        for i=0,items:size()-1 do
            local name=items:get(i):getFullName()
            if inventory:getAllTypeEvalRecurse(name,ISBuildIsoEntity.predicateMaterial):size()>0 then return name end
        end
    end
    local recipe=cursor.craftRecipe
    cursor.equipBothHandItem=tool(recipe:getToolBoth())
    cursor.firstItem=tool(recipe:getToolRight())
    cursor.secondItem=tool(recipe:getToolLeft())
end
function V.cycle(cursor,delta)
    -- Native action copies cursor fields but shares BuildLogic. Freeze recipe
    -- changes until completion/cancel so queued/in-progress cost cannot change.
    if inProgress(cursor) then return end
    cursor:getSprite()
    local state=V.nextState(cursor,delta)
    if not state then return end
    local panel=panels[cursor]
    if panel then
        panel.B47PendingFace=state.nSprite
        panel.logic:setRecipe(state.recipe) -- native widgets update live
        panel:createBuildIsoEntity(false)
    else
        local containers=ISInventoryPaneContextMenu.getContainers(cursor.character)
        local nextCursor=ISBuildIsoEntity:new(cursor.character,state.info,state.nSprite,containers)
        nextCursor.dragNilAfterPlace=cursor.dragNilAfterPlace
        nextCursor.blockAfterPlace=cursor.blockAfterPlace
        equip(nextCursor)
        V.pin(nextCursor,state.nSprite)
        getCell():setDrag(nextCursor,cursor.player)
    end
end
local originalPanelCursor=ISBuildPanel.createBuildIsoEntity
function ISBuildPanel:createBuildIsoEntity(dontSetDrag)
    -- An in-progress action owns the shared logic; retain original cursor/recipe.
    if self.buildEntity and V.cursor(self.buildEntity) and inProgress(self.buildEntity) then return end
    originalPanelCursor(self,dontSetDrag)
    local cursor=self.buildEntity
    if cursor and V.cursor(cursor) then
        panels[cursor]=self
        if self.B47PendingFace then
            V.pin(cursor,self.B47PendingFace)
            self.B47PendingFace=nil
        elseif not cursor.B47ChosenFace then
            cursor:getFace(); V.pin(cursor,cursor.nSprite)
        end
    end
end
local function description(cursor)
    local recipe=cursor.objectInfo:getRecipe():getCraftRecipe()
    local suffix=cursor.objectInfo:getName():match("_([^_]+)$")
    local text=getText("IGUI_B47_VariantSelected",getText("IGUI_B47_Variant_"..suffix),cursor:getFace():getFaceName())
    text=text.." <LINE> "..getText("IGUI_B47_VariantControls").." <LINE> "
    for i=0,recipe:getRequiredSkillCount()-1 do
        local skill=recipe:getRequiredSkill(i)
        text=text..tostring(skill:getPerk():getName())..": "..skill:getLevel().." <LINE> "
    end
    local inputs=recipe:getInputs()
    for i=0,inputs:size()-1 do
        local input=inputs:get(i)
        local options=input:getPossibleInputItems()
        local names={}
        for n=0,options:size()-1 do names[#names+1]=getItemNameFromFullType(options:get(n):getFullName()) end
        text=text..table.concat(names," / ")..": "..input:getAmount()
        if input:isKeep() then text=text.." "..getText("IGUI_B47_VariantKeep") end
        text=text.." <LINE> "
    end
    return text
end
local originalRender=ISBuildIsoEntity.render
function ISBuildIsoEntity:render(x,y,z,square)
    if not V.cursor(self) then return originalRender(self,x,y,z,square) end
    self:getSprite()
    if not inProgress(self) then
        self.buildPanelLogic:updateFloorContainer()
        self.buildPanelLogic:autoPopulateInputs()
    end
    originalRender(self,x,y,z,square) -- render EXACT existing entity face
    if not requirements[self] then
        requirements[self]=ISEntityBuildMenu.addToolTip()
        requirements[self]:addToUIManager()
    end
    local tooltip=requirements[self]
    tooltip.description=description(self)
    tooltip.footNote=getText("IGUI_B47_VariantControls")
    tooltip:setX(getMouseX()+24); tooltip:setY(getMouseY()+24)
    tooltip:setVisible(true)
end
local originalDeactivate=ISBuildIsoEntity.deactivate
function ISBuildIsoEntity:deactivate()
    local tooltip=requirements[self]
    if tooltip then
        tooltip:setVisible(false)
        tooltip:removeFromUIManager()
        requirements[self]=nil
    end
    panels[self]=nil
    return originalDeactivate(self)
end
-- Context path constructs the initial native cursor; pin its selected face.
local originalMenuBuild=ISEntityBuildMenu.onBuildEntity
function ISEntityBuildMenu.onBuildEntity(player,info)
    originalMenuBuild(player,info)
    local cursor=getCell():getDrag(player:getPlayerNum())
    if V.cursor(cursor) then cursor:getFace(); V.pin(cursor,cursor.nSprite) end
end
B47Cohesive.presentationInstalled=true
end
Events.OnGameStart.Add(installPresentation)
