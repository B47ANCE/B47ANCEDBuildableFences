"""Generate exact identity mappings from the hash-pinned downloaded release.

This is an offline audit, never a world migration or a save writer.
"""
import hashlib
import json
import re
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tests"))
from test_fences import BASELINE, ENTITY, MOD, entities

old,new=entities(BASELINE/ENTITY),entities(MOD/ENTITY)
assert len(old)==17
for record in json.loads((ROOT/"docs/evidence/baseline-1.0.37/hashes.json").read_text(encoding="utf-8-sig")):
    assert hashlib.sha256((BASELINE/record["Path"]).read_bytes()).hexdigest().upper()==record["SHA256"]
mappings={}
for name,block in old.items():
    faces=dict(re.findall(r"face (\w+)\s*\{\s*layer\s*\{\s*row = (\w+)",block))
    assert name in new
    assert faces==dict(re.findall(r"face (\w+)\s*\{\s*layer\s*\{\s*row = (\w+)",new[name]))
    mappings[name]={"current_entity":name,"strategy":"retain-existing-object","faces":faces,
                    "recipe_definition":"Unchanged embedded component CraftRecipe in Base."+name,
                    "entity_style":"ES_"+name}
data={"schema":1,"project_version":(ROOT/"VERSION").read_text().strip(),
      "legacy_versions":["1.0.37"],"mod_id":"B47ANCEDBuildableFences","workshop_id":"3810187215",
      "world_mutations":False,"custom_tile_id_remaps":{},
      "recognition":"Exact entity plus face/sprite pairs only; unlabelled IsoObject posts are not identified by sprite alone.",
      "lifecycle":"Native deserialization retains existing objects; no migration callback or marker.",
      "entities":mappings}
target=ROOT/"compatibility/LegacyFenceMap.json"; target.parent.mkdir(exist_ok=True)
target.write_text(json.dumps(data,indent=2)+"\n")
rows=["| Legacy / retained current entity | Faces and retained vanilla sprites |","|---|---|"]
for name,m in mappings.items():
    rows.append("| `"+name+"` | "+", ".join(face+" = `"+sprite+"`" for face,sprite in m["faces"].items())+" |")
(ROOT/"docs/evidence/legacy-identity-table.md").write_text("# Downloaded 1.0.37 identity audit\n\nProject Version: "+data["project_version"]+"\n\n[VERIFIED source] Every row maps identically; no object replacement.\n\n"+"\n".join(rows)+"\n")
