"""Corrected piece/recipe selector: executed Lua with fake APIs, never PZ proof."""
import json
import re
import unittest
from pathlib import Path
from lupa import LuaRuntime
from test_fences import entities,MOD,ENTITY
from test_fence_testkit import lua_data

ROOT=Path(__file__).resolve().parents[1]
OVERLAY=ROOT/"prototypes/cohesive/42"
LUA=OVERLAY/"media/lua"

def definitions():
    blocks=entities(MOD/ENTITY)
    blocks.update(entities(OVERLAY/"media/scripts/entities/b47_cohesive_gate.txt"))
    result={}
    for name,block in blocks.items():
        if not name.startswith("B47_WroughtIron"): continue
        inputs=[]
        for amount,names in re.findall(r"item (\d+) \[([^]]+)\]",block):
            inputs.append({"amount":int(amount),"names":names.split(";")})
        result[name]={"faces":dict(re.findall(r"face (\w+)\s*\{\s*layer\s*\{\s*row = (\w+)",block)),
          "inputs":inputs,"time":int(re.search(r"time = (\d+)",block)[1]),
          "skill":int(re.search(r"SkillRequired = MetalWelding:(\d+)",block)[1]),
          "health":int(re.search(r"health = (\d+)",block)[1])}
    return result

FAKE='''
function require() end
Events={OnGameStart={Add=function(fn) startPresentation=fn end}}
function isServer() return false end
function getText(key,...) local t={...}; return key..' '..table.concat(t,' / ') end
function getItemNameFromFullType(name) return name end
function list(t) return {size=function() return #t end,get=function(self,i) return t[i+1] end} end
Keyboard={KEY_Q=16,KEY_E=18}; Joypad={RBumper=1,LBumper=2}; KeybindId={ROTATE_BUILDING=1}
function getCore() return {isKey=function(self,b,k) return k==19 end} end
ISBuildMenu={cheat=false}; infos={}; infoList={}
function loadInfos(data)
 for name,d in pairs(data) do
  local faces={}; local idx={W=1,N=0,S=2,E=3}
  for dir,sprite in pairs(d.faces) do
   if idx[dir] then faces[idx[dir]]={getFaceName=function() return dir end,getTileInfo=function() return {getSpriteName=function() return sprite end} end} end
  end
  local inputs={}
  for _,input in ipairs(d.inputs) do
   local options={}; for _,name in ipairs(input.names) do options[#options+1]={getFullName=function() return name end} end
   inputs[#inputs+1]={getPossibleInputItems=function() return list(options) end,getAmount=function() return input.amount end,isKeep=function() return false end}
  end
  local recipe={name=name,time=d.time,health=d.health,getToolBoth=function() end,getToolLeft=function() end,getToolRight=function() end,
   getInputs=function() return list(inputs) end,getRequiredSkillCount=function() return 1 end,
   getRequiredSkill=function() return {getPerk=function() return {getName=function() return 'Welding' end} end,getLevel=function() return d.skill end} end}
  local info={getName=function() return name end,getFace=function(self,i) return faces[i] end,
   getRecipe=function() return {getCraftRecipe=function() return recipe end} end}
  recipe.info=info; infos[name]=info; infoList[#infoList+1]=info
 end
end
SpriteConfigManager={GetObjectInfo=function(n) return infos[n] end}
BuildLogic={new=function()
 return {progress=false,allowed=true,getRecipe=function(self) return self.recipe end,setRecipe=function(self,r) self.recipe=r end,
 getSelectedBuildObject=function(self) return self.recipe.info end,getLastSelectedRecipe=function(self) return self.recipe end,
 getAllBuildableRecipes=function() local r={}; for _,i in ipairs(infoList) do r[#r+1]=i:getRecipe():getCraftRecipe() end; return list(r) end,
 setRecipes=function(self,l) self.list=l end,isCraftActionInProgress=function(self) return self.progress end,
 canPerformCurrentRecipe=function(self) return self.allowed end,updateFloorContainer=function() end,autoPopulateInputs=function() end}
end}
player={getPlayerNum=function() return 0 end,isBuildCheat=function() return false end,getInventory=function() return {getAllTypeEvalRecurse=function() return list({{}}) end} end}
ISInventoryPaneContextMenu={getContainers=function() return {} end}
drag=nil; function getCell() return {setDrag=function(self,c) drag=c end,getDrag=function() return drag end} end
ISBuildIsoEntity={getSprite=function() return 'original' end,rotateKey=function() end,rotateMouse=function(self) self.nSprite=3 end,
 onJoypadPressButton=function() end,isValid=function() return true end,deactivate=function() end,
 render=function(self) rendered=self:getSprite() end}
function ISBuildIsoEntity:new(character,info,nSprite,containers,logic)
 local cursor={character=character,objectInfo=info,nSprite=nSprite,player=0,containers=containers,dragNilAfterPlace=true,blockAfterPlace=false}
 cursor.craftRecipe=info:getRecipe():getCraftRecipe(); cursor.buildPanelLogic=logic or BuildLogic.new()
 cursor.buildPanelLogic:setRecipe(cursor.craftRecipe); cursor.maxTime=cursor.craftRecipe.time
 setmetatable(cursor,{__index=ISBuildIsoEntity})
 return cursor
end
function ISBuildIsoEntity:getFace()
 local idx={1,0,3,2}
 for i=1,4 do local f=self.objectInfo:getFace(idx[self.nSprite]); if f then return f end; self.nSprite=self.nSprite%4+1 end
end
ISBuildIsoEntity.GetAllBuildableEntities=function() return infoList end
ISBuildIsoEntity.GetBuildableEntities=function() return infoList,'items' end
ISEntityBuildMenu={onBuildEntity=function(p,i) drag=ISBuildIsoEntity:new(p,i,1,{}) end,
 createToolTip=function(option) option.onSelect=nil; option.notAvailable=true; return {} end,
 addToolTip=function() return {addToUIManager=function() end,setX=function() end,setY=function() end,setVisible=function() end,removeFromUIManager=function() end} end}
ISBuildPanel={createBuildIsoEntity=function(self,noDrag)
 local info=self.logic:getSelectedBuildObject()
 if not self.buildEntity or self.buildEntity.objectInfo~=info then self.buildEntity=ISBuildIsoEntity:new(player,info,1,{},self.logic) end
 if not noDrag then drag=self.buildEntity end
end}
ArrayList={new=function() local t={}; local l=list(t); l.add=function(self,v) t[#t+1]=v end; return l end}
function getMouseX() return 100 end; function getMouseY() return 100 end
'''

class VariantTests(unittest.TestCase):
    def setUp(self):
        self.lua=LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute(FAKE)
        self.lua.execute("loadInfos("+lua_data(definitions())+")")
        for side,name in [("shared","B47_CohesiveModel"),("server","B47_CohesiveCursor"),("client","B47_CohesivePresentation")]:
            self.lua.execute((LUA/side/(name+".lua")).read_text())
        self.lua.execute("startPresentation()")
        self.lua.execute("ISEntityBuildMenu.onBuildEntity(player,infos['B47_WroughtIronFence_PlainSection'])")

    def test_every_real_piece_face_in_order_and_reverse(self):
        expected=[("PlainSection","fencing_01_66"),("PlainSection","fencing_01_65"),
                  ("PostEndedSection","fencing_01_67"),("PostEndedSection","fencing_01_64"),
                  ("Corner","fencing_01_68"),("Post","fencing_01_69")]
        for suffix,sprite in expected:
            self.assertEqual(self.lua.eval("drag.objectInfo:getName()"),"B47_WroughtIronFence_"+suffix)
            self.assertEqual(self.lua.eval("drag:getSprite()"),sprite)
            self.lua.execute("drag:rotateKey(Keyboard.KEY_E)")
        for suffix,sprite in reversed(expected):
            self.lua.execute("drag:rotateKey(Keyboard.KEY_Q)")
            self.assertEqual(self.lua.eval("drag:getSprite()"),sprite)

    def test_recipe_time_health_cost_skill_follow_selected_entity(self):
        for _ in range(6):
            name=self.lua.eval("drag.objectInfo:getName()")
            d=definitions()[name]
            self.assertEqual(self.lua.eval("drag.maxTime"),d["time"])
            self.assertEqual(self.lua.eval("drag.craftRecipe.health"),d["health"])
            self.assertEqual(self.lua.eval("drag.buildPanelLogic:getRecipe().name"),name)
            text=self.lua.eval("B47Cohesive.description(drag)")
            for i in d["inputs"]:
                self.assertIn(i["names"][0]+": "+str(i["amount"]),text)
            self.assertIn("Welding: 7",text)
            self.lua.execute("drag:rotateKey(Keyboard.KEY_E)")

    def test_action_freeze_and_panel_live_recipe_switch(self):
        self.lua.execute("panel={logic=BuildLogic.new(),ReselectRecipeOrFirst=function() end}; setmetatable(panel,{__index=ISBuildPanel}); panel:refreshList(); assert(panel.logic.list:size()==2); panel.logic:setRecipe(infos['B47_WroughtIronFence_PlainSection']:getRecipe():getCraftRecipe()); panel:createBuildIsoEntity(false)")
        self.lua.execute("drag:rotateKey(Keyboard.KEY_E); drag:rotateKey(Keyboard.KEY_E); assert(panel.logic:getRecipe().name=='B47_WroughtIronFence_PostEndedSection'); assert(drag:getSprite()=='fencing_01_67')")
        self.lua.execute("old=drag; old.buildPanelLogic.progress=true; drag:rotateKey(Keyboard.KEY_E); assert(drag==old and panel.logic:getRecipe().name=='B47_WroughtIronFence_PostEndedSection'); old.buildPanelLogic.progress=false; drag:rotateKey(Keyboard.KEY_Q); assert(drag:getSprite()=='fencing_01_65')")

    def test_preview_native_face_pin_and_per_recipe_validity(self):
        self.lua.execute("drag:rotateKey(Keyboard.KEY_E); drag:rotateKey(Keyboard.KEY_E); drag:rotateMouse(1,1); assert(drag.nSprite==1); drag.nSprite=2; assert(drag:getSprite()=='fencing_01_67'); drag:render(0,0,0,{}); assert(rendered=='fencing_01_67'); drag.buildPanelLogic.allowed=false; assert(not drag:isValid({}))")

    def test_gate_only_closed_placement_faces(self):
        self.lua.execute("ISEntityBuildMenu.onBuildEntity(player,infos['B47_WroughtIronGate'])")
        self.assertEqual(self.lua.eval("drag:getSprite()"),"fixtures_doors_fences_01_20")
        self.lua.execute("drag:rotateKey(Keyboard.KEY_E)")
        self.assertEqual(self.lua.eval("drag:getSprite()"),"fixtures_doors_fences_01_21")
        self.lua.execute("drag:rotateKey(Keyboard.KEY_E)")
        self.assertEqual(self.lua.eval("drag:getSprite()"),"fixtures_doors_fences_01_20")

    def test_menu_single_entry_all_entities_and_no_active_topology(self):
        self.assertEqual(self.lua.eval("#ISBuildIsoEntity.GetAllBuildableEntities()"),2)
        self.assertEqual(len(definitions()),5)
        for p in LUA.rglob("*Cohesive*.lua"):
            self.lua.execute("assert(load(...))",p.read_text())
            for forbidden in ["transmitUpdatedSprite","AddTileObject","OnObjectAboutToBeRemoved","OnDestroyIsoThumpable","LoadGridsquare","getGridSquare","B47CohesiveIronPost"]:
                self.assertNotIn(forbidden,p.read_text(),(p,forbidden))

    def test_all_reachable_axes_match_preserved_tile_metadata(self):
        tiles=json.loads((ROOT/"docs/evidence/vanilla_tiles.json").read_text())["tiles"]
        for d in definitions().values():
            for direction,sprite in d["faces"].items():
                if direction not in ("W","N"): continue
                props=tiles[sprite]
                self.assertTrue("Wall"+direction in props or "Wall"+direction+"Trans" in props or "door"+direction in props)

    def test_complete_variant_localization(self):
        files=list((LUA/"shared/Translate").glob("*/IG_UI.json"))
        self.assertEqual(len(files),29)
        for p in files:
            values=json.loads(p.read_text())
            for suffix in ["PlainSection","PostEndedSection","Corner","Post","WroughtIronGate"]:
                self.assertIn("IGUI_B47_Variant_"+suffix,values)

    def test_family_entry_remains_accessible_for_cheaper_piece(self):
        self.lua.execute("option={onSelect=ISEntityBuildMenu.onBuildEntity}; ISEntityBuildMenu.createToolTip(option,player,infos['B47_WroughtIronFence_PlainSection']); assert(not option.notAvailable and option.onSelect~=nil)")

if __name__=="__main__": unittest.main()
