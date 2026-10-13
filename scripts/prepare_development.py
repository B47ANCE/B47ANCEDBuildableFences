"""One-time, bounded upgrade of the recovered B47 baseline; never deploys."""
import json
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "src/B47ANCEDBuildableFences/42"
VERSION = "1.1.0-dev.1"
LANGUAGES = "AR CA CH CN CS DA DE EN ES ES_CL ES_MX FI FR HU ID IT JP KO NL NO PL PT PTBR RO RU STREW TH TR UA".split()


def set_version():
    paths = [ROOT / "VERSION", ROOT / "README.md", MOD / "mod.info", MOD / "README.txt",
             MOD / "media/lua/client/B47_NonBlockingPosts_Client.lua",
             MOD / "media/lua/server/B47_NonBlockingPosts_Server.lua"]
    for path in paths:
        text = path.read_text(encoding="utf-8-sig")
        # Only current headers; historical operation comments remain intact.
        if path.name == "VERSION":
            text = VERSION + "\n"
        elif path.name == "README.md":
            text = text.replace("Project Version: 1.0.37", "Project Version: " + VERSION)
        elif path.name == "mod.info":
            text = text.replace("modversion=1.0.37", "modversion=" + VERSION)
        else:
            text = text.replace("Buildable Fences v1.0.37", "Buildable Fences v" + VERSION)
            text = text.replace("Buildable Fences — v1.0.37", "Buildable Fences — v" + VERSION)
        path.write_text(text, encoding="utf-8")
    changelog = ROOT / "CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8")
    if f"## [{VERSION}]" not in text:
        text = text.replace("# Changelog\n", f"# Changelog\n\n## [{VERSION}]\n\nCompatible minor development expansion from the downloaded baseline.\nAdds four wrought-iron variants, concrete-use Security/Razor recipes and\nmaterial sound initialization. Wooden cutaway correction remains blocked\npending a proven runtime root cause. No release artifacts or deployment.\n")
        changelog.write_text(text, encoding="utf-8")


def implement():
    entities = MOD / "media/scripts/generated/entities/walls/entity_b47_buildable_fences.txt"
    text = entities.read_text(encoding="utf-8-sig")
    if "entity B47_WroughtIronFence_PlainSection" in text:
        raise SystemExit("Expansion already applied; do not regenerate edited source")
    # Reuse ONLY the user's own B47 baseline family structure and balance.
    family = text[:text.index("\nmodule Base", 1)]
    family = family.replace("MilitaryFence", "WroughtIronFence")
    for old, new in [(50, 66), (49, 65), (51, 67), (48, 64), (52, 68), (53, 69)]:
        family = family.replace(f"fencing_01_{old}", f"fencing_01_{new}")
    text += "\n" + family
    # Entity blocks end at the next entity/module declaration. Keep all other
    # inputs, timings, skills, health and existing orientation rows unchanged.
    chunks = re.split(r"(?=    entity B47_)", text)
    for i, chunk in enumerate(chunks):
        name_match = re.match(r"    entity (B47_\w+)", chunk)
        if not name_match:
            continue
        name = name_match[1]
        chunk = chunk.replace("component SpriteConfig\n        {", "component SpriteConfig\n        {\n            OnCreate = B47Fence.OnCreate,", 1)
        if name.startswith(("B47_SecurityFence_", "B47_RazorWireSecurityFence_")):
            concrete = 2 if name.endswith("_Corner") else 1
            scrap = 3 if concrete == 2 else 2
            old = f"item {scrap} [Base.ScrapMetal],"
            assert chunk.count(old) == 1, name
            chunk = chunk.replace(old, f"item {concrete} [Base.BucketConcreteFull;Base.BucketCarvedConcreteFull] flags[DontRecordInput],")
        chunks[i] = chunk
    entities.write_text("".join(chunks), encoding="utf-8")
    for side in ["client", "server"]:
        path = MOD / f"media/lua/{side}/B47_NonBlockingPosts_{side.title()}.lua"
        source = path.read_text(encoding="utf-8")
        source = source.replace('["B47_MilitaryFence_Post"] = true,', '["B47_MilitaryFence_Post"] = true,\n    ["B47_WroughtIronFence_Post"] = true,')
        source = source.replace('["fencing_01_53"] = true,', '["fencing_01_53"] = true,\n    ["fencing_01_69"] = true,')
        path.write_text(source, encoding="utf-8")
    skin = MOD / "media/scripts/entities/walls/entity_b47_buildable_fences_xuiSkin.txt"
    text = skin.read_text(encoding="utf-8-sig")
    first = text[:text.index("\nmodule Base", 1)]
    first = first.replace("MilitaryFence", "WroughtIronFence").replace("Military Fence", "Wrought Iron Fence")
    text += "\n" + first
    translations = {}
    def localize(match):
        entity, body = match[1], match[2]
        display = re.search(r"DisplayName = (.*?),", body)[1]
        key = "IGUI_B47_" + entity.removeprefix("ES_B47_")
        translations[key] = display
        return "entity " + entity + "\n        {" + body.replace("DisplayName = " + display, "DisplayName = " + key) + "}"
    text = re.sub(r"entity (ES_B47_\w+)\s*\{([^{}]*)\}", localize, text)
    skin.write_text(text, encoding="utf-8")
    sandbox = {
        "Sandbox_B47ANCEDBuildableFences": "B47ANCE'd Buildable Fences",
        "Sandbox_B47_ConstructionHealthPercent": "Fence construction health (%)",
        "Sandbox_B47_ConstructionHealthPercent_tooltip": "Health of newly constructed B47 fence sections and corners, as a percentage of normal health. Default: 100. Range: 10 to 500. Existing fences and nonblocking standalone posts are unchanged. The server setting is authoritative.",
    }
    for language in LANGUAGES:
        path = MOD / f"media/lua/shared/Translate/{language}"
        path.mkdir(parents=True, exist_ok=True)
        for filename, values in [("IG_UI.json", translations), ("Sandbox.json", sandbox)]:
            (path / filename).write_text(json.dumps(values, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    for variant, index in [("PlainSection", 66), ("PostEndedSection", 67), ("Corner", 68), ("Post", 69)]:
        img = Image.open(ROOT / f"docs/evidence/fencing_01_{index}.png").convert("RGBA")
        box = img.getbbox()
        img = img.crop(box)
        img.thumbnail((60, 60), Image.Resampling.LANCZOS)
        icon = Image.new("RGBA", (64, 64))
        icon.paste(img, ((64-img.width)//2, (64-img.height)//2))
        icon.save(MOD / f"media/textures/Build_WroughtIronFence_{variant}.png")
    print("Applied original B47 expansion; installed Workshop copy untouched")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["version", "implement"])
    args = parser.parse_args()
    set_version() if args.mode == "version" else implement()
