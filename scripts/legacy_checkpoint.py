"""Bounded dev.4 -> dev.5 transition; preserve actual deployed evidence."""
import json
import re
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OLD,NEW="1.1.0-dev.4","1.1.0-dev.5"
assert (ROOT/"VERSION").read_text().strip()==OLD
inventory=json.loads((ROOT/"version-inventory.json").read_text())
history=ROOT/"docs/evidence/history"/OLD
assert not history.exists()
paths={m["path"] for m in inventory["mirrors"]}
paths.update(["VERSION","version-inventory.json","CHANGELOG.md","tests/test_variant_selection.py"])
for rel in paths:
    target=history/rel; target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/rel,target)
shutil.copytree(ROOT/"prototypes/cohesive/42",history/"overlay/42")
inventory["mirrors"]=[m for m in inventory["mirrors"] if m["path"]!="docs/evidence/test-deployment.json"]
for m in inventory["mirrors"]:
    p=ROOT/m["path"]; value=p.read_bytes().decode("utf-8")
    pattern=re.compile(m["pattern"].replace("$",r"\r?$"),re.MULTILINE)
    def replace(match):
        a,b=match.span("version")
        return match[0][:a-match.start()]+NEW+match[0][b-match.start():]
    value,count=pattern.subn(replace,value); assert count==1,(p,count)
    p.write_bytes(value.encode("utf-8"))
(ROOT/"VERSION").write_text(NEW+"\n")
p=ROOT/"CHANGELOG.md"
p.write_text(p.read_text().replace("# Changelog\n","# Changelog\n\n## ["+NEW+"]\n\n"
 "Compatible startup fix for the isolated selector: defer client hooks until\n"
 "OnGameStart and load cursor hooks in the native server Lua phase. Audit\n"
 "downloaded 1.0.37 save identities with an explicit unchanged-definition map;\n"
 "no world-object replacement or save edits. Native migration gates untested.\n",1),encoding="utf-8")
inventory["historical"].append({"reference":"docs/evidence/history/"+OLD+"; docs/evidence/test-deployment.json; scripts/legacy_checkpoint.py",
 "reason":"Preserved dev.4 validation and actual deployed dev.4 copy; not dev.5 proof"})
(ROOT/"version-inventory.json").write_text(json.dumps(inventory,indent=2)+"\n")
