"""Guarded skill-only dev.1 -> dev.2 edit; never deploys or packages."""
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "src/B47ANCEDBuildableFences/42"
OLD, NEW = "1.1.0-dev.1", "1.1.0-dev.2"
ENTITY = Path("media/scripts/generated/entities/walls/entity_b47_buildable_fences.txt")


def main():
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != OLD:
        raise SystemExit("Expected dev.1 baseline; refusing to edit another checkpoint")
    history = ROOT / "docs/evidence/history" / OLD
    if history.exists():
        raise SystemExit("Historical checkpoint already exists; inspect rather than overwrite")
    history.mkdir(parents=True)
    inventory = json.loads((ROOT / "version-inventory.json").read_text(encoding="utf-8"))
    paths = {m["path"] for m in inventory["mirrors"]} | {"VERSION", "CHANGELOG.md", "version-inventory.json", "docs/evidence/source-diff.txt", "tests/test_fences.py"}
    for rel in paths:
        source = ROOT / rel
        dest = history / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
    dest = history / "src/B47ANCEDBuildableFences/42" / ENTITY
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(MOD / ENTITY, dest)
    hashes = []
    for path in sorted(MOD.rglob("*")):
        if path.is_file():
            raw = path.read_bytes()
            normalized = raw.replace(OLD.encode(), b"CURRENT_VERSION") if path.suffix == ".lua" or path.name == "mod.info" else raw
            hashes.append({"path": path.relative_to(MOD).as_posix(), "sha256": hashlib.sha256(raw).hexdigest(), "version_neutral_sha256": hashlib.sha256(normalized).hexdigest()})
    (history / "source-hashes.json").write_text(json.dumps(hashes, indent=2) + "\n", encoding="utf-8")

    # Advance current text mirrors, not historical validations/hashes.
    excluded = {"docs/evidence/offline-tests.txt", "docs/evidence/version-check.txt", "docs/evidence/development-hashes.json", "docs/evidence/CHANGED_FILES.md"}
    for m in inventory["mirrors"]:
        if m["path"] not in excluded:
            path = ROOT / m["path"]
            path.write_bytes(path.read_bytes().replace(OLD.encode(), NEW.encode()))
    (ROOT / "VERSION").write_text(NEW + "\n", encoding="utf-8")
    changelog = ROOT / "CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8")
    text = text.replace("# Changelog\n", "# Changelog\n\n## [" + NEW + "]\n\nSkill-only compatible rebalance: Straight Top Carpentry 7 to 4; Security\nand Razor Welding 7 to 4. Sloped Top, Military and Wrought Iron remain at 7.\nAll materials, XP rewards, health fields, sprites, cutaway, sound and\nnetworking behavior are preserved. No deployment or runtime claim.\n", 1)
    changelog.write_text(text, encoding="utf-8")

    path = MOD / ENTITY
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    names = {"B47_TallWoodenFence_" + v: "Woodwork" for v in ["StraightTop", "StraightTopCorner", "StraightTopPost"]}
    names.update({"B47_" + family + "_" + variant: "MetalWelding" for family in ["SecurityFence", "RazorWireSecurityFence"] for variant in ["PlainSection", "PostEndedSection", "Corner"]})
    edits = []
    for match in re.finditer(r"    entity (B47_\w+)\s*\{", text):
        if match[1] not in names:
            continue
        depth = 0
        for pos in range(match.end()-1, len(text)):
            depth += (text[pos] == "{") - (text[pos] == "}")
            if depth == 0:
                block = text[match.start():pos+1]
                old = f"SkillRequired = {names[match[1]]}:7,"
                assert block.count(old) == 1, match[1]
                edits.append((match.start(), pos+1, block.replace(old, old.replace(":7,", ":4,"))))
                break
    assert len(edits) == 9, len(edits)
    for start, end, replacement in reversed(edits):
        text = text[:start] + replacement + text[end:]
    path.write_bytes(text.encode("utf-8"))
    print("Updated exactly nine SkillRequired entries; preserved every other entity byte")


if __name__ == "__main__":
    main()
