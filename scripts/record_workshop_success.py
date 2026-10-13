"""Record explicit SteamCMD commit success; never turn it into runtime PASS."""
import hashlib
import json
import re
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
record_path=ROOT/"docs/evidence/workshop-test-package.json"
record=json.loads(record_path.read_text())
log_path=ROOT/"docs/evidence/workshop-test-upload.txt"
log=log_path.read_text(encoding="utf-8-sig")
assert "Committing update...Success." in log
assert "ERROR!" not in log
vdf=Path(record["vdf"])
assert re.search(r'"publishedfileid"\s+"3810187215"',vdf.read_text())
assert '"previewfile"' not in vdf.read_text()
assert record["version"]==(ROOT/"VERSION").read_text().strip()
base=Path(record["stage"])/"Contents/mods/B47ANCEDBuildableFences"
for item in record["files"]:
    assert hashlib.sha256((base/item["path"]).read_bytes()).hexdigest()==item["sha256"]
record.update(upload="SUCCESS: SteamCMD Committing update...Success.; process exit 0",
              published_at_utc=datetime.now(timezone.utc).isoformat(),
              upload_log_sha256=hashlib.sha256(log_path.read_bytes()).hexdigest(),
              upload_vdf_sha256=hashlib.sha256(vdf.read_bytes()).hexdigest(),
              workshop_url="https://steamcommunity.com/sharedfiles/filedetails/?id=3810187215")
record_path.write_text(json.dumps(record,indent=2)+"\n")
print("Recorded successful dev.5 Workshop commit for",record["publishedfileid"])
