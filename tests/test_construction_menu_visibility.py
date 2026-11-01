"""All mod recipe routes and partial native lists; offline Lua, not PZ runtime."""
import json
import re
import unittest
from pathlib import Path
import test_expanded_catalog as catalog_fixture
from lua_test_helpers import lua_data
from prepare_workshop import runtime_files
from audit_vanilla_recipes import blocks

ROOT = Path(__file__).resolve().parents[1]


class ConstructionMenuVisibility(unittest.TestCase):
    def setUp(self):
        harness = catalog_fixture.ExpandedCatalog()
        harness.setUp()
        self.lua = harness.lua
        families = self.lua.eval('B47Cohesive.families')
        self.groups = [[families[i][j] for j in range(1, len(families[i])+1)]
                       for i in range(1, len(families)+1)]
        self.groups.append([self.lua.eval('B47Cohesive.gateName')])
        self.names = [name for group in self.groups for name in group]
        self.lua.execute('''
foreignRecipe={name='Base.UnrelatedVanillaRecipe'}
function nativePanel(names)
 local recipes={}
 for _,name in ipairs(names) do
  recipes[#recipes+1]=name==foreignRecipe.name and foreignRecipe or infos[name]:getRecipe():getCraftRecipe()
 end
 panel={logic=BuildLogic.new(),ReselectRecipeOrFirst=function() end}
 panel.logic.getAllBuildableRecipes=function() return list(recipes) end
 setmetatable(panel,{__index=ISBuildPanel})
 panel:refreshList()
end
function visibleRecipeNames()
 local result={}
 for i=0,panel.logic.list:size()-1 do result[#result+1]=panel.logic.list:get(i).name end
 return result
end
''')

    def visible(self, names):
        self.lua.execute('nativePanel(' + lua_data(names) + ')')
        result = self.lua.eval('visibleRecipeNames()')
        return [result[i] for i in range(1, len(result)+1)]

    def test_all_47_recipe_components_styles_and_29_language_bindings_are_valid(self):
        files = runtime_files()
        entities, styles = {}, {}
        for name, path in files.items():
            if not name.startswith('media/scripts/') or path.suffix != '.txt':
                continue
            for entity, body in blocks(path.read_text(encoding='utf-8-sig'), 'entity'):
                if entity.startswith('B47_'):
                    self.assertNotIn(entity, entities)
                    entities[entity] = body
                elif entity.startswith('ES_B47_'):
                    self.assertNotIn(entity, styles)
                    styles[entity] = body
        self.assertEqual(len(self.names), 47)
        self.assertEqual(len(set(self.names)), 47)
        self.assertEqual(set(entities), set(self.names))
        translations = [json.loads(p.read_text(encoding='utf-8')) for n, p in files.items()
                        if re.fullmatch(r'media/lua/shared/Translate/[^/]+/IG_UI.json', n)]
        self.assertEqual(len(translations), 29)
        for name, body in entities.items():
            with self.subTest(recipe=name):
                components = dict(blocks(body, 'component'))
                self.assertTrue({'UiConfig','CraftRecipe','SpriteConfig'} <= components.keys())
                recipe = components['CraftRecipe']
                self.assertEqual(re.findall(r'category\s*=\s*(\w+)', recipe), ['Fences'])
                self.assertNotRegex(recipe, r'NeedToBeLearn\s*=\s*true')
                self.assertNotIn('OnAddToMenu', recipe)
                self.assertRegex(recipe, r'SkillRequired\s*=\s*(?:Woodwork|MetalWelding):\d+')
                self.assertRegex(recipe, r'item\s+[1-9]')
                style = re.search(r'entityStyle\s*=\s*(\w+)', components['UiConfig'])[1]
                key = re.search(r'DisplayName\s*=\s*(\w+)', styles[style])[1]
                for language in translations:
                    self.assertTrue(language.get(key), key)

    def test_full_catalog_has_19_grouped_entries_and_every_gate_is_reachable(self):
        self.assertEqual(len(self.groups), 19)
        self.assertEqual(set(self.visible(self.names)), {group[0] for group in self.groups})
        reached = set()
        for group in self.groups:
            self.lua.execute("panel.logic:setRecipe(infos[...]:getRecipe():getCraftRecipe()); panel:createBuildIsoEntity(false)", group[0])
            states = self.lua.eval('B47Cohesive.states(...)', group[0])
            for _ in range(len(states)):
                name = self.lua.eval('drag.objectInfo:getName()')
                reached.add(name)
                self.assertEqual(self.lua.eval('panel.logic:getRecipe().name'), name)
                self.assertEqual(self.lua.eval('drag.maxTime'), catalog_fixture.info_data()[name]['time'])
                self.lua.execute('drag:rotateKey(Keyboard.KEY_E)')
            self.assertEqual(self.lua.eval('drag.objectInfo:getName()'), group[0])
        self.assertEqual(reached, set(self.names))
        self.assertEqual(len([name for name in reached if 'Gate' in name]), 6)

    def test_each_recipe_alone_keeps_its_family_available(self):
        for name in self.names:
            with self.subTest(recipe=name):
                self.assertEqual(self.visible([name]), [name])
                self.lua.execute('panel.logic:setRecipe(panel.logic.list:get(0)); panel:createBuildIsoEntity(false)')
                self.assertEqual(self.lua.eval('drag.objectInfo:getName()'), name)

    def test_secondary_only_lists_use_an_existing_recipe_in_native_order(self):
        for group in self.groups:
            if len(group) < 2:
                continue
            supplied = list(reversed(group[1:]))
            self.assertEqual(self.visible(supplied), [supplied[0]])

    def test_root_is_preferred_without_touching_unrelated_native_recipes(self):
        foreign = 'Base.UnrelatedVanillaRecipe'
        for group in self.groups:
            if len(group) < 2:
                continue
            self.assertEqual(self.visible([foreign,group[-1],group[0],foreign]),
                             [foreign,group[0],foreign])

    def test_missing_root_info_keeps_a_valid_secondary_entry(self):
        for group in self.groups:
            if len(group) < 2:
                continue
            self.lua.execute('savedRoot=infos[...]; infos[...]=nil',group[0],group[0])
            self.assertEqual(self.visible([group[-1]]), [group[-1]])
            self.lua.execute('infos[...]=savedRoot', group[0])

    def test_empty_native_list_does_not_inject_recipes(self):
        self.assertEqual(self.visible([]), [])


if __name__ == '__main__':
    unittest.main()
