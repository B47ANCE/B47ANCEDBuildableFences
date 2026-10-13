"""Read installed vanilla text tile definitions without modifying the game."""
import hashlib
import json
import re
from pathlib import Path

GAME = Path(r"E:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid")
ROOT = Path(__file__).resolve().parents[1]


def read_tiles(path):
    tiles = {}
    text = path.read_text(encoding="utf-8-sig")
    for match in re.finditer(r"// ([\w]+_\d+)\s+tile\s*\{([^{}]*)\}", text):
        props = {}
        for line in match[2].splitlines():
            if "=" in line:
                key, value = line.strip().split("=", 1)
                props[key.strip()] = value.strip()
        tiles[match[1]] = props
    return tiles


def main():
    files = [GAME / "media/newtiledefinitions.tiles.txt",
             GAME / "media/tiledefinitions_noiseworks.patch.tiles.txt"]
    records = {}
    for path in files:
        for name, props in read_tiles(path).items():
            if name.startswith(("fencing_01_", "fixtures_doors_fences_01_", "carpentry_02_", "constructedobjects_01_")):
                records.setdefault(name, {}).update(props)
    result = {"evidence": "VERIFIED_SOURCE, text definitions; runtime loading not tested",
              "sources": [{"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],
              "tiles": records}
    out = ROOT / "docs/evidence/vanilla_tiles.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded {len(records)} tiles in {out}")
    for i in list(range(64, 80)) + [8, 9, 10, 11, 12, 13, 48, 49, 50, 51, 52, 53, 80, 81, 82, 83, 84, 88, 89, 90, 91, 92]:
        name = f"fencing_01_{i}"
        print(name, json.dumps(records.get(name)))


if __name__ == "__main__":
    main()
