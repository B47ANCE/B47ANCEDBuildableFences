"""Offline source-contract and executed Lua regression tests; not PZ proof."""
import hashlib
import json
import re
import unittest
from pathlib import Path
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "src/B47ANCEDBuildableFences/42"
BASELINE = Path(r"E:\Program Files (x86)\Steam\steamapps\workshop\content\108600\3810187215\mods\B47ANCEDBuildableFences\42")
ENTITY = "media/scripts/generated/entities/walls/entity_b47_buildable_fences.txt"
SKIN = "media/scripts/entities/walls/entity_b47_buildable_fences_xuiSkin.txt"


def entities(path):
    text = path.read_text(encoding="utf-8-sig")
    result = {}
    for match in re.finditer(r"    entity (B47_\w+)\s*\{", text):
        start = match.end() - 1
        depth = 0
        for pos in range(start, len(text)):
            depth += (text[pos] == "{") - (text[pos] == "}")
            if depth == 0:
                result[match[1]] = text[match.start():pos+1]
                break
    return result


def normalize(text):
    return re.sub(r"\s+", " ", text).strip()


class SourceContracts(unittest.TestCase):
    def test_installed_baseline_is_untouched(self):
        for record in json.loads((ROOT / "docs/evidence/baseline-1.0.37/hashes.json").read_text(encoding="utf-8-sig")):
            with self.subTest(path=record["Path"]):
                self.assertEqual(hashlib.sha256((BASELINE / record["Path"]).read_bytes()).hexdigest().upper(), record["SHA256"])

    def test_existing_entities_preserved_except_callback_and_six_inputs(self):
        old, new = entities(BASELINE / ENTITY), entities(MOD / ENTITY)
        self.assertEqual(len(old), 17)
        self.assertEqual(len(new), 21)
        for name, before in old.items():
            after = new[name].replace("            OnCreate = B47Fence.OnCreate,\n", "")
            if name.startswith(("B47_SecurityFence_", "B47_RazorWireSecurityFence_")):
                uses, scrap = (2, 3) if name.endswith("_Corner") else (1, 2)
                expected = f"item {uses} [Base.BucketConcreteFull;Base.BucketCarvedConcreteFull] flags[DontRecordInput],"
                self.assertEqual(after.count(expected), 1)
                self.assertNotIn("Base.ScrapMetal", after)
                after = after.replace(expected, f"item {scrap} [Base.ScrapMetal],")
            self.assertEqual(normalize(after), normalize(before), name)

    def test_axes_and_iron_properties(self):
        tiles = json.loads((ROOT / "docs/evidence/vanilla_tiles.json").read_text())["tiles"]
        for name, block in entities(MOD / ENTITY).items():
            for direction, sprite in re.findall(r"face ([WN])\s*\{\s*layer\s*\{\s*row = (\w+)", block):
                props = tiles[sprite]
                self.assertTrue("Wall" + direction in props or "Wall" + direction + "Trans" in props, (name, direction, sprite))
        iron = {"PlainSection": ["fencing_01_66", "fencing_01_65"], "PostEndedSection": ["fencing_01_67", "fencing_01_64"], "Corner": ["fencing_01_68"], "Post": ["fencing_01_69"]}
        for variant, expected in iron.items():
            self.assertEqual(re.findall(r"row = (\w+)", entities(MOD / ENTITY)["B47_WroughtIronFence_" + variant]), expected)
            for sprite in expected:
                self.assertEqual(tiles[sprite]["Material"], "MetalBars")
                if variant != "Post":
                    self.assertEqual(tiles[sprite]["ThumpSound"], "ZombieThumpMetalPoleFence")

    def test_post_conversion_is_only_an_allowlist_extension(self):
        for side in ("client", "server"):
            path = f"media/lua/{side}/B47_NonBlockingPosts_{side.title()}.lua"
            old, new = (BASELINE / path).read_text(), (MOD / path).read_text()
            new = new.replace("v1.1.0-dev.1", "v1.0.37", 1)
            for addition in ['    ["B47_WroughtIronFence_Post"] = true,\n', '    ["fencing_01_69"] = true,\n']:
                self.assertEqual(new.count(addition), 1)
                new = new.replace(addition, "")
            self.assertEqual(new, old)

    def test_localization_styles_icons_and_callback_coverage(self):
        styles = (MOD / SKIN).read_text()
        names = entities(MOD / ENTITY)
        self.assertEqual(set(re.findall(r"entity (ES_B47_\w+)", styles)), {"ES_" + n for n in names})
        keys = set(re.findall(r"DisplayName = (IGUI_B47_\w+)", styles))
        self.assertEqual(len(keys), 21)
        langs = set("AR CA CH CN CS DA DE EN ES ES_CL ES_MX FI FR HU ID IT JP KO NL NO PL PT PTBR RO RU STREW TH TR UA".split())
        folders = MOD / "media/lua/shared/Translate"
        self.assertEqual({p.name for p in folders.iterdir()}, langs)
        for lang in langs:
            values = json.loads((folders / lang / "IG_UI.json").read_text())
            self.assertEqual(set(values), keys)
            self.assertTrue(all(values.values()))
            self.assertEqual(len(json.loads((folders / lang / "Sandbox.json").read_text())), 3)
        for icon in re.findall(r"Icon = (\w+)", styles):
            self.assertTrue((MOD / f"media/textures/{icon}.png").is_file(), icon)
        for name, block in names.items():
            self.assertEqual(block.count("OnCreate = B47Fence.OnCreate,"), 1, name)

    def test_concrete_use_semantics_from_installed_vanilla(self):
        game = Path(r"E:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid")
        items = (game / "media/scripts/generated/items/drainable.txt").read_text()
        for item, bucket in [("BucketConcreteFull", "Bucket"), ("BucketCarvedConcreteFull", "BucketCarved")]:
            block = re.search(r"item " + item + r"\s*\{([^{}]*)\}", items)[1]
            self.assertIn("ItemType = base:drainable,", block)
            self.assertIn("UseDelta = 0.25,", block)
            self.assertIn("ReplaceOnDeplete = Base." + bucket + ",", block)
        self.assertIsNone(re.search(r"item Concrete\s*\{", items))
        for name, block in entities(MOD / ENTITY).items():
            if name.startswith(("B47_SecurityFence_", "B47_RazorWireSecurityFence_")):
                self.assertIn("SkillRequired = MetalWelding:7,", block)
                self.assertNotIn("ItemCount", block)
                self.assertNotIn("mode:destroy", block)
                amount = 7 if name.endswith("_Corner") else 5
                for item in ("BlowTorch", "MetalPipe", "WeldingRods"):
                    self.assertIn(f"item {amount} [Base.{item}]", block)
                if "Razor" in name:
                    wire = 3 if name.endswith("_Corner") else 2
                    self.assertIn(f"item {wire} [Base.BarbedWire]", block)

    def test_balanced_script_braces(self):
        for path in (MOD / "media/scripts").rglob("*.txt"):
            text = re.sub(r"/\*.*?\*/|//[^\n]*", "", path.read_text(), flags=re.S)
            depth = 0
            for char in text:
                depth += (char == "{") - (char == "}")
                self.assertGreaterEqual(depth, 0, path)
            self.assertEqual(depth, 0, path)


class LuaAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute('''
            client = false
            function isClient() return client end
            function instanceof(obj, cls) return obj.class == cls end
            SandboxVars = { B47ANCEDBuildableFences = { ConstructionHealthPercent = 100 } }
            IsoThumpable = { GetBreakFurnitureSound = function(sprite) return "BreakFurnitureMetal" end }
            function makeObject(name, spriteName, class)
                local obj = { name=name, spriteName=spriteName, class=class or "IsoThumpable", health=2500, maxHealth=2500, writes=0 }
                function obj:getName() return self.name end
                function obj:getSprite() return {getName=function() return self.spriteName end} end
                function obj:getMaxHealth() return self.maxHealth end
                function obj:setThumpSound(value) self.thump=value; self.writes=self.writes+1 end
                function obj:setBreakSound(value) self.breakSound=value; self.writes=self.writes+1 end
                function obj:setMaxHealth(value) self.maxHealth=value; self.writes=self.writes+1 end
                function obj:setHealth(value) self.health=value; self.writes=self.writes+1 end
                return obj
            end
        ''')
        self.lua.execute((MOD / "media/lua/server/B47_FenceConstruction.lua").read_text())

    def call(self, name="B47_MilitaryFence_PlainSection", sprite="fencing_01_50", cls="IsoThumpable"):
        obj = self.lua.globals().makeObject(name, sprite, cls)
        result = self.lua.globals().B47Fence.OnCreate(self.lua.table_from({"thumpable": obj}))
        self.assertIsNone(result, "Nil return preserves native single transmission")
        return obj

    def test_material_and_default_health(self):
        cases = [("B47_MilitaryFence_PlainSection", "fencing_01_50", "ZombieThumpChainlinkFence"),
                 ("B47_SecurityFence_Corner", "fencing_01_84", "ZombieThumpChainlinkFence"),
                 ("B47_RazorWireSecurityFence_PlainSection", "fencing_01_90", "ZombieThumpChainlinkFence"),
                 ("B47_WroughtIronFence_PlainSection", "fencing_01_66", "ZombieThumpMetalPoleFence"),
                 ("B47_TallWoodenFence_Corner", "fencing_01_12", "ZombieThumpWood")]
        for name, sprite, expected in cases:
            obj = self.call(name, sprite)
            self.assertEqual(obj.thump, expected)
            self.assertEqual(obj.health, 2500)
            self.assertEqual(obj.maxHealth, 2500)
            self.assertEqual(obj.writes, 2)
            self.assertEqual(obj.breakSound, "ZombieThumpWoodCollapse" if "Wooden" in name else "BreakFurnitureMetal")

    def test_client_and_invalid_objects_cannot_mutate(self):
        self.lua.globals().client = True
        self.assertEqual(self.call().writes, 0)
        self.lua.globals().client = False
        for name, sprite, cls in [("OtherMod", "fencing_01_50", "IsoThumpable"), ("B47_MilitaryFence_PlainSection", "fencing_01_84", "IsoThumpable"), ("B47_MilitaryFence_PlainSection", "fencing_01_50", "IsoObject")]:
            self.assertEqual(self.call(name, sprite, cls).writes, 0)
        self.lua.globals().B47Fence.OnCreate(None)

    def test_authority_sandbox_bounds_and_posts(self):
        options = self.lua.globals().SandboxVars.B47ANCEDBuildableFences
        for percent, expected in [(10, 250), (200, 5000), (500, 12500), (0, 2500), (501, 2500), ("bad", 2500), (float("nan"), 2500), (float("inf"), 2500)]:
            options.ConstructionHealthPercent = percent
            self.assertEqual(self.call().maxHealth, expected)
        options.ConstructionHealthPercent = 200
        for name, sprite in [("B47_TallWoodenFence_Post", "fencing_01_13"), ("B47_TallWoodenFence_StraightTopPost", "fencing_01_74"), ("B47_MilitaryFence_Post", "fencing_01_53"), ("B47_WroughtIronFence_Post", "fencing_01_69")]:
            self.assertEqual(self.call(name, sprite).maxHealth, 2500)

    def test_lua_syntax_all_runtime_files(self):
        compiler = self.lua.eval("function(source) local chunk, err = load(source); assert(chunk, err); return true end")
        for path in MOD.rglob("*.lua"):
            self.assertTrue(compiler(path.read_text()), path)


class PostAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute('''
            function isClient() return false end
            function isServer() return true end
            function instanceof(obj, cls) return obj.class == cls end
            Events = { OnClientCommand = { Add = function(fn) handler = fn end } }
            operations = {}
            local player = { getX=function() return 100 end, getY=function() return 100 end, getZ=function() return 0 end }
            sender = player
            square = { x=100, y=100, z=0, objects={} }
            function square:getObjects()
                return { size=function() return #self.objects end, get=function(_, i) return self.objects[i+1] end }
            end
            function square:transmitRemoveItemFromSquare(obj)
                table.insert(operations, "remove")
                for i, v in ipairs(self.objects) do if v == obj then table.remove(self.objects, i); break end end
            end
            function square:AddTileObject(obj) table.insert(operations, "add"); table.insert(self.objects, obj) end
            function getCell() return { getGridSquare=function(_, x,y,z) if x==100 and y==100 and z==0 then return square end end } end
            IsoObject = { new=function(sq, sprite)
                table.insert(operations, "new")
                return {class="IsoObject", sprite=sprite, transmitCompleteItemToClients=function() table.insert(operations, "replicate") end}
            end }
            function addPost(name, sprite, class)
                local obj = {name=name, sprite=sprite, class=class or "IsoThumpable"}
                function obj:getName() return self.name end
                function obj:getSprite() return {getName=function() return self.sprite end} end
                function obj:getSquare() return square end
                table.insert(square.objects, obj)
                return obj
            end
        ''')
        self.lua.execute((MOD / "media/lua/server/B47_NonBlockingPosts_Server.lua").read_text())

    def request(self, **overrides):
        args = {"x": 100, "y": 100, "z": 0, "name": "B47_WroughtIronFence_Post", "sprite": "fencing_01_69"}
        args.update(overrides)
        self.lua.globals().handler("B47ANCEDBuildableFences", "ReplacePost", self.lua.globals().sender, self.lua.table_from(args))

    def test_iron_replacement_sequence_and_duplicate_request(self):
        self.lua.globals().addPost("B47_WroughtIronFence_Post", "fencing_01_69", "IsoThumpable")
        self.request()
        self.assertEqual(list(self.lua.globals().operations.values()), ["remove", "new", "add", "replicate"])
        self.assertEqual(self.lua.globals().square.objects[1].sprite, "fencing_01_69")
        self.request()
        self.assertEqual(len(self.lua.globals().operations), 4)
        self.assertEqual(len(self.lua.globals().square.objects), 1)

    def test_distant_invalid_name_sprite_class_and_sender_rejected(self):
        self.lua.globals().addPost("B47_WroughtIronFence_Post", "fencing_01_69", "IsoThumpable")
        for overrides in [{"x": 120}, {"z": 1}, {"name": "Other"}, {"sprite": "fencing_01_68"}, {"x": "invalid"}]:
            self.request(**overrides)
            self.assertEqual(len(self.lua.globals().operations), 0)
        self.lua.globals().handler("B47ANCEDBuildableFences", "ReplacePost", None, self.lua.table_from({"x":100,"y":100,"z":0}))
        self.assertEqual(len(self.lua.globals().operations), 0)
        self.lua.globals().square.objects[1]["class"] = "IsoObject"
        self.request()
        self.assertEqual(len(self.lua.globals().operations), 0)

    def test_mp_detector_submits_intent_without_local_mutation(self):
        self.lua.execute('''
            function isClient() return true end
            Events.OnPlayerUpdate = { Add = function(fn) scan = fn end }
            function getPlayer() return sender end
            function square:getX() return self.x end
            function square:getY() return self.y end
            function square:getZ() return self.z end
            commands = {}
            function sendClientCommand(module, command, args)
                table.insert(commands, {module=module, command=command, args=args})
            end
        ''')
        self.lua.globals().addPost("B47_WroughtIronFence_Post", "fencing_01_69", "IsoThumpable")
        self.lua.execute((MOD / "media/lua/client/B47_NonBlockingPosts_Client.lua").read_text())
        for _ in range(60):
            self.lua.globals().scan(self.lua.globals().sender)
        self.assertEqual(len(self.lua.globals().commands), 1)
        command = self.lua.globals().commands[1]
        self.assertEqual(command.module, "B47ANCEDBuildableFences")
        self.assertEqual(command.command, "ReplacePost")
        self.assertEqual(command.args.sprite, "fencing_01_69")
        self.assertEqual(len(self.lua.globals().operations), 0)
        self.assertEqual(self.lua.globals().square.objects[1]["class"], "IsoThumpable")


if __name__ == "__main__":
    unittest.main(verbosity=2)
