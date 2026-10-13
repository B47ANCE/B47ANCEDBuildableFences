"""Definition identity and staged Lua loading; no real save/runtime proof."""
import json
import re
import unittest
from lupa import LuaRuntime
from test_fences import BASELINE, ENTITY, MOD, ROOT, SKIN, entities
from test_variant_selection import FAKE, LUA

MAP=ROOT/"compatibility/LegacyFenceMap.json"

class LegacyCompatibilityTests(unittest.TestCase):
    def test_exact_released_identity_map_and_complete_faces(self):
        data=json.loads(MAP.read_text())
        old,new=entities(BASELINE/ENTITY),entities(MOD/ENTITY)
        self.assertEqual(data["legacy_versions"],["1.0.37"])
        self.assertEqual(set(data["entities"]),set(old))
        for name,mapping in data["entities"].items():
            self.assertEqual(mapping["current_entity"],name)
            self.assertEqual(mapping["strategy"],"retain-existing-object")
            faces=dict(re.findall(r"face (\w+)\s*\{\s*layer\s*\{\s*row = (\w+)",old[name]))
            self.assertEqual(mapping["faces"],faces)
            self.assertEqual(faces,dict(re.findall(r"face (\w+)\s*\{\s*layer\s*\{\s*row = (\w+)",new[name])))
            for field in ("health","skillBaseHealth","dontNeedFrame"):
                pattern=rf"\b{field}\s*=\s*([^,\n]+)"
                self.assertEqual(re.findall(pattern,old[name]),re.findall(pattern,new[name]))
            self.assertEqual(re.findall(r"CraftRecipe\s*\{",old[name]),re.findall(r"CraftRecipe\s*\{",new[name]))

    def test_native_assets_ids_and_legacy_ui_definitions_retained(self):
        old_styles=(BASELINE/SKIN).read_text()
        new_styles=(MOD/SKIN).read_text()
        old_ids=set(re.findall(r"entity (ES_B47_\w+)",old_styles))
        self.assertTrue(old_ids.issubset(set(re.findall(r"entity (ES_B47_\w+)",new_styles))))
        self.assertEqual(len(old_ids),17)
        self.assertIn("id=B47ANCEDBuildableFences",(MOD/"mod.info").read_text())
        self.assertFalse(list(BASELINE.rglob("*.tiles")))
        self.assertFalse(list(MOD.rglob("*.tiles")))
        data=json.loads(MAP.read_text())
        self.assertEqual(data["world_mutations"],False)
        self.assertEqual(data["custom_tile_id_remaps"],{})

    def test_client_boot_does_not_require_server_cursor_then_installs_once(self):
        lua=LuaRuntime(unpack_returned_tuples=True)
        lua.execute(FAKE)
        lua.execute((LUA/"shared/B47_CohesiveModel.lua").read_text())
        lua.execute("savedClass=ISBuildIsoEntity; ISBuildIsoEntity=nil; phase='client'; function require(name) assert(phase~='client',name) end")
        lua.execute((LUA/"client/B47_CohesivePresentation.lua").read_text())
        self.assertFalse(lua.eval("B47Cohesive.presentationInstalled or false"))
        lua.execute("phase='server'; ISBuildIsoEntity=savedClass")
        lua.execute((LUA/"server/B47_CohesiveCursor.lua").read_text())
        lua.execute("phase='game'; startPresentation(); firstRender=ISBuildIsoEntity.render; startPresentation(); assert(firstRender==ISBuildIsoEntity.render)")
        self.assertTrue(lua.eval("B47Cohesive.presentationInstalled"))
        self.assertFalse((LUA/"shared/B47_CohesiveCursor.lua").exists())

if __name__=="__main__": unittest.main()
