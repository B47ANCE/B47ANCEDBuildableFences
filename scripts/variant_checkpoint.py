"""Archive the rejected dev.3 experiment; advance the isolated design checkpoint."""
import json
import re
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OLD,NEW="1.1.0-dev.3","1.1.0-dev.4"
assert (ROOT/"VERSION").read_text().strip()==OLD
history=ROOT/"docs/evidence/history"/OLD
assert not history.exists()
inventory=json.loads((ROOT/"version-inventory.json").read_text())
paths={m["path"] for m in inventory["mirrors"]}
paths.update(["VERSION","version-inventory.json","CHANGELOG.md","tests/test_cohesive.py",
 "tests/test_fence_testkit.py","docs/BADLANDS_FENCE_REFERENCE_AUDIT.md",
 "src/B47ANCEDBuildableFences/42/media/scripts/generated/entities/walls/entity_b47_buildable_fences.txt"])
for rel in paths:
    target=history/rel; target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/rel,target)
shutil.copytree(ROOT/"prototypes/cohesive/42",history/"automatic-topology-overlay/42")
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
 "Corrected isolated Wrought Iron variant-selection prototype: Q/E reaches all\n"
 "original pieces/faces using their own recipes. Automatic topology archived\n"
 "and removed from active overlay. Public source gameplay remains unchanged.\n"
 "Native collision/save/dedicated gates remain untested.\n",1),encoding="utf-8")
inventory["historical"].append({"reference":"docs/evidence/history/"+OLD+"; scripts/variant_checkpoint.py",
 "reason":"Rejected topology overlay, old tests/reports and exact dev.3 evidence; never current proof"})
(ROOT/"version-inventory.json").write_text(json.dumps(inventory,indent=2)+"\n")
