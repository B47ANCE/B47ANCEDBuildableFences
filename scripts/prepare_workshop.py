"""Prepare a clean, unpublished Workshop candidate from committed source."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import zipfile

from prepare_workshop_metadata import vdf_string

ROOT = Path(__file__).resolve().parents[1]
MOD = 'B47ANCEDBuildableFences'
SOURCES = ('src/' + MOD + '/42', 'prototypes/cohesive/42')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def runtime_files(root=ROOT):
    """Compose established sources; only translation overrides are intentional."""
    result = {}
    for source in SOURCES:
        for path in sorted((root / source).rglob('*')):
            if not path.is_file():
                continue
            if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                raise ValueError('Linked/escaping source: ' + str(path))
            relative = path.relative_to(root / source).as_posix()
            if relative in result and relative != 'media/sandbox-options.txt' and not re.fullmatch(r'media/lua/shared/Translate/[^/]+/(IG_UI|Sandbox)\.json', relative):
                raise ValueError('Unexpected source override: ' + relative)
            result[relative] = path
    if not result or len(result) != len({name.casefold() for name in result}):
        raise ValueError('Empty payload or case-colliding paths')
    for name, path in result.items():
        if path.suffix.lower() not in {'.lua', '.json', '.txt', '.info', '.png'}:
            raise ValueError('Unexpected runtime file: ' + name)
        if any(part.lower() in {'tests', 'research', '__pycache__'} for part in path.relative_to(root).parts):
            raise ValueError('Development content in payload: ' + name)
        if path.suffix == '.lua':
            text = path.read_text(encoding='utf-8')
            if re.search(r'B47FenceTestKit|b47fencetestkit|V\.description\s*=|\bprint\s*\(', text):
                raise ValueError('Runtime test/debug hook: ' + name)
    modules = {re.sub(r'^media/lua/(shared|client|server)/', '', name)[:-4]
               for name in result if name.endswith('.lua')}
    for name, path in result.items():
        if path.suffix == '.lua':
            for module in re.findall(r'require\s*[\(]?\s*["\']([^"\']+)', path.read_text(encoding='utf-8')):
                if module.startswith('B47_') and module not in modules:
                    raise ValueError('Missing/case-incorrect mod require: ' + module)
    return result


def verify_zip(path, expected):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or len(names) != len({name.casefold() for name in names}):
            raise ValueError('Duplicate/case-colliding ZIP entries')
        for name in names:
            normalized = name.replace('\\', '/')
            if normalized.startswith('/') or ':' in normalized or '..' in PurePosixPath(normalized).parts:
                raise ValueError('Unsafe ZIP member')
        if archive.testzip() is not None:
            raise ValueError('ZIP CRC/data failure')
        if set(names) != set(expected) | {MOD + '/common/'}:
            raise ValueError('Unexpected/missing archive files')
        for name, data in expected.items():
            if archive.read(name) != data:
                raise ValueError('Source/archive mismatch: ' + name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true', help='Write a candidate under ignored dist/; never upload')
    args = parser.parse_args()
    files = runtime_files()
    if not args.prepare:
        print(f'PASS: {len(files)} runtime files; no shipped tests, diagnostics or custom Java/JAR')
        return
    version = (ROOT / 'VERSION').read_text().strip()
    item = (ROOT / 'WORKSHOP_ID.txt').read_text().strip()
    if not item.isdigit() or len(item) < 7:
        raise ValueError('Existing Workshop ID required')
    commit = git('rev-parse', 'HEAD')
    if commit != git('rev-parse', '@{upstream}'):
        raise ValueError('Push and verify the source commit before preparation')
    if git('status', '--porcelain', '--', 'VERSION', 'version-inventory.json', 'WORKSHOP_ID.txt',
           'WORKSHOP_DESCRIPTION.txt', 'WORKSHOP_CHANGE_NOTE.txt', 'scripts/prepare_workshop.py', *SOURCES):
        raise ValueError('Uncommitted release inputs; commit intended changes first')
    tracked = set(git('ls-files').splitlines())
    if any(path.relative_to(ROOT).as_posix() not in tracked for path in files.values()):
        raise ValueError('Untracked source in payload')
    description = (ROOT / 'WORKSHOP_DESCRIPTION.txt').read_text(encoding='utf-8').strip()
    note = (ROOT / 'WORKSHOP_CHANGE_NOTE.txt').read_text(encoding='utf-8').strip()
    if not all(text.startswith('[b]Version ' + version + '[/b]') for text in (description, note)):
        raise ValueError('Workshop prose version mismatch')
    if '\\n' in description or '\\n' in note or len(description.encode()) > 8000:
        raise ValueError('Invalid Workshop prose formatting/size')
    info = files['mod.info'].read_text(encoding='utf-8')
    if not re.search(r'^id=' + MOD + r'\r?$', info, re.M) or not re.search(r'^modversion=' + re.escape(version) + r'\r?$', info, re.M):
        raise ValueError('Runtime metadata mismatch')
    names = re.findall(r'^name=([^\r\n]+)\r?$', info, re.M)
    if len(names) != 1 or not names[0].strip():
        raise ValueError('One nonempty mod display name required')
    title = names[0].strip()
    subprocess.run([sys.executable, str(ROOT / 'scripts/check_versions.py'), '--root', str(ROOT)], check=True)
    stage = ROOT / 'dist/workshop-candidates' / version
    inventory = json.loads((ROOT / 'version-inventory.json').read_text())
    package_directory = Path(inventory['packaging']['artifacts'][0]['glob']).parent
    if package_directory.is_absolute() or '..' in package_directory.parts:
        raise ValueError('Unsafe package output directory')
    package = ROOT / package_directory / (MOD + '-' + version + '.zip')
    if stage.exists() or package.exists():
        raise ValueError('Candidate already exists; preserve prior output')
    payload = {MOD + '/42/' + name: path.read_bytes() for name, path in files.items()}
    stage.mkdir(parents=True)
    package.parent.mkdir(parents=True, exist_ok=True)
    (stage / 'Contents/mods' / MOD / 'common').mkdir(parents=True)
    for name, data in payload.items():
        target = stage / 'Contents/mods' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (stage / 'preview.png').write_bytes(files['poster.png'].read_bytes())
    (stage / 'workshop.txt').write_text('version=1\nid=' + item + '\ntitle=' + title + '\n' +
        ''.join('description=' + line + '\n' for line in description.splitlines()), encoding='utf-8')
    with zipfile.ZipFile(package, 'x', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(MOD + '/common/', '')
        for name, data in payload.items():
            archive.writestr(name, data)
    verify_zip(package, payload)
    for name, data in payload.items():
        if (stage / 'Contents/mods' / name).read_bytes() != data:
            raise ValueError('Stage/source mismatch: ' + name)
    fields = {'appid': '108600', 'publishedfileid': item, 'contentfolder': str(stage / 'Contents'),
              'title': title, 'description': description, 'changenote': note}
    # Title follows the reviewed mod.info name; preserve preview and visibility.
    (stage / 'upload.vdf').write_text('"workshopitem"\n{\n' + ''.join(
        '    "' + key + '" "' + vdf_string(value) + '"\n' for key, value in fields.items()) + '}\n', encoding='utf-8')
    manifest = {'version': version, 'commit': commit, 'mod_id': MOD, 'workshop_id': item,
        'display_name': title, 'appid': 108600, 'game_minimum': '42.0', 'exact_runtime_build': 'UNKNOWN / NOT TESTED',
        'publish_ready': False, 'G6_SP': 'NOT TESTED', 'G7_dedicated_MP': 'BLOCKED / NOT TESTED',
        'G8_release': 'BLOCKED', 'package_sha256': hashlib.sha256(package.read_bytes()).hexdigest(),
        'files': [{'path': name, 'sha256': hashlib.sha256(data).hexdigest()} for name, data in payload.items()]}
    (stage / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    subprocess.run([sys.executable, str(ROOT / 'scripts/check_versions.py'), '--root', str(ROOT), '--release'], check=True)
    print('PREPARED, NOT PUBLISHED:', stage)
    print('PACKAGE:', package)
    print('G6/G7 NOT TESTED; stable G8 BLOCKED')


if __name__ == '__main__':
    main()
