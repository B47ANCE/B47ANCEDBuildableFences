"""Prepare a metadata-only update; run SteamCMD separately to publish it."""
import argparse
from pathlib import Path


def vdf_string(value):
    # SteamCMD submits escaped newline text literally; quoted multiline values
    # preserve the actual paragraphs used by Steam Workshop BBCode.
    return str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\r\n", "\n").replace("\r", "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--visibility", choices=("Public", "FriendsOnly", "Private", "Unlisted"), required=True,
                        help="Explicit intended visibility; avoids SteamCMD defaults on metadata-only updates")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    item = (root / "WORKSHOP_ID.txt").read_text().strip()
    version = (root / "VERSION").read_text().strip()
    description = (root / "WORKSHOP_DESCRIPTION.txt").read_text(encoding="utf-8").strip()
    if not item.isdigit() or len(item) < 7:
        raise ValueError("A confirmed existing Workshop ID is required")
    if not description.startswith(f"[b]Version {version}[/b]"):
        raise ValueError("Description must identify the current version")
    if "\\n" in description or len(description.encode("utf-8")) > 8000:
        raise ValueError("Description contains literal newline escapes or exceeds Steam's limit")
    fields = {"appid": "108600", "publishedfileid": item, "description": description}
    fields["visibility"] = {"Public": "0", "FriendsOnly": "1", "Private": "2", "Unlisted": "3"}[args.visibility]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        output.write('"workshopitem"\n{\n')
        for key, value in fields.items():
            output.write(f'    "{key}" "{vdf_string(value)}"\n')
        output.write("}\n")
    print(f"Prepared metadata for {item}: {len(description.encode('utf-8'))} UTF-8 bytes")
    print(args.output.resolve())


if __name__ == "__main__":
    main()
