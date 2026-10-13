"""Preserve failed upload evidence; retain the existing published preview."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
record_path=ROOT/"docs/evidence/workshop-test-package.json"
record=json.loads(record_path.read_text())
assert record["version"]=="1.1.0-dev.5" and record["publishedfileid"]=="3810187215"
log=ROOT/"docs/evidence/workshop-test-upload.txt"
failed=ROOT/"docs/evidence/workshop-test-upload-preview-failed.txt"
assert "Failed to update workshop item (Limit exceeded)" in log.read_text(encoding="utf-8-sig")
assert not failed.exists()
failed.write_bytes(log.read_bytes())
def escape(value):
    return str(value).replace("\\","\\\\").replace('"','\\"').replace("\r\n","\n").replace("\r","\n")
fields={"appid":"108600","publishedfileid":record["publishedfileid"],
        "contentfolder":str(Path(record["stage"])/"Contents"),
        "description":(ROOT/"WORKSHOP_DESCRIPTION.txt").read_text().strip(),
        "changenote":(ROOT/"WORKSHOP_CHANGE_NOTE.txt").read_text().strip()}
Path(record["vdf"]).write_text('"workshopitem"\n{\n'+"".join('    "'+key+'" "'+escape(value)+'"\n' for key,value in fields.items())+'}\n',encoding="utf-8")
record["first_upload"]="FAILED: Limit exceeded during preview handling; retained complete log"
record["preview"]="Retain existing Workshop image; retry omits previewfile"
record["upload"]="RETRY PREPARED; NOT YET CONFIRMED"
record_path.write_text(json.dumps(record,indent=2)+"\n")
print("Prepared content-only retry; existing title, visibility and preview retained")
