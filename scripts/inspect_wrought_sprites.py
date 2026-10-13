"""Extract only vanilla iron-fence art for inspection and B47 menu icons."""
import io
import struct
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PACK = Path(r"E:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid\media\texturepacks\Tiles2x.pack")


def integer(stream):
    return struct.unpack("<i", stream.read(4))[0]


def string(stream):
    return stream.read(integer(stream)).decode("utf-8")


def extract():
    found = {}
    with PACK.open("rb") as stream:
        assert stream.read(4) == b"PZPK"
        assert integer(stream) == 1
        pages = integer(stream)
        for _ in range(pages):
            page_name = string(stream)
            entries = integer(stream)
            integer(stream)  # alpha flag
            selected = []
            for _ in range(entries):
                name = string(stream)
                values = [integer(stream) for _ in range(8)]
                if name in {f"fencing_01_{i}" for i in range(64, 70)}:
                    selected.append((name, values))
            length = integer(stream)
            if selected:
                page = Image.open(io.BytesIO(stream.read(length))).convert("RGBA")
                for name, (x, y, w, h, ox, oy, fw, fh) in selected:
                    canvas = Image.new("RGBA", (fw, fh))
                    canvas.paste(page.crop((x, y, x+w, y+h)), (ox, oy))
                    found[name] = canvas
                    canvas.save(ROOT / f"docs/evidence/{name}.png")
                    print(name, page_name, (x, y, w, h, ox, oy, fw, fh))
            else:
                stream.seek(length, 1)
    assert len(found) == 6, found.keys()
    sheet = Image.new("RGB", (6 * 160, 340), "#4b5057")
    draw = ImageDraw.Draw(sheet)
    for n, (name, img) in enumerate(sorted(found.items())):
        img.thumbnail((150, 290))
        sheet.paste(img, (n*160+5, 30), img)
        draw.text((n*160+5, 5), name, fill="white")
    sheet.save(ROOT / "docs/evidence/wrought_sprites.png")


if __name__ == "__main__":
    extract()
