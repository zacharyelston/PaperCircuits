"""Build every sheet into out/, PNG previews into docs/img/, and the README's headline
image from those previews.

Run with: uv run build.py
CI runs:  uv run build.py --check   (PDFs only, then checks the previews aren't stale)
"""

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

from papercircuits.sheets import (
    l01_led_polarity,
    l02_and_or,
    l03_pencil_resistor,
    l04_resistors,
    l05_series_parallel,
    l06_diodes,
    l07_dividers,
    l08_capacitor,
    p1_power,
    t0_contact_tests,
    t1_pencil_contacts,
    template,
)

ROOT = Path(__file__).parent
OUT = ROOT / "out"
PREVIEWS = ROOT / "docs" / "img"
FINGERPRINTS = PREVIEWS / "previews.sha256"

SHEETS = {
    "template.pdf": template.build,
    "T0-contact-tests.pdf": t0_contact_tests.build,
    "T1-pencil-contacts.pdf": t1_pencil_contacts.build,
    "P1-power.pdf": p1_power.build,
    "L01-led-polarity.pdf": l01_led_polarity.build,
    "L02-and-or.pdf": l02_and_or.build,
    "L03-pencil-resistor.pdf": l03_pencil_resistor.build,
    "L04-resistors.pdf": l04_resistors.build,
    "L05-series-parallel.pdf": l05_series_parallel.build,
    "L06-diodes.pdf": l06_diodes.build,
    "L07-dividers.pdf": l07_dividers.build,
    "L08-capacitor.pdf": l08_capacitor.build,
}


def main(argv):
    check = "--check" in argv
    OUT.mkdir(exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    render = not check and shutil.which("pdftoppm") is not None
    if not check and not render:
        print("pdftoppm not found; skipping previews, so docs/img/ will be out of date")
    for name, build in SHEETS.items():
        path = OUT / name
        build(path)
        print("wrote", path.relative_to(ROOT))
        if render:
            subprocess.run(["pdftoppm", "-png", "-r", "90", str(path), str(PREVIEWS / path.stem)], check=True)
    if check:
        return check_previews()
    if render:
        write_fingerprints()
    hero()
    return 0


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_fingerprints():
    """Record which PDF each preview was rendered from. Poppler's PNGs differ between
    platforms, so CI compares these fingerprints instead of re-rendering."""
    lines = [f"{_sha256(OUT / name)}  out/{name}" for name in SHEETS]
    FINGERPRINTS.write_text("\n".join(lines) + "\n")
    print("wrote", FINGERPRINTS.relative_to(ROOT))


def check_previews():
    """0 if every preview was rendered from the PDF the code builds now."""
    recorded = {}
    if FINGERPRINTS.exists():
        for line in FINGERPRINTS.read_text().splitlines():
            digest, name = line.split("  ", 1)
            recorded[name] = digest
    stale = [name for name in SHEETS if recorded.get(f"out/{name}") != _sha256(OUT / name)]
    if stale:
        print("Previews are out of date for: " + ", ".join(stale))
        print("Run `uv run build.py` with pdftoppm installed, then commit out/ and docs/img/.")
        return 1
    print("Previews match the PDFs they were rendered from.")
    return 0


HERO_PAGES = ("L01-led-polarity", "L02-and-or", "L03-pencil-resistor", "L08-capacitor")


def hero(width=400, gap=28, border=2):
    """A row of lesson-page previews on a light backdrop, for the top of the README."""
    pages = [PREVIEWS / f"{stem}-1.png" for stem in HERO_PAGES]
    if not all(p.exists() for p in pages):
        print("  previews missing; skipped hero.png")
        return
    thumbs = []
    for p in pages:
        im = Image.open(p).convert("RGB")
        thumbs.append(im.resize((width, round(im.height * width / im.width)), Image.LANCZOS))
    tall = max(t.height for t in thumbs)
    canvas = Image.new("RGB", (gap + len(thumbs) * (width + 2 * border + gap), tall + 2 * border + 2 * gap), "#f1efe8")
    x = gap
    for t in thumbs:
        canvas.paste(Image.new("RGB", (width + 2 * border, t.height + 2 * border), "#c9c6bd"), (x, gap))
        canvas.paste(t, (x + border, gap + border))
        x += width + 2 * border + gap
    path = PREVIEWS / "hero.png"
    canvas.save(path, optimize=True)
    print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
