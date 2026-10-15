"""Render the reviewed vanilla-art catalog; no game, package or network actions."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / 'prototypes/cohesive/42'


def render(catalog, version):
    entities = ['module Base\n{']
    skins = ['module Base\n{\n    xuiSkin default\n    {']
    model = ["-- B47ANCE'd Buildable Fences v" + version,
             '-- Generated from catalog/vanilla-expansion.json; no world access.',
             'B47ExpandedCatalog={families={},policies={}}', 'local C=B47ExpandedCatalog']
    translations = {}
    for family in catalog['families']:
        if family.get('kind') not in {'fence', 'gate'}:
            raise ValueError('Only fence and gate families belong in this catalog')
        members = []
        for part in family['parts']:
            sprites = [sprite for rows in part['faces'].values() for row in rows for sprite in row]
            if part.get('decorative') or any(sprite.startswith('fixtures_railings_') for sprite in sprites):
                raise ValueError('Railing/decorative components are outside project scope')
            name = part['name']
            members.append('"' + name + '"')
            label = family['label'] + ' - ' + part['label']
            translations['IGUI_' + name] = label
            translations['IGUI_B47_Variant_' + name.rsplit('_', 1)[1]] = part['label']
            entities += ['    entity ' + name, '    {', '        component UiConfig', '        {',
                         '            xuiSkin = default,', '            entityStyle = ES_' + name + ',',
                         '            uiEnabled = false,', '        }', '        component SpriteConfig', '        {',
                         '            OnCreate = B47ExpandedCatalog.OnCreate,',
                         '            health = ' + str(part['health']) + ',',
                         '            skillBaseHealth = ' + str(part['skill_bonus']) + ',',
                         '            dontNeedFrame = true,']
            if not part.get('gate'):
                entities += ['            LogicClass = WoodenWall,']
            orientations = []
            for direction, rows in part['faces'].items():
                entities += ['            face ' + direction, '            {', '                layer', '                {']
                for row in rows:
                    entities += ['                    row = ' + ' '.join(row) + ',']
                    if not direction.endswith('_OPEN'):
                        orientations += [('true' if direction == 'N' else 'false') + ':' + sprite for sprite in row]
                entities += ['                }', '            }']
            entities += ['        }', '        component CraftRecipe', '        {',
                         '            timedAction = ' + part['action'] + ',',
                         '            time = ' + str(part['time']) + ',', '            category = Fences,',
                         '            SkillRequired = ' + part['perk'] + ':' + str(part['skill']) + ',',
                         '            xpAward = ' + part['perk'] + ':' + str(part['skill'] * 10) + ',',
                         '            inputs', '            {']
            for item in part['inputs']:
                entities += ['                item ' + str(item['amount']) + ' ' + item['selector'] + item.get('suffix', '') + ',']
            entities += ['            }', '        }', '    }']
            skins += ['        entity ES_' + name, '        {', '            LuaWindowClass = ISEntityWindow,',
                      '            DisplayName = IGUI_' + name + ',', '            Icon = B47ANCEDBuildableFences_icon,', '        }']
            allowed = ','.join('["' + key + '"]=true' for key in orientations)
            model += ['C.policies["' + name + '"]={material="' + part['material'] + '",post=' + str(part.get('post', False)).lower() + ',gate=' + str(part.get('gate',False)).lower() + ',allowed={' + allowed + '}}']
        model += ['C.families[#C.families+1]={' + ','.join(members) + '}']
    entities += ['}']
    skins += ['    }', '}']
    return {
        'media/scripts/entities/b47_expanded_fences.txt': '\n'.join(entities) + '\n',
        'media/scripts/entities/b47_expanded_fences_skin.txt': '\n'.join(skins) + '\n',
        'media/lua/shared/B47_ExpandedCatalog.lua': '\n'.join(model) + '\n',
    }, translations


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    catalog = json.loads((ROOT / 'catalog/vanilla-expansion.json').read_text(encoding='utf-8'))
    files, labels = render(catalog, (ROOT / 'VERSION').read_text().strip())
    for relative, text in files.items():
        path = OVERLAY / relative
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        elif not path.exists() or path.read_text(encoding='utf-8') != text:
            raise ValueError('Generated catalog drift: ' + relative)
    for path in (OVERLAY / 'media/lua/shared/Translate').glob('*/IG_UI.json'):
        data = json.loads(path.read_text(encoding='utf-8'))
        if args.write:
            for key in catalog.get('retired_translation_keys', []):
                data.pop(key, None)
            data.update(labels)
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        elif any(data.get(key) != value for key, value in labels.items()):
            raise ValueError('Translation fallback drift: ' + path.parent.name)
        elif any(key in data for key in catalog.get('retired_translation_keys', [])):
            raise ValueError('Retired out-of-scope translation remains: ' + path.parent.name)
    print('Catalog generation ' + ('WRITE' if args.write else 'CHECK') + ' PASS')


if __name__ == '__main__':
    main()
