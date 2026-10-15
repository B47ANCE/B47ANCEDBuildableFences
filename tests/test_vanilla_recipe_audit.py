"""Independent recipe bindings, aliases and audit freshness; offline only."""
import io
import copy
import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_vanilla_recipes import audit, blocks, construction_inventory, art_fingerprints, part_findings, REPORT
from generate_expanded_catalog import render


class VanillaRecipeAudit(unittest.TestCase):
    def test_balanced_blocks_ignore_comments_and_quoted_braces(self):
        text = '''// entity Fake { component CraftRecipe {} }
        entity Actual { description="brace } remains in string"; /* } */
          component SpriteConfig { face W { layer { row = fencing_01_2, } } }
          component CraftRecipe { time = 100, }
        }'''
        actual = list(blocks(text,'entity'))
        self.assertEqual([name for name,body in actual], ['Actual'])
        self.assertEqual(set(dict(blocks(actual[0][1],'component'))), {'SpriteConfig','CraftRecipe'})

    def test_multi_entity_and_split_component_files_do_not_create_false_bindings(self):
        with tempfile.TemporaryDirectory(prefix='b47-recipe-audit-') as directory:
            game = Path(directory)
            scripts = game/'media/scripts';scripts.mkdir(parents=True)
            (game/'media/newtiledefinitions.tiles.txt').write_text('')
            (scripts/'custom.txt').write_text('''module Base {
              entity Supplied { component SpriteConfig { face W { layer {
                row = fencing_01_2,
              } } } }
              entity Scenery { component SpriteConfig { face W { layer {
                row = fencing_01_4,
              } } } }
            }''')
            (scripts/'separate-recipe.txt').write_text('''module Base {
              entity Supplied { component CraftRecipe { SkillRequired = Woodwork:3, } }
              entity Other { component CraftRecipe { time = 100, } }
            }''')
            records,supplied,upgrades,index = construction_inventory(game)
            self.assertEqual([r['entity'] for r in records],['Base.Supplied'])
            self.assertEqual(set(supplied),{'fencing_01_2'})
            self.assertEqual(len(records[0]['sources']),2)

    def test_legacy_upgrade_art_is_counted_as_vanilla_supplied(self):
        with tempfile.TemporaryDirectory(prefix='b47-upgrade-audit-') as directory:
            game=Path(directory);scripts=game/'media/scripts';scripts.mkdir(parents=True)
            (game/'media/newtiledefinitions.tiles.txt').write_text('')
            (scripts/'upgrades.txt').write_text('''module Base {
              multistagebuild FenceUpgrade { SpriteNorth = fencing_01_1, Sprite = fencing_01_2, }
            }''')
            records,supplied,upgrades,index = construction_inventory(game)
            self.assertEqual(set(supplied),{'fencing_01_1','fencing_01_2'})
            self.assertEqual(upgrades[0]['name'],'FenceUpgrade')

    def test_pixel_alias_is_detected_even_with_a_different_sprite_name(self):
        catalog={'families':[{'label':'Test fence','parts':[{'name':'B47_New','label':'Section','faces':{'W':[['new_sprite']]}}]}]}
        result=part_findings(catalog,{'old_sprite':{'Base.NativeFence'}},{'new_sprite':'identical','old_sprite':'identical'})[0]
        self.assertEqual(result['exact_matches'],[])
        self.assertEqual(result['identical_art_matches'],[{'sprite':'new_sprite','vanilla_sprite':'old_sprite','recipes':['Base.NativeFence']}])
        result=part_findings(catalog,{'new_sprite':{'Base.NativeFence'}},{'new_sprite':'identical'})[0]
        self.assertEqual(result['exact_matches'],[{'sprite':'new_sprite','recipes':['Base.NativeFence']}])

    def test_atlas_art_comparison_ignores_padding_but_keeps_visible_differences(self):
        with tempfile.TemporaryDirectory(prefix='b47-atlas-audit-') as directory:
            page=Image.new('RGBA',(12,4))
            page.paste((200,30,10,255),(0,0,4,4));page.paste((200,30,10,255),(4,0,8,4));page.paste((10,30,200,255),(8,0,12,4))
            png=io.BytesIO();page.save(png,format='PNG')
            integer=lambda v:struct.pack('<i',v)
            def string(v):
                data=v.encode();return integer(len(data))+data
            data=b'PZPK'+integer(1)+integer(1)+string('testpage')+integer(3)+integer(1)
            for name,values in [('candidate',[0,0,4,4,0,0,4,4]),('alias',[4,0,4,4,8,8,16,16]),('different',[8,0,4,4,0,0,4,4])]:
                data+=string(name)+b''.join(integer(v) for v in values)
            data+=integer(len(png.getvalue()))+png.getvalue()
            path=Path(directory)/'test.pack';path.write_bytes(data)
            result=art_fingerprints(path,{'candidate','alias','different'})
            self.assertEqual(result['candidate'],result['alias'])
            self.assertNotEqual(result['candidate'],result['different'])

    def test_installed_audit_matches_report_and_all_proposed_parts_remain_distinct(self):
        current=audit()
        self.assertEqual(current,json.loads(REPORT.read_text(encoding='utf-8')))
        self.assertEqual(len(current['parts']),25)
        self.assertFalse(current['candidate_missing_art'])
        self.assertFalse(current['native_missing_art'])
        self.assertTrue(all(not p['exact_matches'] and not p['identical_art_matches'] for p in current['parts']))
        self.assertTrue(all(r['classification']!='REVIEW' for r in current['literal_lua_asset_references']))

    def test_reviewed_vanilla_duplicates_cannot_return_by_name_or_sprite(self):
        catalog=json.loads((ROOT/'catalog/vanilla-expansion.json').read_text(encoding='utf-8'))
        expected={'B47_LowWood_'+p for p in ('PlainSection','PostEndedSection','Corner','Post')}
        expected.add('B47_TallWoodGate_DoubleGate')
        exclusions=catalog['vanilla_equivalent_exclusions']
        self.assertEqual({n for e in exclusions for n in e['part_names']},expected)
        for entry in exclusions:
            for name in entry['part_names']:
                invalid=copy.deepcopy(catalog)
                invalid['families'][0]['parts'][0]['name']=name
                with self.assertRaisesRegex(ValueError,'functional duplicate'):
                    render(invalid,'1.1.0-dev.15')
            for sprite in entry['sprites']:
                invalid=copy.deepcopy(catalog)
                invalid['families'][0]['parts'][0]['faces']['W']=[[sprite]]
                with self.assertRaisesRegex(ValueError,'functional duplicate'):
                    render(invalid,'1.1.0-dev.15')

    def test_white_picket_marker_and_paint_sources_do_not_build_picket_fence(self):
        from audit_tiles import GAME
        marker=(GAME/'media/scripts/generated/entities/outdoors/entity_wood_picket.txt').read_text(encoding='utf-8-sig')
        paint=(GAME/'media/lua/server/BuildingObjects/PaintingReference.lua').read_text(encoding='utf-8-sig')
        action=(GAME/'media/lua/shared/BuildingObjects/TimedActions/ISPaintAction.lua').read_text(encoding='utf-8-sig')
        self.assertIn('location_community_cemetary_01_31',marker)
        self.assertNotIn('fencing_01_',marker)
        self.assertNotIn('fencing_01_',paint)
        self.assertIn('OtherPainting["crates"]["PaintWhite"]',paint)
        self.assertIn('setCustomColor',action)


if __name__ == '__main__':
    unittest.main()
