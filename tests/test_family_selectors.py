"""Executed Lua family/recipe selection using parsed source; offline, not PZ."""
import json
import unittest
from lupa import LuaRuntime
from test_variant_selection import FAKE, LUA, definitions
from lua_test_helpers import lua_data


FAMILIES = [
    ['B47_TallWoodenFence_' + part for part in ('StraightTop', 'StraightTopCorner', 'StraightTopPost')],
    ['B47_TallWoodenFence_' + part for part in ('PostEnded', 'Continuous', 'Corner', 'Post')],
    ['B47_MilitaryFence_' + part for part in ('PlainSection', 'PostEndedSection', 'Corner', 'Post')],
    ['B47_SecurityFence_' + part for part in ('PlainSection', 'PostEndedSection', 'Corner')],
    ['B47_RazorWireSecurityFence_' + part for part in ('PlainSection', 'PostEndedSection', 'Corner')],
    ['B47_WroughtIronFence_' + part for part in ('PlainSection', 'PostEndedSection', 'Corner', 'Post')],
]


class FamilySelectors(unittest.TestCase):
    def setUp(self):
        self.data = definitions(all_families=True)
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute(FAKE)
        self.lua.execute('loadInfos(' + lua_data(self.data) + ')')
        for side, name in [('shared', 'B47_CohesiveModel'), ('server', 'B47_CohesiveCursor'), ('client', 'B47_CohesivePresentation')]:
            self.lua.execute((LUA / side / (name + '.lua')).read_text())
        self.lua.execute('startPresentation()')

    def open(self, name):
        self.lua.execute("ISEntityBuildMenu.onBuildEntity(player,infos[...])", name)

    def test_six_roots_and_gate_in_both_menus_and_build_window(self):
        roots = {family[0] for family in FAMILIES} | {'B47_WroughtIronGate'}
        for query in ['ISBuildIsoEntity.GetAllBuildableEntities()', '(ISBuildIsoEntity.GetBuildableEntities(player))']:
            values = self.lua.eval(query)
            self.assertEqual({info.getName() for info in values.values()}, roots)
        self.lua.execute('panel={logic=BuildLogic.new(),ReselectRecipeOrFirst=function() end}; setmetatable(panel,{__index=ISBuildPanel}); panel:refreshList()')
        self.assertEqual(self.lua.eval('panel.logic.list:size()'), 7)
        self.assertEqual(len(self.data), 22)  # all original entities remain registered

    def test_every_part_face_keeps_own_recipe_time_health_inputs_and_skill(self):
        for family in FAMILIES:
            with self.subTest(family=family[0]):
                self.open(family[0])
                expected = [(name, direction, self.data[name]['faces'][direction])
                            for name in family for direction in ('W', 'N', 'E', 'S')
                            if direction in self.data[name]['faces']]
                for name, direction, sprite in expected:
                    self.assertEqual(self.lua.eval('drag.objectInfo:getName()'), name)
                    self.assertEqual(self.lua.eval('drag:getSprite()'), sprite)
                    self.assertEqual(self.lua.eval('drag.buildPanelLogic:getRecipe().name'), name)
                    self.assertEqual(self.lua.eval('drag.maxTime'), self.data[name]['time'])
                    self.assertEqual(self.lua.eval('drag.craftRecipe.health'), self.data[name]['health'])
                    self.lua.execute('drag:render(0,0,0,{})')
                    text = self.lua.eval('drag.B47Requirements.description')
                    for item in self.data[name]['inputs']:
                        self.assertIn(' / '.join(item['names']) + ': ' + str(item['amount']), text)
                    skill_name = 'Carpentry' if self.data[name]['perk'] == 'Woodwork' else 'Welding'
                    self.assertIn(skill_name + ': ' + str(self.data[name]['skill']), text)
                    self.lua.execute('drag:rotateKey(Keyboard.KEY_E)')
                self.assertEqual(self.lua.eval('drag.objectInfo:getName()'), family[0])
                for name, direction, sprite in reversed(expected):
                    self.lua.execute('drag:rotateKey(Keyboard.KEY_Q)')
                    self.assertEqual(self.lua.eval('drag:getSprite()'), sprite)

    def test_panel_selection_recipe_cost_and_action_freeze_for_each_family(self):
        for family in FAMILIES:
            self.lua.execute("panel={logic=BuildLogic.new()}; setmetatable(panel,{__index=ISBuildPanel}); panel.logic:setRecipe(infos[...]:getRecipe():getCraftRecipe()); panel:createBuildIsoEntity(false)", family[0])
            for _ in range(12):
                name = self.lua.eval('drag.objectInfo:getName()')
                self.assertIn(name, family)
                self.assertEqual(self.lua.eval('panel.logic:getRecipe().name'), name)
                self.lua.execute('old=drag; old.buildPanelLogic.progress=true; drag:rotateKey(Keyboard.KEY_E); assert(drag==old); old.buildPanelLogic.progress=false; drag:rotateKey(Keyboard.KEY_E)')

    def test_family_entry_access_and_unaffordable_selected_part(self):
        for family in FAMILIES:
            self.lua.execute("option={onSelect=ISEntityBuildMenu.onBuildEntity}; ISEntityBuildMenu.createToolTip(option,player,infos[...]); assert(not option.notAvailable and option.onSelect~=nil)", family[0])
            self.open(family[0])
            self.lua.execute('drag.buildPanelLogic.allowed=false; assert(not drag:isValid({})); drag:rotateKey(Keyboard.KEY_E); drag.buildPanelLogic.allowed=false; assert(not drag:isValid({}))')

    def test_affordable_secondary_piece_still_exposes_its_family_root(self):
        for family in FAMILIES:
            self.lua.execute('availableInfos={infos[...]}', family[-1])
            self.lua.execute("local infos,items=ISBuildIsoEntity.GetBuildableEntities(player); assert(#infos==1 and items=='items'); assert(infos[1]:getName()==...)", family[0])

    def test_controller_cycles_within_family_and_missing_info_fails_closed(self):
        for family in FAMILIES:
            self.open(family[0])
            sprite = self.lua.eval('drag:getSprite()')
            self.lua.execute('drag:onJoypadPressButton(0,nil,Joypad.RBumper); drag:onJoypadPressButton(0,nil,Joypad.LBumper)')
            self.assertEqual(self.lua.eval('drag:getSprite()'), sprite)
            self.lua.execute("saved=infos[...]; infos[...]=nil", family[-1], family[-1])
            self.lua.execute('old=drag; drag:rotateKey(Keyboard.KEY_E); assert(drag==old)')
            self.lua.execute('infos[...]=saved', family[-1])

    def test_all_selected_piece_labels_have_language_fallbacks(self):
        suffixes = {name.rsplit('_', 1)[-1] for family in FAMILIES for name in family}
        for path in (LUA / 'shared/Translate').glob('*/IG_UI.json'):
            values = json.loads(path.read_text(encoding='utf-8'))
            for suffix in suffixes:
                self.assertTrue(values['IGUI_B47_Variant_' + suffix])
