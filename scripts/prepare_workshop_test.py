"""Explicitly authorized untested test package; no upload or native test claims."""
import hashlib
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
version=(ROOT/"VERSION").read_text().strip()
assert version=="1.1.0-dev.5"
modid="B47ANCEDBuildableFences"
item=(ROOT/"WORKSHOP_ID.txt").read_text().strip()
assert item.isdigit() and len(item)>=7
source=ROOT/"src"/modid/"42"
overlay=ROOT/"prototypes/cohesive/42"
stage=Path(r"C:\Users\willi\Zomboid\Workshop")/modid
assert not stage.exists(), "Preserve any prior staging; do not overwrite it blindly."
expected={}
for base in (source,overlay):
    for p in sorted(base.rglob("*")):
        if p.is_file(): expected[p.relative_to(base).as_posix()]=p
assert len(expected)==97
assert "media/lua/shared/B47_CohesiveCursor.lua" not in expected
assert "media/lua/server/B47_CohesiveCursor.lua" in expected
assert all("1.1.0-dev.5" in p.read_text() for rel,p in expected.items()
           if rel.endswith(".lua") and "B47_" in rel)
for rel,p in expected.items():
    if "Cohesive" not in rel or not rel.endswith(".lua"): continue
    text=p.read_text()
    for forbidden in ("transmitUpdatedSprite","B47CohesiveIronPost","LoadGridsquare",
                      "getGridSquare","OnObjectAboutToBeRemoved","OnDestroyIsoThumpable"):
        assert forbidden not in text,(rel,forbidden)
build=stage/"Contents/mods"/modid
(build/"common").mkdir(parents=True)
records=[]
for rel,p in expected.items():
    target=build/"42"/rel; target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(p,target)
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    assert hashlib.sha256(target.read_bytes()).hexdigest()==digest
    records.append({"path":"42/"+rel,"sha256":digest})
shutil.copy2(source/"poster.png",stage/"preview.png")
assert (stage/"preview.png").stat().st_size<1048576
description=(ROOT/"WORKSHOP_DESCRIPTION.txt").read_text().strip()
note=(ROOT/"WORKSHOP_CHANGE_NOTE.txt").read_text().strip()
assert description.startswith("[b]Version "+version+"[/b]")
assert note.startswith("[b]Version "+version+"[/b]")
assert "UNTESTED" in description and "UNTESTED" in note
assert "\\n" not in note
(stage/"workshop.txt").write_text("version=1\nid="+item+"\ntitle=B47ANCE'd Buildable Fences\ndescription="+
 description.replace("\n","<LINE>")+"\ntags=Build 42;Building\n",encoding="utf-8")
out=ROOT/"dist/current"; out.mkdir(parents=True,exist_ok=True)
archive=out/(modid+"-"+version+".zip")
assert not archive.exists(),"Preserve prior artifacts."
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
    z.writestr(modid+"/common/","")
    for rec in records:
        z.write(build/rec["path"],modid+"/"+rec["path"])
with zipfile.ZipFile(archive) as z:
    assert len([n for n in z.namelist() if not n.endswith("/")])==len(records)
    for rec in records:
        assert hashlib.sha256(z.read(modid+"/"+rec["path"])).hexdigest()==rec["sha256"]
vdfdir=stage.parent/"_steamcmd"; vdfdir.mkdir(exist_ok=True)
vdf=vdfdir/(modid+"-"+version+".vdf")
def escape(value):
    return str(value).replace("\\","\\\\").replace('"','\\"').replace("\r\n","\n").replace("\r","\n")
fields={"appid":"108600","publishedfileid":item,"contentfolder":str(stage/"Contents"),
        "description":description,"changenote":note}
# Existing item: retain visibility/title/preview. Reuploading the large preview
# hit Steam's legacy-cloud Limit exceeded error; no new preview was requested.
vdf.write_text('"workshopitem"\n{\n'+"".join('    "'+key+'" "'+escape(value)+'"\n' for key,value in fields.items())+'}\n',encoding="utf-8")
record={"version":version,"publishedfileid":item,"timestamp_utc":datetime.now(timezone.utc).isoformat(),
        "source":str(source),"overlay":str(overlay),"stage":str(stage),"vdf":str(vdf),
        "archive":str(archive),"archive_sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),
        "file_count":len(records),"files":records,"source_stage_zip_parity":"PASS",
        "visibility":"Preserve","test_kit":"Included by explicit testing-publication authorization",
        "publication_gate_exception":"User explicitly requests untested prerelease for dedicated testing",
        "native_SP":"NOT TESTED","dedicated_MP":"NOT TESTED","stable_G8":"BLOCKED",
        "upload":"NOT YET ATTEMPTED"}
(ROOT/"docs/evidence/workshop-test-package.json").write_text(json.dumps(record,indent=2)+"\n")
inventory=json.loads((ROOT/"version-inventory.json").read_text())
for artifact in inventory["packaging"]["artifacts"]:
    for member in artifact.get("zip_members",[]):
        if member["member"]==modid+"/42/mod.info":
            # ZIP decoding preserves source CRLF; filesystem read_text normalizes it.
            member["pattern"]=r"^modversion=(?P<version>\S+)\r?$"
new=[("WORKSHOP_DESCRIPTION.txt",r"^\[b\]Version (?P<version>[^\[]+)\[/b\]$"),
     ("docs/WORKSHOP_DEV5_TEST_RELEASE.md",r"^Project Version: (?P<version>\S+)$"),
     ("docs/evidence/workshop-test-package.json",r'"version": "(?P<version>[^"]+)"')]
for rel,pattern in new:
    if not any(m["path"]==rel for m in inventory["mirrors"]):
        inventory["mirrors"].append({"path":rel,"pattern":pattern})
inventory["other_versions"].append({"category":"compatibility","reference":"Generated staging workshop.txt version=1",
                                    "reason":"Native Workshop metadata format, independent of project version"})
(ROOT/"version-inventory.json").write_text(json.dumps(inventory,indent=2)+"\n")
print("Prepared",len(records),"hash-verified files; archive:",archive)
print("Upload VDF:",vdf)
