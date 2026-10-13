"""Execute kit discovery/authority against current source recipes; offline only."""
import json
import re
import unittest
from pathlib import Path
from lupa import LuaRuntime
from test_fences import entities

ROOT=Path(__file__).resolve().parents[1]
OVERLAY=ROOT/"prototypes/cohesive/42/media/lua"
SOURCE=ROOT/"src/B47ANCEDBuildableFences/42/media/scripts/generated/entities/walls/entity_b47_buildable_fences.txt"
GATE=ROOT/"prototypes/cohesive/42/media/scripts/entities/b47_cohesive_gate.txt"

def current_inputs():
    result={}
    blocks=entities(SOURCE)
    blocks.update(entities(GATE))
    for name,block in blocks.items():
        inputs=[]
        for line in block.splitlines():
            m=re.search(r"item (\d+) (\[[^]]+\]|tags\[[^]]+\])(.*)",line)
            if not m: continue
            names=["Base.Hammer"] if m[2].startswith("tags") else m[2][1:-1].split(";")
            inputs.append({"amount":int(m[1]),"names":names,"keep":"mode:keep" in m[3],"count":"ItemCount" in m[3]})
        result[name]=inputs
    return result

def lua_data(value):
    if isinstance(value,dict): return "{"+",".join("["+json.dumps(k)+"]="+lua_data(v) for k,v in value.items())+"}"
    if isinstance(value,list): return "{"+",".join(lua_data(v) for v in value)+"}"
    if isinstance(value,bool): return str(value).lower()
    return json.dumps(value)

FAKE='''
client=false; server=true; replies={}; inv={}; ground={}; created=0
function isClient() return client end
function isServer() return server end
function require() end
Events={OnClientCommand={Add=function() end}}
Capability={AddItem=1}; ResourceType={Item=1}
function list(t) return {size=function() return #t end,get=function(self,i) return t[i+1] end} end
local capacity={['Base.BlowTorch']=10,['Base.WeldingRods']=20,['Base.BucketConcreteFull']=4,['Base.BucketCarvedConcreteFull']=4}
function instanceItem(name)
 created=created+1
 return {name=name,drain=capacity[name]~=nil,getCurrentUses=function() return capacity[name] or 1 end,
 getScriptItem=function() return {getDisplayCategory=function() return name=='Base.BlowTorch' and 'Tool' or 'Material' end} end}
end
function instanceof(item,kind) return kind=='DrainableComboItem' and item.drain end
function sendServerCommand(player,module,command,args) replies[#replies+1]=args end
function sendAddItemToContainer(container,item) end
function getText(key,count) return key end
local sq={AddWorldInventoryItem=function(self,item,x,y,z) ground[#ground+1]=item.name end}
player={role='admin',capability=true,getSquare=function() return sq end,getInventory=function() return {AddItem=function(self,item) inv[#inv+1]=item.name end} end,
 getRole=function(self) return {getName=function() return self.role end,hasCapability=function() return self.capability end} end}
function makeInfos(data)
 local infos={}
 for name,definitions in pairs(data) do
  local inputs={}
  for _,d in ipairs(definitions) do
   local names={}; for _,name in ipairs(d.names) do names[#names+1]={getFullName=function() return name end} end
   inputs[#inputs+1]={getPossibleInputItems=function() return list(names) end,getAmount=function() return d.amount end,
    getResourceType=function() return ResourceType.Item end,isKeep=function() return d.keep end,isItemCount=function() return d.count end}
  end
  infos[#infos+1]={getName=function() return name end,getRecipe=function() return {getCraftRecipe=function() return {getInputs=function() return list(inputs) end} end} end}
 end
 return list(infos)
end
'''

class KitTests(unittest.TestCase):
    def setUp(self):
        self.lua=LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute(FAKE)
        self.lua.execute("infos=makeInfos("+lua_data(current_inputs())+"); SpriteConfigManager={GetObjectInfoList=function() return infos end}")
        self.lua.execute((OVERLAY/"shared/B47_FenceTestKitPlan.lua").read_text())
        self.lua.execute((OVERLAY/"server/B47_FenceTestKitServer.lua").read_text())

    def test_current_recipe_quantities_and_uses(self):
        self.lua.execute("plan=B47FenceTestKit.plan(infos)")
        inventory=dict(self.lua.eval("plan.inventory").items())
        ground=dict(self.lua.eval("plan.ground").items())
        self.assertEqual(inventory,{"Base.Hammer":1,"Base.WeldingMask":1,"Base.BlowTorch":1})
        self.assertEqual(ground,{"Base.Plank":240,"Base.Nails":288,"Base.MetalPipe":792,
            "Base.ScrapMetal":192,"Base.BarbedWire":72,"Base.BucketCarvedConcreteFull":24,
            "Base.WeldingRods":40,"Base.BlowTorch":79,"Base.Hinge":48,"Base.Doorknob":24})
        self.assertEqual(self.lua.eval("plan.recipes"),22)
        self.assertEqual(self.lua.eval("plan.families"),7)
        self.assertEqual(self.lua.eval("plan.worldCount"),1799)
        self.assertEqual(self.lua.eval("plan.uses['Base.BlowTorch']"),792)
        self.assertEqual(self.lua.eval("plan.uses['Base.BucketCarvedConcreteFull']"),96)

    def test_admin_repeat_current_square_and_no_bulk_inventory(self):
        self.lua.execute("assert(B47FenceTestKit.spawn(player)); assert(B47FenceTestKit.spawn(player))")
        self.assertEqual(self.lua.eval("#inv"),6)
        self.assertEqual(self.lua.eval("#ground"),3598)
        self.assertEqual(self.lua.eval("#replies"),2)

    def test_non_admin_and_admin_without_capability_denied_before_discovery(self):
        for role,cap in [("user",True),("moderator",True),("admin",False)]:
            self.setUp()
            self.lua.execute(f"player.role='{role}'; player.capability={str(cap).lower()}; B47FenceTestKit.onCommand('B47FenceTestKit','b47fencetestkit',player,{{role='admin',item='Base.Concrete',count=999999}})")
            self.assertEqual(self.lua.eval("#inv+#ground+created"),0)
            self.assertEqual(self.lua.eval("replies[1].key"),"IGUI_B47_TestKitDenied")

    def test_payload_ignored_admin_plan_unchanged(self):
        self.lua.execute("B47FenceTestKit.onCommand('B47FenceTestKit','b47fencetestkit',player,{item='Base.Concrete',count=999999,x=9999})")
        self.assertEqual(self.lua.eval("#inv"),3)
        self.assertEqual(self.lua.eval("#ground"),1799)

    def test_sp_allowed_client_refused_and_failed_preflight_no_items(self):
        self.lua.execute("server=false; player.role='user'; assert(B47FenceTestKit.spawn(player))")
        self.assertEqual(self.lua.eval("#ground"),1799)
        self.setUp()
        self.lua.execute("client=true; assert(not B47FenceTestKit.spawn(player))")
        self.assertEqual(self.lua.eval("#ground+#inv"),0)
        self.setUp()
        self.lua.execute("instanceItem=function() return nil end; assert(not B47FenceTestKit.spawn(player))")
        self.assertEqual(self.lua.eval("#ground+#inv"),0)

    def test_recipe_changes_update_plan_and_unresolved_input_fails(self):
        data=current_inputs()
        data["B47_WroughtIronGate"][1]["amount"]=10 # pipes
        self.lua.execute("newInfos=makeInfos("+lua_data(data)+"); plan=B47FenceTestKit.plan(newInfos)")
        self.assertEqual(self.lua.eval("plan.ground['Base.MetalPipe']"),912)
        data["B47_WroughtIronGate"][1]["names"]=[]
        self.lua.execute("infos=makeInfos("+lua_data(data)+"); assert(not B47FenceTestKit.spawn(player))")
        self.assertEqual(self.lua.eval("#ground+#inv"),0)

    def test_chat_exact_command_fallback_and_other_chat_preserved(self):
        self.lua.execute('''
calls=0; originalCalls=0; text='/b47fencetestkit'
ISChat={onCommandEntered=function() originalCalls=originalCalls+1 end}
ISChat.instance={textEntry={getText=function() return text end},logChatCommand=function() end,unfocus=function() end}
function getSpecificPlayer() return player end
function doKeyPress() end
HaloTextHelper={addText=function() end,getColorWhite=function() return {} end}
Events.OnFillWorldObjectContextMenu={Add=function(fn) menu=fn end}
Events.OnServerCommand={Add=function() end}
function sendClientCommand(p,m,c,args) assert(m=='B47FenceTestKit' and c=='b47fencetestkit' and next(args)==nil); calls=calls+1 end
''')
        self.lua.execute((OVERLAY/"client/B47_FenceTestKitClient.lua").read_text())
        self.lua.execute("client=true; ISChat.onCommandEntered(ISChat.instance); assert(calls==1); text='/b47fencetestkit extra'; ISChat.onCommandEntered(ISChat.instance); assert(originalCalls==1)")

if __name__=="__main__": unittest.main()
