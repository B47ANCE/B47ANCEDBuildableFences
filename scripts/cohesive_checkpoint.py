"""Preserve dev.2 evidence and advance metadata; never deploy/package a mod."""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD, NEW = "1.1.0-dev.2", "1.1.0-dev.3"
assert (ROOT / "VERSION").read_text().strip() == OLD
inventory = json.loads((ROOT / "version-inventory.json").read_text())
history = ROOT / "docs/evidence/history" / OLD
assert not history.exists()
paths = {m["path"] for m in inventory["mirrors"]}
paths.update(["VERSION", "version-inventory.json", "CHANGELOG.md", "tests/test_fences.py",
              "docs/BADLANDS_FENCE_REFERENCE_AUDIT.md",
              "src/B47ANCEDBuildableFences/42/media/scripts/generated/entities/walls/entity_b47_buildable_fences.txt"])
for rel in sorted(paths):
    target = history / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / rel, target)
for mirror in inventory["mirrors"]:
    path = ROOT / mirror["path"]
    value = path.read_bytes().decode("utf-8")
    pattern = re.compile(mirror["pattern"].replace("$", r"\r?$"), re.MULTILINE)
    def replace(match):
        a, b = match.span("version")
        return match[0][:a-match.start()] + NEW + match[0][b-match.start():]
    value, count = pattern.subn(replace, value)
    assert count == 1, (path, count)
    path.write_bytes(value.encode("utf-8"))
(ROOT / "VERSION").write_text(NEW + "\n")
changelog = ROOT / "CHANGELOG.md"
value = changelog.read_text()
value = value.replace("# Changelog\n", "# Changelog\n\n## [" + NEW + "]\n\n"
    "Isolated Wrought Iron cohesive construction prototype; production recipe/gameplay\n"
    "files retain dev.2 behavior. One fence entry, Q/E intent, native gate, authority-only\n"
    "topology and decorative posts. Offline evidence only; G7/G8 remain blocked.\n", 1)
changelog.write_text(value, encoding="utf-8")
inventory["historical"].append({"reference": "docs/evidence/history/" + OLD + "; scripts/cohesive_checkpoint.py",
    "reason": "Immutable prior checkpoint and fixed transition fixture; not current proof"})
(ROOT / "version-inventory.json").write_text(json.dumps(inventory, indent=2) + "\n")
