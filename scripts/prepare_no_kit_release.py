"""Build explicitly authorized dev.6 Workshop testing candidate; never upload."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile
from prepare_workshop_metadata import vdf_string

ROOT = Path(__file__).resolve().parents[1]
version = (ROOT / 'VERSION').read_text().strip()
assert version == '1.1.0-dev.6'
item = (ROOT / 'WORKSHOP_ID.txt').read_text().strip()
assert item == '3817174798'
stage = Path.home() / 'Zomboid/Workshop/B47ANCEDBuildableFences'
assert not stage.exists(), 'Archive old staging first'
mod = stage / 'Contents/mods/B47ANCEDBuildableFences'
(mod / 'common').mkdir(parents=True)
source = ROOT / 'src/B47ANCEDBuildableFences/42'
overlay = ROOT / 'prototypes/cohesive/42'
expected = {}
for base in (source, overlay):
    for path in sorted(base.rglob('*')):
        if path.is_file():
            expected['42/' + path.relative_to(base).as_posix()] = path
assert len(expected) == 94
for relative, path in expected.items():
    assert 'FenceTestKit' not in relative
    if path.suffix == '.lua':
        assert 'B47FenceTestKit' not in path.read_text(encoding='utf-8')
    target = mod / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)
shutil.copy2(source / 'poster.png', stage / 'preview.png')
description = (ROOT / 'WORKSHOP_DESCRIPTION.txt').read_text(encoding='utf-8').strip()
note = (ROOT / 'WORKSHOP_CHANGE_NOTE.txt').read_text(encoding='utf-8').strip()
assert 'test kit' not in description.lower()
(stage / 'workshop.txt').write_text('version=1\nid='+item+"\ntitle=B47ANCE'd Buildable Fences\n" +
    ''.join('description='+line+'\n' for line in description.splitlines()), encoding='utf-8')
archive = ROOT / f'dist/current/B47ANCEDBuildableFences-{version}.zip'
assert not archive.exists()
records = []
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as output:
    output.writestr('B47ANCEDBuildableFences/common/', '')
    for relative, path in expected.items():
        output.write(mod / relative, 'B47ANCEDBuildableFences/' + relative)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert hashlib.sha256((mod / relative).read_bytes()).hexdigest() == digest
        records.append({'path': relative, 'sha256': digest})
with zipfile.ZipFile(archive) as output:
    for record in records:
        assert hashlib.sha256(output.read('B47ANCEDBuildableFences/'+record['path'])).hexdigest() == record['sha256']
vdf = stage.parent / f'_steamcmd/B47ANCEDBuildableFences-{version}.vdf'
assert not vdf.exists()
fields = {'appid':'108600', 'publishedfileid':item, 'contentfolder':str(stage/'Contents'),
          'visibility':'0', 'description':description, 'changenote':note}
vdf.write_text('"workshopitem"\n{\n'+''.join(f'    "{key}" "{vdf_string(value)}"\n' for key,value in fields.items())+'}\n',encoding='utf-8')
record = {'version':version, 'publishedfileid':item, 'stage':str(stage), 'vdf':str(vdf),
          'archive':str(archive), 'files':records, 'file_count':len(records),
          'source_stage_zip_parity':'PASS', 'test_kit':'REMOVED', 'upload':'NOT ATTEMPTED',
          'native_SP':'NOT TESTED', 'dedicated_MP':'NOT TESTED', 'stable_G8':'BLOCKED'}
(ROOT/'docs/evidence/workshop-dev6-package.json').write_text(json.dumps(record,indent=2)+'\n')
print('Prepared 94 hash-verified files without test kit:', vdf)
