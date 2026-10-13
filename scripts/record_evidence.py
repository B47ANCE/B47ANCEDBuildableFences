"""Record scoped source diff/hash evidence, never create release artifacts."""
import difflib
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "src/B47ANCEDBuildableFences/42"
BASELINE = Path(r"E:\Program Files (x86)\Steam\steamapps\workshop\content\108600\3810187215\mods\B47ANCEDBuildableFences\42")
GAME = Path(r"E:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    records, diffs = [], []
    for path in sorted(MOD.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(MOD)
        old = BASELINE / rel
        state = "added" if not old.exists() else "unchanged" if old.read_bytes() == path.read_bytes() else "modified"
        records.append({"path": "src/B47ANCEDBuildableFences/42/" + rel.as_posix(), "state": state,
                        "sha256": digest(path), "baseline_sha256": digest(old) if old.exists() else None})
        if state != "unchanged" and path.suffix in (".lua", ".txt", ".info", ".json"):
            before = old.read_text(encoding="utf-8-sig").splitlines(True) if old.exists() else []
            after = path.read_text(encoding="utf-8-sig").splitlines(True)
            diffs.extend(difflib.unified_diff(before, after, fromfile="baseline-1.0.37/" + rel.as_posix(), tofile=version + "/" + rel.as_posix()))
    native = ["projectzomboid.jar", "media/newtiledefinitions.tiles", "media/newtiledefinitions.tiles.txt",
              "media/tiledefinitions_noiseworks.patch.tiles", "media/tiledefinitions_noiseworks.patch.tiles.txt",
              "media/tileGeometry.txt", "media/texturepacks/Tiles2x.pack",
              "media/scripts/generated/items/drainable.txt", "media/scripts/generated/recipes/recipes_buckets.txt",
              "media/lua/server/BuildingObjects/ISBuildIsoEntity.lua", "media/lua/server/BuildingObjects/ISBuildUtil.lua",
              "media/lua/client/BuildingObjects/TimedActions/ISBuildAction.lua", "media/lua/server/Items/BrokenFences.lua",
              "media/scripts/generated/sounds/zombies/sounds_zombie_foley.txt"]
    references = [{"path": str(GAME / name), "sha256": digest(GAME / name)} for name in native]
    badlands = Path(r"E:\Program Files (x86)\Steam\steamapps\workshop\content\108600\3804156157\mods\FullBookcases\42")
    for name in ["mod.info", "media/scripts/entities/knx_fences.txt", "media/scripts/entities/knx_fences_xuiSkin.txt", "media/badlands_bookcase_01.tiles.txt"]:
        references.append({"path": str(badlands / name), "sha256": digest(badlands / name), "reference_only": True})
    data = {"version": version, "date": "2026-10-02", "environment": "Windows offline; PZ/server NOT RUN",
            "source": records, "references": references}
    (ROOT / "docs/evidence/development-hashes.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    (ROOT / "docs/evidence/source-diff.txt").write_text("".join(diffs), encoding="utf-8")
    changed = [r for r in records if r["state"] != "unchanged"]
    listing = "# Exact source file changes\n\nProject Version: " + version + "\n\n"
    listing += "Compared with the user's downloaded baseline; all paths are project-relative.\n\n"
    for r in changed:
        listing += f"- {r['state']}: `{r['path']}`\n"
    listing += "\nUnchanged baseline assets are copied into the editable project, not modified.\n"
    listing += "Current SHA256 manifest and full text diff: development-hashes.json and source-diff.txt.\n"
    (ROOT / "docs/evidence/CHANGED_FILES.md").write_text(listing, encoding="utf-8")
    print(f"Recorded {len(records)} source files; {len(changed)} added/modified; {len(references)} upstream reference hashes")


if __name__ == "__main__":
    main()
