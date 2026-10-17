"""Vanilla-recipe exclusion, catalog completeness and authority; offline only."""
import hashlib
import copy
import json
import re
import sys
import unittest
from pathlib import Path
from lupa import LuaRuntime
from test_fences import entities, MOD, ENTITY
from test_variant_selection import definitions, FAKE, LUA
from lua_test_helpers import lua_data

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_tiles import GAME, read_tiles
from generate_expanded_catalog import render, OVERLAY

CATALOG = json.loads((ROOT / 'catalog/vanilla-expansion.json').read_text())
AVAILABILITY = json.loads((ROOT / 'catalog/vanilla-availability.json').read_text())
PARTS = [p for f in CATALOG['families'] for p in f['parts']]


def info_data():
    result = definitions(all_families=True)
    for part in PARTS:
        result[part['name']] = {
            'faces': {d: rows[0][0] for d, rows in part['faces'].items()},
            'inputs': [{'amount': i['amount'], 'names': i['selector'][1:-1].split(';')}
                       for i in part['inputs'] if i['selector'].startswith('[')],
            'time': part['time'], 'perk': part['perk'], 'skill': part['skill'], 'health': part['health'],
        }
    return result


class ExpandedCatalog(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute(FAKE)
        self.lua.execute('loadInfos(' + lua_data(info_data()) + ')')
        for side, name in [('shared', 'B47_ExpandedCatalog'), ('shared', 'B47_CohesiveModel'),
                           ('server', 'B47_CohesiveCursor'), ('client', 'B47_CohesivePresentation')]:
            self.lua.execute((LUA / side / (name + '.lua')).read_text())
        self.lua.execute('startPresentation()')

    def test_generated_files_and_all_language_fallbacks_match_reviewed_data(self):
        files, labels = render(CATALOG, (ROOT / 'VERSION').read_text().strip())
        for relative, text in files.items():
            self.assertEqual((OVERLAY / relative).read_text(), text)
        paths = list((LUA / 'shared/Translate').glob('*/IG_UI.json'))
        self.assertEqual(len(paths), 29)
        for path in paths:
            data = json.loads(path.read_text(encoding='utf-8'))
            for key, label in labels.items():
                self.assertEqual(data[key], label)
            self.assertFalse(set(CATALOG['retired_translation_keys']) & set(data))

    def test_only_fences_and_gates_are_in_scope(self):
        allowed = {'OrnamentalIron','WhitePicket','PostAndWire','ShortChainLink',
                   'MetalPanel','TallChainLink','RazorCoil','RoundPicket',
                   'OrnamentalIronGate','WhitePicketGate','TallWoodGate','FieldGate'}
        self.assertEqual({f['id'] for f in CATALOG['families']}, allowed)
        self.assertEqual(len(PARTS), 25)
        for family in CATALOG['families']:
            self.assertIn(family['kind'], ('fence','gate'))
        actual = {s for p in PARTS for rows in p['faces'].values() for row in rows for s in row}
        self.assertFalse(actual & set(AVAILABILITY['out_of_scope_sprites']))
        self.assertFalse(any(s.startswith('fixtures_railings_') for s in actual))
        self.assertFalse(any(p.get('decorative') for p in PARTS))
        for mutation in ('kind', 'decorative', 'railing'):
            invalid = copy.deepcopy(CATALOG)
            if mutation == 'kind': invalid['families'][0]['kind'] = 'railing'
            elif mutation == 'decorative': invalid['families'][0]['parts'][0]['decorative'] = True
            else: invalid['families'][0]['parts'][0]['faces']['W'] = [['fixtures_railings_01_0']]
            with self.assertRaises(ValueError):
                render(invalid, '1.1.0-dev.14')

    def test_no_added_sprite_already_supplied_by_vanilla_recipe(self):
        vanilla = set(AVAILABILITY['vanilla_supplied_sprites'])
        sprites = {s for p in PARTS for rows in p['faces'].values() for row in rows for s in row}
        self.assertFalse(vanilla & sprites)
        self.assertFalse(set(AVAILABILITY['existing_mod_sprites']) & sprites)
        for proof in AVAILABILITY['vanilla_recipe_sources']:
            path = GAME / proof['path']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), proof['sha256'])
        # Implicit opening sprites of existing double gates are excluded too.
        for base in (64, 80, 96):
            self.assertTrue({f'fixtures_doors_fences_01_{i}' for i in range(base, base+16)} <= vanilla)

    def test_complete_intact_asset_coverage_has_explicit_missing_art_blockers(self):
        actual = read_tiles(GAME / 'media/newtiledefinitions.tiles.txt')
        expected = {n for n in actual if n.startswith(('fencing_01_', 'fixtures_railings_01_', 'fixtures_doors_fences_01_'))}
        self.assertEqual(expected, set(AVAILABILITY['all_intact_sprites']))
        combined = set().union(*(set(AVAILABILITY[k]) for k in
                               ('vanilla_supplied_sprites','existing_mod_sprites','added_sprites',
                                'vanilla_equivalent_sprites','out_of_scope_sprites','blocked_missing_texture')))
        self.assertEqual(combined, expected)
        self.assertEqual(set(AVAILABILITY['blocked_missing_texture']), {f'fencing_01_{i}' for i in range(116,120)})
        self.assertFalse(any('damaged' in n or 'burnt' in n for n in combined))

    def test_recipe_items_exist_and_no_free_parts(self):
        items = set()
        for path in (GAME / 'media/scripts/generated/items').glob('*.txt'):
            items.update('Base.' + n for n in re.findall(r'^\s*item (\w+)\s*$', path.read_text(encoding='utf-8-sig'), re.M))
        for part in PARTS:
            with self.subTest(part=part['name']):
                self.assertGreater(part['skill'], 0)
                self.assertGreater(part['time'], 0)
                self.assertGreater(part['health'], 0)
                self.assertTrue(part['inputs'])
                for entry in part['inputs']:
                    self.assertGreater(entry['amount'], 0)
                    if entry['selector'].startswith('['):
                        self.assertTrue(set(entry['selector'][1:-1].split(';')) <= items, entry)
                self.assertTrue(any('mode:keep' not in i.get('suffix','') for i in part['inputs']))

    def test_every_entity_has_own_real_faces_recipe_and_cost(self):
        blocks = entities(OVERLAY / 'media/scripts/entities/b47_expanded_fences.txt')
        self.assertEqual(set(blocks), {p['name'] for p in PARTS})
        for part in PARTS:
            block = blocks[part['name']]
            self.assertIn('OnCreate = B47ExpandedCatalog.OnCreate,', block)
            self.assertIn('SkillRequired = ' + part['perk'] + ':' + str(part['skill']) + ',', block)
            self.assertIn('time = ' + str(part['time']) + ',', block)
            self.assertEqual(re.findall(r'item (\d+) ([^\n]+),', block),
                             [(str(i['amount']), i['selector'] + i.get('suffix','')) for i in part['inputs']])

    def test_each_family_is_one_menu_entry_and_all_parts_are_reachable_both_ways(self):
        roots = {f['parts'][0]['name'] for f in CATALOG['families']}
        actual = self.lua.eval('ISBuildIsoEntity.GetAllBuildableEntities()')
        names = {i.getName() for i in actual.values()}
        self.assertTrue(roots <= names)
        self.assertEqual(len(names), len(roots)+7)
        for family in CATALOG['families']:
            root = family['parts'][0]['name']
            self.lua.execute('ISEntityBuildMenu.onBuildEntity(player,infos[...])', root)
            expected = [(p['name'], d, rows[0][0]) for p in family['parts']
                        for d, rows in p['faces'].items() if d in ('W','N','E','S')]
            # Native enumeration order W,N,E,S, independent of catalog serialization.
            expected = [(p['name'],d,p['faces'][d][0][0]) for p in family['parts']
                        for d in ('W','N','E','S') if d in p['faces']]
            for name, direction, sprite in expected:
                self.assertEqual(self.lua.eval('drag.objectInfo:getName()'), name)
                self.assertEqual(self.lua.eval('drag:getSprite()'), sprite)
                self.assertEqual(self.lua.eval('drag.buildPanelLogic:getRecipe().name'), name)
                self.lua.execute('drag:rotateKey(Keyboard.KEY_E)')
            self.assertEqual(self.lua.eval('drag.objectInfo:getName()'), root)
            for name, direction, sprite in reversed(expected):
                self.lua.execute('drag:rotateKey(Keyboard.KEY_Q)')
                self.assertEqual(self.lua.eval('drag.objectInfo:getName()'), name)
                self.assertEqual(self.lua.eval('drag:getSprite()'), sprite)

    def test_unaffordable_parts_and_in_progress_actions_keep_native_validation(self):
        for family in CATALOG['families']:
            self.lua.execute('ISEntityBuildMenu.onBuildEntity(player,infos[...])', family['parts'][0]['name'])
            self.lua.execute('drag.buildPanelLogic.allowed=false; assert(not drag:isValid({})); drag.buildPanelLogic.progress=true; previous=drag; drag:rotateKey(Keyboard.KEY_E); assert(drag==previous)')

    def test_new_gates_have_valid_open_or_native_double_door_layouts(self):
        tiles = read_tiles(GAME / 'media/newtiledefinitions.tiles.txt')
        for part in PARTS:
            if not part['gate']: continue
            if 'W_OPEN' in part['faces']:
                self.assertIn('doorW', tiles[part['faces']['W'][0][0]])
                self.assertIn('doorN', tiles[part['faces']['N'][0][0]])
                self.assertEqual(set(part['faces']), {'W','N','W_OPEN','N_OPEN'})
            else:
                self.assertEqual(len(part['faces']['W']), 4)
                self.assertEqual(len(part['faces']['N'][0]), 4)
                for direction, expected in [('W',[4,3,2,1]),('N',[1,2,3,4])]:
                    sprites = [s for row in part['faces'][direction] for s in row]
                    self.assertEqual([int(tiles[s]['DoubleDoor']) for s in sprites], expected)

    def test_server_only_callback_validates_exact_name_sprite_and_orientation(self):
        self.lua.execute('''
client=false; function isClient() return client end
function instanceof(o,k) return o and o.class==k end
SandboxVars={B47ANCEDBuildableFences={ConstructionHealthPercent=200}}
IsoThumpable={GetBreakFurnitureSound=function() return 'native_break' end}
function makeObject(name,sprite,north)
 local o={class='IsoThumpable',name=name,sprite=sprite,north=north,hp=500,writes=0}
 function o:getName() return self.name end
 function o:getNorth() return self.north end
 function o:getSprite() return {getName=function() return self.sprite end} end
 function o:setThumpSound(v) self.sound=v;self.writes=self.writes+1 end
 function o:setBreakSound(v) self.breakSound=v;self.writes=self.writes+1 end
 function o:getMaxHealth() return self.hp end
 function o:setMaxHealth(v) self.hp=v end
 function o:setHealth(v) self.current=v end
 return o
end
''')
        self.lua.execute((LUA / 'server/B47_ExpandedConstruction.lua').read_text())
        for part in PARTS:
            for d, rows in part['faces'].items():
                if d.endswith('_OPEN'):continue
                for sprite in [s for row in rows for s in row]:
                    self.lua.execute('obj=makeObject(...)', part['name'], sprite, d=='N')
                    self.lua.execute('B47ExpandedCatalog.OnCreate({thumpable=obj})')
                    self.assertEqual(self.lua.eval('obj.hp'), 500 if part['post'] else 1000)
                    self.assertEqual(self.lua.eval('obj.breakSound'), 'BreakDoor' if part['gate'] else 'native_break')
                    for mutation in ('client=true', "obj.name='Other'", "obj.sprite='wrong'", 'obj.north=not obj.north', "obj.class='IsoObject'"):
                        self.lua.execute('client=false; obj=makeObject(...)', part['name'], sprite, d=='N')
                        self.lua.execute(mutation + '; B47ExpandedCatalog.OnCreate({thumpable=obj})')
                        self.assertEqual(self.lua.eval('obj.writes'), 0)
        self.lua.execute('client=false; B47ExpandedCatalog.OnCreate(nil); B47ExpandedCatalog.OnCreate({})')
        part = next(p for p in PARTS if not p['post'])
        d, rows = next(iter(part['faces'].items()))
        for config, expected in [('nil',500),('false',500),('0',500),('501',500),('0/0',500),('math.huge',500),('10',50),('500',2500),("'150'",750),('100.9',500)]:
            self.lua.execute('obj=makeObject(...)',part['name'],rows[0][0],d=='N')
            self.lua.execute('SandboxVars.B47ANCEDBuildableFences.ConstructionHealthPercent='+config+'; B47ExpandedCatalog.OnCreate({thumpable=obj})')
            self.assertEqual(self.lua.eval('obj.hp'),expected)


    def test_existing_entity_and_gate_contracts_are_unchanged(self):
        expected = json.loads((ROOT / 'catalog/existing-contracts.json').read_text())
        version = (ROOT / 'VERSION').read_text().strip().encode()
        for relative, sha in expected.items():
            data = (ROOT / relative).read_bytes().replace(version, b'{VERSION}').replace(b'\r\n',b'\n')
            self.assertEqual(hashlib.sha256(data).hexdigest(), sha)
