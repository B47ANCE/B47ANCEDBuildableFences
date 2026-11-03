"""Installed vanilla tryBuild + bounded recursive-copy model; offline, not PZ."""
import unittest

import test_expanded_catalog as catalog_fixture
from audit_tiles import GAME


class ConstructionActionCopy(unittest.TestCase):
    def setUp(self):
        harness = catalog_fixture.ExpandedCatalog()
        harness.setUp()
        self.lua = harness.lua
        source = (GAME / 'media/lua/server/BuildingObjects/ISBuildingObject.lua').read_text()
        start = source.index('function ISBuildingObject:tryBuild(')
        end = source.index('\nfunction ISBuildingObject:onActionComplete(', start)
        self.assertIn('local selfCopy = copyTable(self)', source[start:end])
        self.lua.execute('ISBuildingObject={}\n' + source[start:end])
        self.lua.execute('''
-- Real engine objects are userdata. Mark their fake table equivalents opaque
-- so recipe/info/logic fixture links are not mistaken for Lua UI-table cycles.
local nativeRefs={}
nativeRefs[player]=true
for _,info in pairs(infos) do
    nativeRefs[info]=true
    nativeRefs[info:getRecipe():getCraftRecipe()]=true
end
foreignInfo=setmetatable({getName=function() return 'Base.Unrelated' end},
    {__index=infos.B47_WroughtIronGate})
nativeRefs[foreignInfo]=true
local newLogic=BuildLogic.new
BuildLogic.new=function(...)
    local logic=newLogic(...)
    nativeRefs[logic]=true
    logic.startCraftAction=function(self,action) self.progress=true; self.action=action end
    return logic
end
function copyTable(value)
    local active={}
    local function copy(t)
        if nativeRefs[t] then return t end
        -- Native copyTable recursively copies table values without memoizing.
        -- Detect the same failure deterministically instead of overflowing Lua.
        assert(not active[t], 'recursive cursor copy reached a Lua table cycle')
        active[t]=true
        local result={}
        for key,item in pairs(t) do
            result[key]=type(item)=='table' and copy(item) or item
        end
        active[t]=nil
        return result
    end
    return copy(value)
end
DebugType={Lua={debugln=function() end}}
Perks={Woodwork=1}
player.getPerkLevel=function() return 7 end
player.isTimedActionInstant=function() return false end
function getSpecificPlayer() return player end
ISBuildIsoEntity.tryBuild=ISBuildingObject.tryBuild
ISBuildIsoEntity.walkTo=function() return true end
ISBuildIsoEntity.onActionComplete=function() end
ISBuildAction={new=function(self,character,item,x,y,z,north,sprite,time)
    queuedAction={character=character,item=item,sprite=sprite,time=time,
        setOnComplete=function() end,setOnCancel=function() end}
    return queuedAction
end}
ISTimedActionQueue={add=function(action) assert(action==queuedAction); queued=true end}
local oldNew=ISBuildIsoEntity.new
function ISBuildIsoEntity:new(...)
    local cursor=oldNew(self,...)
    cursor.noNeedHammer=true
    return cursor
end
local oldCell=getCell
function getCell()
    local cell=oldCell()
    cell.getGridSquare=function() return {} end
    cell.setDrag=function(self,cursor)
        if drag and drag~=cursor then drag:deactivate() end
        drag=cursor
    end
    return cell
end
-- UI objects can contain parent/child/self links; they must never be copied
-- into an action. The self-link makes accidental tooltip copying detectable.
ISEntityBuildMenu.addToolTip=function()
    local tooltip={removed=0,added=0,addToUIManager=function(self) self.added=self.added+1 end,
        removeFromUIManager=function(self) self.removed=self.removed+1 end,
        setX=function() end,setY=function() end,setVisible=function(self,value) self.visible=value end}
    tooltip.self=tooltip
    lastTooltip=tooltip
    return tooltip
end
function openPanel(name)
    queued=false
    panel={logic=BuildLogic.new()}
    setmetatable(panel,{__index=ISBuildPanel})
    panel.logic:setRecipe(infos[name]:getRecipe():getCraftRecipe())
    panel:createBuildIsoEntity(false)
    -- Match the installed panel's persistent placement cursor flags.
    drag.dragNilAfterPlace=false
    drag.blockAfterPlace=true
end
''')

    def test_native_build_start_copies_every_panel_recipe_before_render(self):
        for name in catalog_fixture.info_data():
            with self.subTest(recipe=name):
                self.lua.execute('''
openPanel(...)
local cursor=drag
local action=cursor:tryBuild(1,2,0)
assert(queued and action==queuedAction)
assert(action.item~=cursor and action.item.objectInfo==cursor.objectInfo)
assert(action.item.buildPanelLogic==cursor.buildPanelLogic)
assert(action.item.B47BuildPanel==nil and action.item.B47Requirements==nil)
''', name)

    def test_panel_preview_ui_is_not_copied_into_native_action(self):
        self.lua.execute('''
openPanel('B47_RazorWireSecurityFence_PlainSection')
drag:render(0,0,0,{})
assert(lastTooltip.visible and lastTooltip.added==1)
local action=drag:tryBuild(1,2,0)
assert(queued and action.item.B47Requirements==nil and action.item.B47BuildPanel==nil)
''')

    def test_context_preview_ui_is_not_copied_into_native_action(self):
        self.lua.execute('''
ISEntityBuildMenu.onBuildEntity(player,infos.B47_WroughtIronGate)
drag:render(0,0,0,{})
local action=drag:tryBuild(1,2,0)
assert(queued and action.item.B47Requirements==nil)
''')

    def test_queued_face_recipe_and_native_logic_survive_selector_changes(self):
        self.lua.execute('''
openPanel('B47_WroughtIronFence_PlainSection')
drag:rotateKey(Keyboard.KEY_E)
drag:rotateKey(Keyboard.KEY_E)
local cursor=drag
local info,face,recipe=cursor.objectInfo,cursor.nSprite,panel.logic:getRecipe()
local action=cursor:tryBuild(1,2,0)
drag:rotateKey(Keyboard.KEY_E)
assert(drag==cursor and panel.logic:getRecipe()==recipe)
assert(action.item.objectInfo==info and action.item.nSprite==face)
assert(action.item.B47ChosenFace==face and action.item.craftRecipe==recipe)
assert(action.item.buildPanelLogic==panel.logic)
panel.logic.progress=false
drag:rotateKey(Keyboard.KEY_E)
assert(action.item.objectInfo==info and action.item.nSprite==face)
''')

    def test_deactivate_removes_tooltip_and_reused_panel_cursor_can_cycle(self):
        self.lua.execute('''
openPanel('B47_TallWoodenFence_StraightTop')
drag:render(0,0,0,{})
local tooltip,cursor=lastTooltip,drag
getCell():setDrag(nil,0)
assert(tooltip.removed==1 and tooltip.visible==false)
cursor:deactivate()
assert(tooltip.removed==1)
panel:createBuildIsoEntity(false)
assert(drag==cursor)
drag:rotateKey(Keyboard.KEY_E)
assert(panel.logic:getRecipe()==drag.craftRecipe)
drag:render(0,0,0,{})
assert(lastTooltip~=tooltip and lastTooltip.added==1)
drag:tryBuild(1,2,0)
assert(queued)
''')

    def test_unrelated_native_cursor_keeps_its_original_render_and_action(self):
        self.lua.execute('''
ISEntityBuildMenu.onBuildEntity(player,foreignInfo)
assert(not B47Cohesive.cursor(drag))
drag:render(0,0,0,{})
assert(rendered=='original' and lastTooltip==nil)
local action=drag:tryBuild(1,2,0)
assert(queued and action.item.objectInfo==foreignInfo)
''')


if __name__ == '__main__':
    unittest.main()
