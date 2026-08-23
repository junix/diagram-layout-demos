from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"
SOURCES = ROOT / "sources"
CASES = [
    ("architecture", ["dot", "-Tsvg", str(SOURCES / "architecture.dot"), "-o"]),
    ("knowledge", ["neato", "-Tsvg", str(SOURCES / "knowledge.dot"), "-o"]),
    ("incident", ["d2", "--theme=200", "--pad=48", str(SOURCES / "incident.d2")]),
]


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, check=True, cwd=ROOT)


def main() -> None:
    for binary in ("dot", "neato", "d2", "rsvg-convert"):
        if not shutil.which(binary):
            raise SystemExit(f"missing renderer: {binary}")
    OUT.mkdir(exist_ok=True)
    report = []
    for name, command in CASES:
        svg = OUT / f"{name}.svg"
        png = OUT / f"{name}-transparent.png"
        if name == "incident":
            run([*command, str(svg)])
            raw_svg = svg.read_text()
            raw_svg, replacements = re.subn(
                r'(<svg class="[^"]*d2-svg"[^>]*>)<rect[^>]*class=" fill-[^"]+"[^>]*/>',
                r"\1",
                raw_svg,
                count=1,
            )
            if replacements != 1:
                raise SystemExit("D2 output background contract changed")
            svg.write_text(raw_svg)
        else:
            run([*command, str(svg)])
        run(["rsvg-convert", "--background-color", "none", "--width", "1600", "--keep-aspect-ratio", "--output", str(png), str(svg)])
        image = Image.open(png).convert("RGBA")
        alpha = image.getchannel("A")
        histogram = alpha.histogram()
        pixels = image.width * image.height
        transparent = histogram[0]
        visible = pixels - sum(histogram[:16])
        colors = image.getcolors(maxcolors=pixels) or []
        colorful = sum(count for count, rgba in colors if rgba[3] > 16 and max(rgba[:3]) - min(rgba[:3]) > 24)
        if transparent < pixels * 0.05 or visible < pixels * 0.03 or colorful < 1500:
            raise SystemExit(f"{name}: failed pixel contract t={transparent} v={visible} c={colorful}")
        item = {"scene": name, "size": image.size, "transparent_pct": round(100 * transparent / pixels, 1), "visible_pct": round(100 * visible / pixels, 1), "colorful": colorful}
        print(json.dumps(item))
        report.append(item)
    print(json.dumps({"validated": report}, indent=2))


if __name__ == "__main__":
    main()
