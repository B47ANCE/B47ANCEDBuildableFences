"""Synchronize current audit links/inventory without altering deployed evidence."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
assert (ROOT/"VERSION").read_text().strip()=="1.1.0-dev.5"
p=ROOT/"version-inventory.json"; data=json.loads(p.read_text())
for m in data["mirrors"]:
    if m["path"].endswith("shared/B47_CohesiveCursor.lua"):
        m["path"]=m["path"].replace("shared/B47_CohesiveCursor.lua","server/B47_CohesiveCursor.lua")
for path,pattern in [
    ("docs/LEGACY_COMPATIBILITY.md",r"^Project Version: (?P<version>\S+)$"),
    ("docs/evidence/legacy-identity-table.md",r"^Project Version: (?P<version>\S+)$"),
    ("compatibility/LegacyFenceMap.json",r'"project_version": "(?P<version>[^"]+)"'),
]:
    if not any(m["path"]==path for m in data["mirrors"]):
        data["mirrors"].append({"path":path,"pattern":pattern})
data["historical"].append({"reference":"scripts/finish_legacy_checkpoint.py",
 "reason":"Bounded dev.5 documentation transition fixture, not current metadata"})
p.write_text(json.dumps(data,indent=2)+"\n")
updates={
"README.md":[("This checkpoint changes only nine construction skill requirements.","The earlier skill checkpoint changed nine construction skill requirements."),
 ("See [implementation report]", "See [legacy compatibility audit](docs/LEGACY_COMPATIBILITY.md) for the exact\n17 retained 1.0.37 identities and source-only startup fix. Native save safety\nis untested; local deployment remains dev.4.\n\nSee [implementation report]")],
"docs/COHESIVE_PROTOTYPE_REPORT.md":[("shared B47_CohesiveCursor.lua", "server B47_CohesiveCursor.lua"),
 ("The complete current suite passes 33 offline tests; all declared version mirrors\nmatch dev.4. This supersedes active validation while keeping dev.3 proofs intact.",
  "Current offline results are in evidence/offline-tests.txt. Dev.4 user-supplied\nstartup trace FAILED during shared cursor loading; dev.5 moves that cursor\nto server Lua and defers client presentation to OnGameStart. Native retest\nis pending. Historical dev.4/deployment proofs remain unchanged.")],
"docs/ARCHITECTURE.md":[("dev.4 contains", "The active overlay contains")],
}
for rel,replacements in updates.items():
    p=ROOT/rel; value=p.read_text()
    for before,after in replacements:
        assert before in value,(rel,before)
        value=value.replace(before,after,1)
    p.write_text(value,encoding="utf-8")
paragraphs={
 "docs/VERSIONING.md":"\nDev.5 is a compatible startup fix and explicit 1.0.37 identity-retention audit\nwithin the same 1.1.0 MINOR target. See LEGACY_COMPATIBILITY.md. Actual local\ndev.4 deployment evidence is classified historical, never retagged as dev.5.\n",
 "docs/TESTING.md":"\n## Legacy and initialization gate\n\nSee LEGACY_COMPATIBILITY.md for the exact 17-entity identity map and full\nold-save fixture procedure. The supplied dev.4-like prototype startup log\nFAILS at shared cursor initialization. Dev.5 source fixes phase ordering;\nnative retest, old-save SP/listen/dedicated/restart/late-chunk validation are\nNOT TESTED. Existing post-conversion custom-state limitations block blanket\nstate-preservation claims. Current offline counts are in evidence/offline-tests.txt.\n",
 "docs/ROADMAP.md":"\n- Legacy 1.0.37 identity retention audited; no destructive migration needed\n  for unchanged definitions. Earlier versions UNKNOWN; old-save native matrix\n  and post-conversion state preservation remain blocked.\n- Prototype load-order source fix implemented; user-log startup failure needs\n  native retest before testing Q/E/menu behavior. Local deployed copy is dev.4.\n",
 "docs/FENCE_TEST_KIT.md":"\nThe supplied runtime log fails during shared cursor loading before normal\nprototype startup. Dev.5 fixes phase ordering in source; native menu retest\nis pending. The deployed dev.4 copy has not been updated by this checkpoint.\n",
 "docs/WORKSHOP_DESCRIPTION.md":"\nDevelopment note: 1.0.37 entity/sprite identities remain defined. Native\nold-save compatibility is untested; no save-safe claim. Prototype startup\nphase fix awaits native verification.\n",
 "WORKSHOP_CHANGE_NOTE.txt":"\nDevelopment source: retain all 17 downloaded 1.0.37 identities; explicit\ncompatibility audit and staged-load fix for isolated Q/E prototype. Native\nsave and dedicated validation pending. Not deployed or published.\n",
 "docs/IMPLEMENTATION_REPORT.md":"\nCurrent follow-up: see LEGACY_COMPATIBILITY.md for exact identity retention,\nstartup failure/source fix, post-state limitation and remaining native gates.\n",
 "prototypes/cohesive/README.md":"\nDev.5 moves cursor hooks into server Lua and defers client UI installation to\nOnGameStart after a user-supplied startup failure. Native retest pending.\nSource-only checkpoint; actual local deployed copy remains dev.4.\n",
}
for rel,paragraph in paragraphs.items():
    p=ROOT/rel; p.write_text(p.read_text()+paragraph,encoding="utf-8")
