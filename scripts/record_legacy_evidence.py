"""Record exact dev.5 scope and observed deployment; read-only external inputs."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
version=(ROOT/"VERSION").read_text().strip()
history=ROOT/"docs/evidence/history/1.1.0-dev.4"
inventory=json.loads((ROOT/"version-inventory.json").read_text())
startup={"path":"prototypes/cohesive/42/media/lua/client/B47_CohesivePresentation.lua",
 "pattern":r'cohesive selector (?P<version>\S+) initialized'}
if not any(m==startup for m in inventory["mirrors"]):
    inventory["mirrors"].append(startup)
for path in ("docs/evidence/legacy-checkpoint-changes.md",):
    if not any(m["path"]==path for m in inventory["mirrors"]):
        inventory["mirrors"].append({"path":path,"pattern":r"^Project Version: (?P<version>\S+)$"})
observation_mirror={"path":"docs/evidence/legacy-live-observation.json",
 "pattern":r'"source_version": "(?P<version>[^"]+)"'}
if not any(m==observation_mirror for m in inventory["mirrors"]):
    inventory["mirrors"].append(observation_mirror)
(ROOT/"version-inventory.json").write_text(json.dumps(inventory,indent=2)+"\n")
changes=[]
for p in sorted(history.rglob("*")):
    if not p.is_file(): continue
    rel=p.relative_to(history).as_posix()
    if rel.startswith("overlay/"):
        rel="prototypes/cohesive/"+rel[len("overlay/"):]
    target=ROOT/rel
    if not target.exists(): changes.append((rel,"removed / relocated"))
    elif target.read_bytes()!=p.read_bytes(): changes.append((rel,"modified"))
added=["scripts/legacy_checkpoint.py","scripts/finish_legacy_checkpoint.py","scripts/audit_legacy.py",
       "scripts/record_legacy_evidence.py","tests/test_legacy_compatibility.py","docs/LEGACY_COMPATIBILITY.md",
       "compatibility/LegacyFenceMap.json","docs/evidence/legacy-identity-table.md",
       "prototypes/cohesive/42/media/lua/server/B47_CohesiveCursor.lua"]
changes=sorted(set(changes+[(p,"added") for p in added]))
rows=["# Dev.4 to dev.5 checkpoint changes","","Project Version: "+version,"",
      "Runtime behavior changed only in the isolated cursor/presentation load phase.",
      "Production Lua changes are version headers only; gameplay definitions unchanged.",
      "All dev.4 evidence is archived under history/1.1.0-dev.4, including its overlay.","",
      "| Project-relative file | Change |","|---|---|"]
rows.extend("| `"+p+"` | "+status+" |" for p,status in changes)
rows.extend(["","Also modified workspace docs/BUILD42_INTERACTION_PATTERNS.md with the",
             "phase-ordering finding; native confirmation remains untested.",
             "This report itself is new. Native class/decompile evidence was added under",
             "research/classes and research/vanilla for LuaManager, GameWindow,",
             "GameLoadingState, GameServer (class only), and IsoWorld."])
(ROOT/"docs/evidence/legacy-checkpoint-changes.md").write_text("\n".join(rows)+"\n")
attachment=Path(r"C:\Users\willi\.codex\attachments\490ac2f3-224d-4fa0-ba78-98febfb4de15\Pasted text.txt")
live=Path(r"C:\Users\willi\Zomboid\mods\B47ANCEDBuildableFences")
deploy=json.loads((ROOT/"docs/evidence/test-deployment.json").read_text())
observation={"source_version":version,"runtime_loaded_version":"UNKNOWN: no path/version diagnostic in supplied trace",
 "supplied_log_sha256":hashlib.sha256(attachment.read_bytes()).hexdigest(),
 "supplied_log":str(attachment),"native_failure":"shared B47_CohesiveCursor.lua:6 indexes unavailable ISBuildIsoEntity",
 "local_mod_info":(live/"42/mod.info").read_text(),
 "original_deployment_version":deploy["version"],"new_deployment_performed":False,
 "native_fix_retest":"NOT TESTED","legacy_save_runtime":"NOT TESTED"}
(ROOT/"docs/evidence/legacy-live-observation.json").write_text(json.dumps(observation,indent=2)+"\n")
print("Recorded",len(changes),"checkpoint file changes; actual local metadata retained")
