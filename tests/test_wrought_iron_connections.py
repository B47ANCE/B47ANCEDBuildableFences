"""Execute native corner helpers plus the scoped wrapper; not runtime proof."""
from pathlib import Path
import json
import sys
import unittest
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_tiles import GAME
MODULE = ROOT / 'prototypes/cohesive/42/media/lua/server/B47_WroughtIronConnections.lua'
NATIVE = GAME / 'media/lua/server/BuildingObjects/ISBuildUtil.lua'


class WroughtIronConnections(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute('''
client=false; SandboxVars={B47ANCEDBuildableFences={}}
function isClient() return client end
function require() end
function instanceof(obj,kind) return obj and obj.class==kind end
function list(t) return {size=function() return #t end,get=function(self,i) return t[i+1] end} end
world={}; calls=0; sent=0; created={}
function key(x,y,z) return x..':'..y..':'..z end
function square(x,y,z)
 local s={x=x,y=y,z=z,objects={},special={},wall=false,solid=false,solidTrans=false}
 function s:getObjects() return list(self.objects) end
 function s:getSpecialObjects() return list(self.special) end
 function s:getWallFull() return self.wall end
 function s:isSolid() return self.solid end
 function s:isSolidTrans() return self.solidTrans end
 function s:AddSpecialObject(obj) self.objects[#self.objects+1]=obj; self.special[#self.special+1]=obj end
 function s:RecalcAllWithNeighbours() self.recalculated=true end
 world[key(x,y,z)]=s; return s
end
cell={getGridSquare=function(self,x,y,z) return world[key(x,y,z)] end}
function getCell() return cell end
function section(s,name,sprite,north,kind)
 local o={class=kind or 'IsoThumpable',name=name,sprite=sprite,north=north}
 function o:getName() return self.name end
 function o:getNorth() return self.north end
 function o:getSprite() return {getName=function() return self.sprite end} end
 s.objects[#s.objects+1]=o; s.special[#s.special+1]=o; return o
end
IsoThumpable={new=function(cell,s,sprite,north,item)
 local o={class='IsoThumpable',sprite=sprite,north=north}
 function o:getName() return nil end
 function o:getSprite() return {getName=function() return self.sprite end} end
 function o:setCorner(value) self.corner=value end
 function o:setCanBarricade(value) self.barricade=value end
 function o:setCanBePlastered(value) self.plaster=value end
 function o:transmitCompleteItemToClients() sent=sent+1 end
 created[#created+1]=o; return o
end}
buildUtil={}
''')
        text = NATIVE.read_text()
        self.lua.execute(text[text.index('function buildUtil.checkCorner'):text.index('function buildUtil.addWoodXp')])
        self.lua.execute('native=buildUtil.checkCorner; buildUtil.checkCorner=function(...) calls=calls+1; return native(...) end')
        self.lua.execute(MODULE.read_text())

    def setup_connection(self, north=True, name='B47_WroughtIronFence_PlainSection', neighbor='B47_WroughtIronFence_PostEndedSection'):
        self.lua.globals().north = north
        self.lua.globals().incomingName = name
        self.lua.globals().neighborName = neighbor
        self.lua.execute('''
origin=square(10,10,0)
opposite=square(10+(north and 1 or -1),10+(north and -1 or 1),0)
target=square(10+(north and 1 or 0),10+(north and 0 or 1),0)
local plain=incomingName=='B47_WroughtIronFence_PlainSection'
incoming=section(origin,incomingName,north and (plain and 'fencing_01_65' or 'fencing_01_64') or (plain and 'fencing_01_66' or 'fencing_01_67'),north)
local plainNeighbor=neighborName=='B47_WroughtIronFence_PlainSection'
other=section(opposite,neighborName,not north and (plainNeighbor and 'fencing_01_65' or 'fencing_01_64') or (plainNeighbor and 'fencing_01_66' or 'fencing_01_67'),not north)
action={corner=nil,recipe='unchanged'}
''')

    def call(self):
        self.lua.execute('buildUtil.checkCorner(10,10,0,north,incoming,action)')

    def test_both_placement_orders_create_one_native_replicated_corner(self):
        for north in (True, False):
            for name in ('B47_WroughtIronFence_PlainSection', 'B47_WroughtIronFence_PostEndedSection'):
                for neighbor in ('B47_WroughtIronFence_PlainSection', 'B47_WroughtIronFence_PostEndedSection'):
                    with self.subTest(north=north, name=name, neighbor=neighbor):
                        self.setUp()
                        self.setup_connection(north, name, neighbor)
                        self.call()
                        self.lua.execute("assert(#created==1 and sent==1 and created[1].corner and created[1].sprite=='fencing_01_69'); assert(target.recalculated); assert(action.corner==nil and action.recipe=='unchanged')")
                        self.call()
                        self.assertEqual(self.lua.eval('#created'), 1)

    def test_mixed_families_parallel_wrong_sprite_and_wrong_class_rejected(self):
        for mutation in ("other.name='B47_MilitaryFence_PostEndedSection'", "other.north=north", "other.sprite='fencing_01_65'", "other.class='IsoObject'", "incoming.sprite='fencing_01_69'", "incoming.class='IsoObject'"):
            with self.subTest(mutation=mutation):
                self.setUp(); self.setup_connection(True)
                self.lua.execute(mutation); self.call()
                self.assertEqual(self.lua.eval('#created'), 0)

    def test_paid_post_paid_corner_and_occupied_junction_not_overwritten(self):
        for setup in ("target.wall=true", "target.solid=true", "target.solidTrans=true",
                      "section(target,'B47_WroughtIronFence_Post','fencing_01_69',false)",
                      "section(target,'B47_WroughtIronFence_Corner','fencing_01_68',false)",
                      "section(target,'Other','other_sprite',false)",
                      "section(target,'','fencing_01_69',false,'IsoObject'); target.special={}"):
            with self.subTest(setup=setup):
                self.setUp(); self.setup_connection(); self.lua.execute(setup); self.call()
                self.assertEqual(self.lua.eval('#created'), 0)

    def test_client_disabled_invalid_config_and_missing_squares_never_create(self):
        for setup in ("client=true", "SandboxVars.B47ANCEDBuildableFences.WroughtIronCornerPosts=false",
                      "SandboxVars.B47ANCEDBuildableFences.WroughtIronCornerPosts='true'", "world={}"):
            with self.subTest(setup=setup):
                self.setUp(); self.setup_connection(); self.lua.execute(setup); self.call()
                self.assertEqual(self.lua.eval('#created'), 0)

    def test_default_old_save_enabled_idempotent_install_and_no_repair_scan(self):
        self.setup_connection()
        self.lua.execute('SandboxVars=nil; installed=buildUtil.checkCorner')
        self.lua.execute(MODULE.read_text())
        self.lua.execute('assert(installed==buildUtil.checkCorner)')
        self.call()
        self.assertEqual(self.lua.eval('#created'), 1)
        self.lua.execute('target.objects={}; target.special={}; assert(#created==1)')

    def test_other_builds_keep_original_native_helper(self):
        self.setup_connection()
        self.lua.execute("incoming.name='VanillaFence'; action.corner='vanilla_post'")
        self.call()
        self.lua.execute("assert(calls==1 and created[1].sprite=='vanilla_post')")

    def test_29_sandbox_fallbacks_and_existing_health_option_preserved(self):
        source = ROOT / 'src/B47ANCEDBuildableFences/42/media'
        overlay = ROOT / 'prototypes/cohesive/42/media'
        files = list((overlay / 'lua/shared/Translate').glob('*/Sandbox.json'))
        self.assertEqual(len(files), 29)
        for path in files:
            actual = json.loads(path.read_text())
            previous = json.loads((source / 'lua/shared/Translate' / path.parent.name / 'Sandbox.json').read_text())
            self.assertTrue(actual.pop('Sandbox_B47_WroughtIronCornerPosts'))
            self.assertTrue(actual.pop('Sandbox_B47_WroughtIronCornerPosts_tooltip'))
            self.assertEqual(actual, previous)
        self.assertTrue((overlay / 'sandbox-options.txt').read_text().startswith((source / 'sandbox-options.txt').read_text()))
