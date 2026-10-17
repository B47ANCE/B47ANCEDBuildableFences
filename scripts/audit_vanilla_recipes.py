"""Audit installed vanilla construction availability; never modify game files."""
import argparse
import hashlib
import io
import json
import re
from collections import defaultdict
from pathlib import Path
from PIL import Image
from audit_tiles import GAME, read_tiles
from inspect_wrought_sprites import integer, string
from generate_expanded_catalog import validate_vanilla_equivalents

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'catalog/vanilla-recipe-audit.json'
PREFIXES = ('fencing_01_', 'fixtures_doors_fences_01_', 'fixtures_railings_01_')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def uncomment(text):
    pattern = r'"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27|//[^\n]*|/\*.*?\*/'
    return re.sub(pattern, lambda m: '' if m[0].startswith(('//','/*')) else m[0], text, flags=re.S)


def blocks(text, keyword):
    """Balanced script blocks, excluding comments and braces inside strings."""
    text = uncomment(text)
    for match in re.finditer(r'\b' + keyword + r'\s+(\w+)\s*\{', text):
        start = match.end()-1
        depth = 0
        for token in re.finditer(r'"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27|[{}]', text[start:]):
            if token[0] == '{': depth += 1
            elif token[0] == '}': depth -= 1
            if depth == 0:
                yield match[1], text[start:start+token.end()]
                break


def construction_inventory(game):
    definitions = defaultdict(list)
    source_index = []
    upgrades = []
    for path in sorted((game / 'media/scripts').rglob('*.txt')):
        raw = path.read_bytes()
        relative = path.relative_to(game).as_posix()
        proof = {'path':relative, 'sha256':sha(raw)}
        source_index.append(proof)
        text = uncomment(raw.decode('utf-8-sig'))
        module = re.search(r'\bmodule\s+(\w+)\s*\{', text)
        for name, body in blocks(text, 'entity'):
            components = dict(blocks(body, 'component'))
            if 'SpriteConfig' in components or 'CraftRecipe' in components:
                definitions[(module[1] if module else 'UNKNOWN', name)].append((components, proof))
        for name, body in blocks(text, 'multistagebuild'):
            upgrades.append({'name':name, **proof, 'sprites':sorted(set(re.findall(r'\b\w+_\d+\b',body)))})
    records = []
    supplied = defaultdict(set)
    for (module,name), chunks in sorted(definitions.items()):
        components = {}
        for component_map, proof in chunks:
            for key, body in component_map.items():
                components[key] = components.get(key,'') + '\n' + body
        if not {'SpriteConfig','CraftRecipe'} <= components.keys(): continue
        config, recipe = components['SpriteConfig'], components['CraftRecipe']
        sprites = sorted({sprite for row in re.findall(r'(?m)^\s*(?:row|corner)\s*=\s*([^\n]+)',config)
                          for sprite in re.findall(r'\b\w+_\d+\b',row)})
        if not sprites: continue
        entity = module + '.' + name
        records.append({'entity':entity, 'sources':sorted([p for c,p in chunks], key=lambda p:p['path']),
                        'sprites':sprites, 'skill':re.findall(r'SkillRequired\s*=\s*([^,\r\n]+)',recipe),
                        'requires_learning':bool(re.search(r'NeedToBeLearn\s*=\s*true',recipe)),
                        'menu_callbacks':re.findall(r'OnAddToMenu\s*=\s*([^,\s]+)',recipe)})
        for sprite in sprites: supplied[sprite].add(entity)
    for upgrade in upgrades:
        for sprite in upgrade['sprites']: supplied[sprite].add('upgrade:' + upgrade['name'])
    tiles = read_tiles(game / 'media/newtiledefinitions.tiles.txt')
    for sprite, recipes in list(supplied.items()):
        if sprite.startswith('fixtures_doors_fences_01_') and 'DoubleDoor' in tiles.get(sprite,{}):
            base = int(sprite.rsplit('_',1)[1]) // 16 * 16
            for index in range(base,base+16): supplied[f'fixtures_doors_fences_01_{index}'].update(recipes)
    return records, supplied, upgrades, source_index


def art_fingerprints(pack, names):
    """Compare visible RGBA pixels, ignoring transparent atlas padding."""
    fingerprints = {}
    with pack.open('rb') as stream:
        if stream.read(4) != b'PZPK' or integer(stream) != 1: raise ValueError('Unsupported atlas format')
        for _ in range(integer(stream)):
            string(stream)
            count = integer(stream)
            integer(stream)
            selected = []
            for _ in range(count):
                name = string(stream)
                values = [integer(stream) for _ in range(8)]
                if name in names: selected.append((name,values))
            length = integer(stream)
            if not selected:
                stream.seek(length,1)
                continue
            page = Image.open(io.BytesIO(stream.read(length))).convert('RGBA')
            for name,(x,y,w,h,ox,oy,fw,fh) in selected:
                canvas = Image.new('RGBA',(fw,fh))
                canvas.alpha_composite(page.crop((x,y,x+w,y+h)),(ox,oy))
                bbox = canvas.getchannel('A').getbbox()
                if bbox:
                    visible = canvas.crop(bbox)
                    fingerprints[name] = sha(str(visible.size).encode() + visible.tobytes())
    return fingerprints


def part_findings(catalog, supplied, art):
    by_art = defaultdict(list)
    for sprite in supplied:
        if sprite in art: by_art[art[sprite]].append(sprite)
    findings = []
    for family in catalog['families']:
        for part in family['parts']:
            sprites = sorted({s for rows in part['faces'].values() for row in rows for s in row})
            exact, aliases = [], []
            for sprite in sprites:
                if supplied.get(sprite): exact.append({'sprite':sprite,'recipes':sorted(supplied[sprite])})
                for match in sorted(by_art.get(art.get(sprite),[])):
                    if sprite != match:
                        aliases.append({'sprite':sprite,'vanilla_sprite':match,'recipes':sorted(supplied[match])})
            findings.append({'name':part['name'],'family':family['label'],'part':part['label'],
                             'sprites':sprites,'exact_matches':exact,'identical_art_matches':aliases})
    return findings


def audit(game=GAME):
    catalog_path = ROOT / 'catalog/vanilla-expansion.json'
    catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
    validate_vanilla_equivalents(catalog)
    records, supplied, upgrades, script_index = construction_inventory(game)
    by_name = {r['entity']: r for r in records}
    equivalents = []
    for entry in catalog.get('vanilla_equivalent_exclusions', []):
        equivalents.append({**entry, 'native_recipe_proofs':[by_name[name] for name in entry['native_entities']]})
    candidates = {s for f in catalog['families'] for p in f['parts'] for rows in p['faces'].values() for row in rows for s in row}
    pack = game / 'media/texturepacks/Tiles2x.pack'
    art = art_fingerprints(pack, candidates | set(supplied))
    floor_pack = game / 'media/texturepacks/Tiles2x.floor.pack'
    art.update(art_fingerprints(floor_pack, (candidates | set(supplied))-art.keys()))
    lua_index, references = [], []
    for path in sorted((game / 'media/lua').rglob('*.lua')):
        raw = path.read_bytes()
        proof = {'path':path.relative_to(game).as_posix(),'sha256':sha(raw)}
        lua_index.append(proof)
        text = raw.decode('utf-8-sig')
        if any(prefix in text for prefix in PREFIXES):
            kind = 'debug' if '/DebugUIs/' in proof['path'] else 'damage/bending' if path.name in ('BentFences.lua','BrokenFences.lua') else 'REVIEW'
            references.append({**proof,'classification':kind})
    manifest = game.parents[1] / 'appmanifest_108600.acf'
    build = re.search(r'"buildid"\s+"(\d+)"',manifest.read_text())[1]
    focused = [r for r in records if any(t in r['entity'].lower() for t in ('fence','gate','doubledoor','woodstake'))]
    source_paths = ['media/lua/client/BuildingObjects/ISUI/ISBuildMenu.lua',
                    'media/lua/client/BuildingObjects/ISUI/ISInventoryBuildMenu.lua',
                    'media/lua/client/Entity/ISUI/ISEntityBuildMenu.lua',
                    'media/lua/server/BuildingObjects/ISBuildIsoEntity.lua',
                    'media/lua/server/CraftRecipeCode/CraftRecipe_BuildMenu.lua']
    picket_sources = ['media/scripts/generated/entities/outdoors/entity_wood_picket.txt',
                      'media/lua/server/BuildingObjects/PaintingReference.lua',
                      'media/lua/shared/BuildingObjects/TimedActions/ISPaintAction.lua']
    report = {'schema':1,'project_version':(ROOT/'VERSION').read_text().strip(),'steam_build':build,'game_version':'UNKNOWN',
              'runtime_status':'NOT TESTED','catalog_sha256':sha(catalog_path.read_bytes()),
              'script_files_scanned':len(script_index),'script_index_sha256':sha(json.dumps(script_index,sort_keys=True).encode()),
              'lua_files_scanned':len(lua_index),'lua_index_sha256':sha(json.dumps(lua_index,sort_keys=True).encode()),
              'construction_entities':len(records),'vanilla_sprite_identities':len(supplied),
              'tiledefs_sha256':sha((game/'media/newtiledefinitions.tiles.txt').read_bytes()),
              'atlas_sources':[{'path':p.relative_to(game).as_posix(),'sha256':sha(p.read_bytes())} for p in (pack,floor_pack)],
              'candidate_missing_art':sorted(candidates-art.keys()),'native_missing_art':sorted(supplied.keys()-art.keys()),
              'legacy_upgrade_definitions':upgrades,'literal_lua_asset_references':references,
              'build_menu_sources':[{'path':r,'sha256':sha((game/r).read_bytes())} for r in source_paths],
              'reviewed_functional_exclusions':equivalents,
              'white_picket_review':{
                  'sprites':[f'fencing_01_{i}' for i in range(4,8)],
                  'finding':'No construction recipe or paint conversion located for this white picket fence set. WoodPicket constructs a cemetery marker post; white tint is not a picket sprite conversion.',
                  'sources':[{'path':r,'sha256':sha((game/r).read_bytes())} for r in picket_sources]},
              'vanilla_fence_gate_recipes':focused,'parts':part_findings(catalog,supplied,art)}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-root',type=Path,default=GAME)
    parser.add_argument('--write',action='store_true',help='Save metadata-only source audit in catalog/; no runtime or packaging changes')
    args = parser.parse_args()
    report = audit(args.game_root)
    if report['candidate_missing_art'] or any(r['classification']=='REVIEW' for r in report['literal_lua_asset_references']):
        raise ValueError('Unresolved asset/menu evidence; review before claiming no duplicates')
    conflicts = [p['name'] for p in report['parts'] if p['exact_matches'] or p['identical_art_matches']]
    if conflicts: raise ValueError('Vanilla recipe duplicates require review: ' + ', '.join(conflicts))
    if report['native_missing_art']: raise ValueError('Native recipe art incomplete; alias audit cannot be claimed complete')
    text = json.dumps(report,indent=2,ensure_ascii=False) + '\n'
    if args.write: REPORT.write_text(text,encoding='utf-8')
    elif not REPORT.exists() or REPORT.read_text(encoding='utf-8') != text: raise ValueError('Vanilla recipe audit stale; review and --write')
    print(f"PASS: {len(report['parts'])} proposed parts; no exact or identical-art vanilla recipe matches; "
          f"{report['construction_entities']} entities / {report['script_files_scanned']} script files / {report['lua_files_scanned']} Lua files")


if __name__ == '__main__':
    main()
