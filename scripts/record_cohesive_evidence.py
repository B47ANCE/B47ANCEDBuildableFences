"""Record isolated overlay provenance; regenerate complete fallback translations."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "prototypes/cohesive/42"
SOURCE = ROOT / "src/B47ANCEDBuildableFences/42"
for folder in (SOURCE / "media/lua/shared/Translate").iterdir():
    values = json.loads((folder / "IG_UI.json").read_text())
    values["IGUI_B47_WroughtIronFence_PlainSection"] = "Wrought Iron Fence"
    values["IGUI_B47_WroughtIronGate"] = "Wrought Iron Gate"
    values.update({
        "IGUI_B47_VariantSelected": "Selected: %1 / %2",
        "IGUI_B47_VariantControls": "Q: previous piece/face | E: next piece/face",
        "IGUI_B47_VariantKeep": "(reusable tool)",
        "IGUI_B47_Variant_PlainSection": "Plain Section",
        "IGUI_B47_Variant_PostEndedSection": "Post-Ended Section",
        "IGUI_B47_Variant_Corner": "Corner",
        "IGUI_B47_Variant_Post": "Standalone Post",
        "IGUI_B47_Variant_WroughtIronGate": "Wrought Iron Gate",
        "IGUI_B47_TestKitMenu": "b47fencetestkit (DEV / RUNTIME TESTING ONLY)",
        "IGUI_B47_TestKitDenied": "B47 test kit denied: multiplayer server admin role required.",
        "IGUI_B47_TestKitFailed": "B47 test kit failed: check the server log; no kit was prepared.",
        "IGUI_B47_TestKitSpawned": "B47 Fence Test Kit spawned: tools -> inventory; materials -> ground (%1 items).",
    })
    target = OVERLAY / "media/lua/shared/Translate" / folder.name / "IG_UI.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(values, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
version = (ROOT / "VERSION").read_text().strip()
data = {"version": version, "environment": "Windows offline; PZ/server NOT RUN",
        "overlay": [{"path": p.relative_to(ROOT).as_posix(),
                     "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                    for p in sorted(OVERLAY.rglob("*")) if p.is_file()]}
(ROOT / "docs/evidence/cohesive-hashes.json").write_text(json.dumps(data, indent=2) + "\n")
inventory = json.loads((ROOT / "version-inventory.json").read_text())
reference = "docs/evidence/history/dev.3-before-testkit"
if not any(h["reference"] == reference for h in inventory["historical"]):
    inventory["historical"].append({"reference": reference,
        "reason": "Original 29-test dev.3 prototype evidence before test utility; not current proof"})
existing = {m["path"] for m in inventory["mirrors"]}
for p in sorted(OVERLAY.rglob("*.lua")):
    rel = p.relative_to(ROOT).as_posix()
    if rel not in existing:
        inventory["mirrors"].append({"path": rel, "pattern": "^-- B47ANCE'd Buildable Fences v(?P<version>\\S+)$"})
for rel in ["docs/COHESIVE_PROTOTYPE_REPORT.md", "prototypes/cohesive/README.md", "docs/FENCE_TEST_KIT.md"]:
    if rel not in existing:
        inventory["mirrors"].append({"path": rel, "pattern": "^Project Version: (?P<version>\\S+)$"})
rel = "docs/evidence/cohesive-hashes.json"
if rel not in existing:
    inventory["mirrors"].append({"path": rel, "pattern": '\\u0022version\\u0022: \\u0022(?P<version>[^\\u0022]+)\\u0022'})
(ROOT / "version-inventory.json").write_text(json.dumps(inventory, indent=2) + "\n")
