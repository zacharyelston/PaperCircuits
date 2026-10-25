"""Build every sheet into out/, PNG previews into docs/img/, and the README's two
pictures from those previews: the headline image and the synth table.

Run with: uv run build.py
CI runs:  uv run build.py --check   (PDFs only, then checks the previews aren't stale)
"""

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

from papercircuits.sheets import (
    l01_led_polarity,
    l02_and_or,
    l03_pencil_resistor,
    l04_resistors,
    l05_series_parallel,
    l06_diodes,
    l07_dividers,
    l08_capacitor,
    m1_oscillator,
    m2_keyboard,
    m3_pencil_ribbon,
    m4_light_pitch,
    m5_pulse,
    m6_tone,
    m7_output,
    p1_power,
    t0_contact_tests,
    t1_pencil_contacts,
    t2_two_sided,
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
    "T2-two-sided.pdf": t2_two_sided.build,
    "P1-power.pdf": p1_power.build,
    "L01-led-polarity.pdf": l01_led_polarity.build,
    "L02-and-or.pdf": l02_and_or.build,
    "L03-pencil-resistor.pdf": l03_pencil_resistor.build,
    "L04-resistors.pdf": l04_resistors.build,
    "L05-series-parallel.pdf": l05_series_parallel.build,
    "L06-diodes.pdf": l06_diodes.build,
    "L07-dividers.pdf": l07_dividers.build,
    "L08-capacitor.pdf": l08_capacitor.build,
    "M1-oscillator.pdf": m1_oscillator.build,
    "M2-keyboard.pdf": m2_keyboard.build,
    "M3-pencil-ribbon.pdf": m3_pencil_ribbon.build,
    "M4-light-pitch.pdf": m4_light_pitch.build,
    "M5-pulse.pdf": m5_pulse.build,
    "M6-tone.pdf": m6_tone.build,
    "M7-output.pdf": m7_output.build,
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
    synth_table()
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
# The paper synth laid out on the table in signal order: controller, beat, tone, filter, output.
SYNTH_PAGES = ("M2-keyboard", "M5-pulse", "M1-oscillator", "M6-tone", "M7-output")


def _page_row(stems, name, width, gap, border):
    """A row of page previews on a light backdrop. Returns the canvas and each page's frame
    (x0, x1), or None if a preview is missing."""
    pages = [PREVIEWS / f"{stem}-1.png" for stem in stems]
    if not all(p.exists() for p in pages):
        print(f"  previews missing; skipped {name}")
        return None, []
    thumbs = []
    for p in pages:
        im = Image.open(p).convert("RGB")
        thumbs.append(im.resize((width, round(im.height * width / im.width)), Image.LANCZOS))
    tall = max(t.height for t in thumbs)
    canvas = Image.new("RGB", (gap + len(thumbs) * (width + 2 * border + gap), tall + 2 * border + 2 * gap), "#f1efe8")
    frames = []
    x = gap
    for t in thumbs:
        canvas.paste(Image.new("RGB", (width + 2 * border, t.height + 2 * border), "#c9c6bd"), (x, gap))
        canvas.paste(t, (x + border, gap + border))
        frames.append((x, x + width + 2 * border))
        x += width + 2 * border + gap
    return canvas, frames


def _save(canvas, name):
    path = PREVIEWS / name
    canvas.save(path, optimize=True)
    print("wrote", path.relative_to(ROOT))


def hero(width=400, gap=28, border=2):
    """Four lesson pages, for the top of the README."""
    canvas, _ = _page_row(HERO_PAGES, "hero.png", width, gap, border)
    if canvas:
        _save(canvas, "hero.png")


def synth_table(width=300, gap=56, border=2):
    """The synth's pages side by side, with an arrow for the sound in each gap."""
    canvas, frames = _page_row(SYNTH_PAGES, "synth-table.png", width, gap, border)
    if not canvas:
        return
    draw = ImageDraw.Draw(canvas)
    y = canvas.height // 2
    for (_, right), (left, _) in zip(frames, frames[1:]):
        x0, x1 = right + 10, left - 10
        draw.line([(x0, y), (x1 - 14, y)], fill="#b87333", width=6)
        draw.polygon([(x1, y), (x1 - 18, y - 12), (x1 - 18, y + 12)], fill="#b87333")
    _save(canvas, "synth-table.png")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
