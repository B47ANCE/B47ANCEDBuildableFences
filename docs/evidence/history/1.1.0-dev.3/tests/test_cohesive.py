"""Executed Lua topology/authority tests with fake world; never native PZ proof."""
import itertools
import json
import unittest
from pathlib import Path
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "prototypes/cohesive/42"
MODEL = OVERLAY / "media/lua/shared/B47_CohesiveModel.lua"

FAKE = r'''
client=false; server=true; sent=0; removed=0
function isClient() return client end
function isServer() return server end
function instanceof(obj,kind) return obj.class == kind end
function require(name) end
local function event() return {Add=function(fn) end} end
Events={OnObjectAdded=event(),OnObjectAboutToBeRemoved=event(),OnDestroyIsoThumpable=event(),LoadGridsquare=event(),OnTick=event()}
world={}; SandboxVars={}
function list(items)
 return {size=function() return #items end,get=function(self,i) return items[i+1] end}
end
function square(x,y,z)
 local sq={x=x,y=y,z=z,items={}}
 function sq:getX() return self.x end
 function sq:getY() return self.y end
 function sq:getZ() return self.z end
 function sq:getObjects() return list(self.items) end
 function sq:AddTileObject(o) o.square=self; self.items[#self.items+1]=o end
 function sq:RecalcAllWithNeighbours() end
 function sq:transmitRemoveItemFromSquare(o)
  for i,v in ipairs(self.items) do if v==o then table.remove(self.items,i); removed=removed+1; return end end
 end
 world[x..':'..y..':'..z]=sq; return sq
end
function getCell() return {getGridSquare=function(self,x,y,z) return world[x..':'..y..':'..z] end} end
for x=-4,5 do for y=-4,5 do square(x,y,0) end end
function object(sq,name,sprite,north,class)
 local o={square=sq,name=name,sprite=sprite,north=north,class=class or 'IsoThumpable',data={},health=777,maxHealth=999,thump='iron',breakSound='metal'}
 function o:getSquare() return self.square end
 function o:getSprite() local name=self.sprite; return {getName=function() return name end} end
 function o:getName() return self.name end
 function o:getNorth() return self.north end
 function o:getModData() return self.data end
 function o:setSpriteFromName(s) self.sprite=s end
 function o:transmitUpdatedSpriteToClients() sent=sent+1 end
 function o:transmitCompleteItemToClients() sent=sent+1 end
 function o:setThumpSound(s) self.thump=s end
 function o:setBreakSound(s) self.breakSound=s end
 function o:getMaxHealth() return self.maxHealth end
 function o:setMaxHealth(n) self.maxHealth=n end
 function o:setHealth(n) self.health=n end
 sq:AddTileObject(o); return o
end
IsoObject={new=function(sq,sprite) local o=object(sq,'',sprite,false,'IsoObject'); table.remove(sq.items); return o end}
B47Fence={OnCreate=function() end}
function build(x,y,axis)
 local C=B47Cohesive; local sq=world[x..':'..y..':0']
 local o=object(sq,C.fenceName,C.sprites[axis].plain,axis=='N')
 B47Fence.OnCreate({thumpable=o}); return o
end
function posts()
 local n=0
 for _,sq in pairs(world) do for _,o in ipairs(sq.items) do if o.class=='IsoObject' then n=n+1 end end end
 return n
end
'''

class CohesiveTests(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute(FAKE)
        self.lua.execute(MODEL.read_text())
        self.lua.execute((OVERLAY / "media/lua/server/B47_CohesiveAuthority.lua").read_text())

    def test_isolated_straight_removal_and_rebuild(self):
        self.lua.execute("a=build(0,0,'W'); b=build(0,1,'W'); c=build(0,2,'W')")
        self.assertEqual(self.lua.eval("a.sprite"), "fencing_01_67")
        self.assertEqual(self.lua.eval("b.sprite"), "fencing_01_66")
        self.assertEqual(self.lua.eval("c.sprite"), "fencing_01_66")
        self.assertEqual(self.lua.eval("posts()"), 1)
        self.lua.execute("b.square:transmitRemoveItemFromSquare(b); B47Cohesive.queue(0,1,0); B47Cohesive.tick()")
        self.assertEqual(self.lua.eval("c.sprite"), "fencing_01_67")
        self.assertEqual(self.lua.eval("posts()"), 2)
        self.lua.execute("b=build(0,1,'W'); B47Cohesive.tick()")
        self.assertEqual(self.lua.eval("c.sprite"), "fencing_01_66")
        self.assertEqual(self.lua.eval("posts()"), 1)

    def test_intent_axis_survives_all_corner_arrangements(self):
        for layout in [[(0,0,"W"),(0,0,"N")],[(0,0,"W"),(0,1,"N")],[(0,0,"N"),(1,0,"W")],[(0,-1,"W"),(-1,0,"N")]]:
            for order in itertools.permutations(layout):
                self.setUp()
                for x,y,axis in order: self.lua.execute(f"build({x},{y},'{axis}')")
                self.lua.execute("B47Cohesive.tick()")
                self.lua.execute("for _,sq in pairs(world) do for _,o in ipairs(sq.items) do if o.class=='IsoThumpable' then assert(o.sprite == B47Cohesive.sprites[o.north and 'N' or 'W'].plain or o.sprite == B47Cohesive.sprites[o.north and 'N' or 'W'].ending); assert(o.health==777 and o.maxHealth==999 and o.thump=='iron' and o.breakSound=='metal') end end end")

    def test_corner_has_one_shared_post_and_no_dual_axis_sprite(self):
        self.lua.execute("a=build(0,0,'W'); b=build(0,0,'N'); B47Cohesive.tick()")
        self.assertEqual(self.lua.eval("a.sprite"), "fencing_01_66")
        self.assertEqual(self.lua.eval("b.sprite"), "fencing_01_64")
        self.assertEqual(self.lua.eval("posts()"), 2)  # far ends; shared post is embedded

    def test_clients_cannot_commit_or_queue(self):
        self.lua.execute("client=true; a=build(0,0,'W'); B47Cohesive.queue(0,0,0); B47Cohesive.tick(); B47Cohesive.recalculate(0,0,0)")
        self.assertEqual(self.lua.eval("a.sprite"), "fencing_01_66")
        self.assertIsNone(self.lua.eval("a.data.B47CohesiveIron"))
        self.assertEqual(self.lua.eval("sent+posts()"), 0)

    def test_duplicate_recalculation_and_orphan_cleanup(self):
        self.lua.execute("a=build(0,0,'N'); for i=1,10 do B47Cohesive.recalculate(0,0,0) end")
        self.assertEqual(self.lua.eval("posts()"), 1)
        self.lua.execute("a.square:transmitRemoveItemFromSquare(a); B47Cohesive.recalculate(0,0,0)")
        self.assertEqual(self.lua.eval("posts()"), 0)

    def test_old_fences_are_read_only_and_wrong_axis_rejected(self):
        self.lua.execute("old=object(world['0:0:0'],'B47_WroughtIronFence_PlainSection','fencing_01_66',false); a=build(0,1,'W'); B47Cohesive.tick()")
        self.assertEqual(self.lua.eval("old.sprite"), "fencing_01_66")
        self.assertIsNone(self.lua.eval("old.data.B47CohesiveIron"))
        self.lua.execute("wrong=object(world['2:2:0'],B47Cohesive.fenceName,'fencing_01_64',false)")
        self.assertIsNone(self.lua.eval("B47Cohesive.readObject(wrong)"))

    def test_gate_state_sprite_and_health_never_rewritten(self):
        self.lua.execute("gate=object(world['0:1:0'],B47Cohesive.gateName,'fixtures_doors_fences_01_22',false); gate.data.B47CohesiveIron={schema=1,axis='W'}; a=build(0,0,'W'); b=build(0,2,'W'); B47Cohesive.recalculate(0,1,0)")
        self.assertEqual(self.lua.eval("gate.sprite"), "fixtures_doors_fences_01_22")
        self.assertEqual(self.lua.eval("gate.health"), 777)

    def test_absent_neighbor_defers_visual_commit(self):
        self.lua.execute("world['-1:0:0']=nil; a=build(0,0,'W')")
        self.assertEqual(self.lua.eval("a.sprite"), "fencing_01_66")
        self.lua.execute("sq=square(-1,0,0); B47Cohesive.loadSquare(sq); B47Cohesive.tick()")
        self.assertEqual(self.lua.eval("a.sprite"), "fencing_01_67")

    def test_q_e_native_intent_and_mouse_retention(self):
        self.lua.execute('''
ISBuildIsoEntity={getSprite=function() return 'other' end,rotateKey=function() end,rotateMouse=function(self) self.nSprite=3 end,onJoypadPressButton=function() end}
Keyboard={KEY_Q=16,KEY_E=18}; KeybindId={ROTATE_BUILDING=1}; Joypad={RBumper=1,LBumper=2}
function getCore() return {isKey=function(self,b,k) return k==19 end} end
''')
        self.lua.execute((OVERLAY / "media/lua/shared/B47_CohesiveCursor.lua").read_text())
        self.lua.execute('''
cursor={nSprite=1,objectInfo={getName=function() return B47Cohesive.fenceName end,getFace=function(self,i) return (i==0 or i==1) and {} or nil end}}
setmetatable(cursor,{__index=ISBuildIsoEntity})
function cursor:getFace() return {getFaceName=function() return self.nSprite==1 and 'W' or 'N' end} end
cursor:rotateKey(Keyboard.KEY_Q); assert(cursor.nSprite==2 and cursor.north)
cursor:rotateMouse(3,3); assert(cursor.nSprite==2)
cursor:rotateKey(Keyboard.KEY_E); assert(cursor.nSprite==1 and cursor.west)
cursor:rotateKey(19); assert(cursor.nSprite==2)
cursor:rotateKey(19); assert(cursor.nSprite==1)
''')

    def test_overlay_localization_and_gate_metadata(self):
        tiles = json.loads((ROOT / "docs/evidence/vanilla_tiles.json").read_text())["tiles"]
        for direction,index in [("W",20),("N",21)]:
            props = tiles[f"fixtures_doors_fences_01_{index}"]
            self.assertIn("door"+direction,props)
            self.assertEqual(props["DoorSound"],"MetalPoleGate")
        files = list((OVERLAY / "media/lua/shared/Translate").glob("*/IG_UI.json"))
        self.assertEqual(len(files),29)
        for p in files:
            values = json.loads(p.read_text())
            self.assertEqual(values["IGUI_B47_WroughtIronFence_PlainSection"],"Wrought Iron Fence")
            self.assertEqual(values["IGUI_B47_WroughtIronGate"],"Wrought Iron Gate")

    def test_menu_window_filter_and_preview_agree_with_authority(self):
        self.lua.execute('''
ISBuildIsoEntity={render=function() end}
ISBuildPanel={}
function info(name)
 local recipe={name=name}
 return {getName=function() return name end,getRecipe=function() return {getCraftRecipe=function() return recipe end} end}
end
infos={info(B47Cohesive.fenceName),info('B47_WroughtIronFence_PostEndedSection'),info('B47_WroughtIronFence_Corner'),info('B47_WroughtIronFence_Post'),info(B47Cohesive.gateName),info('OtherFamily')}
ISBuildIsoEntity.GetAllBuildableEntities=function() return infos end
ISBuildIsoEntity.GetBuildableEntities=function() return infos,'unchanged-items' end
SpriteConfigManager={GetObjectInfo=function(name) for _,i in ipairs(infos) do if i:getName()==name then return i end end end}
ArrayList={new=function() local items={}; local o=list(items); o.add=function(self,v) items[#items+1]=v end; return o end}
ghosts={}
IsoSprite={new=function() return {LoadSingleTexture=function(self,n) self.name=n end,RenderGhostTileColor=function(self,x,y) ghosts[#ghosts+1]={name=self.name,x=x,y=y} end} end}
''')
        self.lua.execute((OVERLAY / "media/lua/client/B47_CohesivePresentation.lua").read_text())
        self.lua.execute('''
assert(#ISBuildIsoEntity.GetAllBuildableEntities()==3)
local available,items=ISBuildIsoEntity.GetBuildableEntities({}); assert(#available==3 and items=='unchanged-items')
local recipes={}; for _,i in ipairs(infos) do recipes[#recipes+1]=i:getRecipe():getCraftRecipe() end
panel={logic={getAllBuildableRecipes=function() return list(recipes) end,setRecipes=function(self,l) self.filtered=l end,getLastSelectedRecipe=function() return nil end},ReselectRecipeOrFirst=function() end}
ISBuildPanel.refreshList(panel); assert(panel.logic.filtered:size()==3)
cursor={objectInfo=infos[1],spriteCache={},north=false,
 ensureSquaresExist=function() end,getSprite=function() end,isValid=function() return true end,renderFloorGrid=function() end}
ISBuildIsoEntity.render(cursor,0,0,0,world['0:0:0'])
assert(ghosts[1].name=='fencing_01_67' and ghosts[2].name=='fencing_01_69')
a=build(0,0,'W'); assert(a.sprite==ghosts[1].name)
''')

    def test_all_overlay_lua_compiles_and_gate_script_balances(self):
        for path in OVERLAY.rglob("*.lua"):
            self.lua.execute("assert(load(...))",path.read_text())
        for path in (OVERLAY / "media/scripts").rglob("*.txt"):
            text=path.read_text()
            self.assertEqual(text.count("{"),text.count("}"))

if __name__ == "__main__": unittest.main()
