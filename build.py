"""Build every sheet into out/, PNG previews into docs/img/, and the README's two
pictures from those previews: the headline image and the synth table.

Run with: uv run build.py
CI runs:  uv run build.py --check   (PDFs only, then checks the previews aren't stale)
"""

import hashlib
import importlib
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
OUT = ROOT / "out"
PREVIEWS = ROOT / "docs" / "img"
FINGERPRINTS = PREVIEWS / "previews.sha256"


@dataclass(frozen=True)
class SheetSpec:
    filename: str
    module: str

    def __post_init__(self):
        if Path(self.filename).name != self.filename or not self.filename.endswith(".pdf"):
            raise ValueError(f"invalid sheet output name: {self.filename!r}")

    @property
    def build(self):
        module_name = f"papercircuits.sheets.{self.module}"
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError as error:
            if error.name != module_name:
                raise
            raise ModuleNotFoundError(f"registered sheet module does not exist: {module_name}") from error
        builder = getattr(module, "build", None)
        if not callable(builder):
            raise TypeError(f"{module_name} has no callable build")
        return builder


# The single, ordered registration point for every generated sheet.
SHEETS = (
    SheetSpec("template.pdf", "template"),
    SheetSpec("T0-contact-tests.pdf", "t0_contact_tests"),
    SheetSpec("T1-pencil-contacts.pdf", "t1_pencil_contacts"),
    SheetSpec("T2-two-sided.pdf", "t2_two_sided"),
    SheetSpec("T3-oxide-wafer.pdf", "t3_oxide_wafer"),
    SheetSpec("P1-power.pdf", "p1_power"),
    SheetSpec("L01-led-polarity.pdf", "l01_led_polarity"),
    SheetSpec("L02-and-or.pdf", "l02_and_or"),
    SheetSpec("L03-pencil-resistor.pdf", "l03_pencil_resistor"),
    SheetSpec("L04-resistors.pdf", "l04_resistors"),
    SheetSpec("L05-series-parallel.pdf", "l05_series_parallel"),
    SheetSpec("L06-diodes.pdf", "l06_diodes"),
    SheetSpec("L07-dividers.pdf", "l07_dividers"),
    SheetSpec("L08-capacitor.pdf", "l08_capacitor"),
    SheetSpec("M1-oscillator.pdf", "m1_oscillator"),
    SheetSpec("M2-keyboard.pdf", "m2_keyboard"),
    SheetSpec("M3-pencil-ribbon.pdf", "m3_pencil_ribbon"),
    SheetSpec("M4-light-pitch.pdf", "m4_light_pitch"),
    SheetSpec("M5-pulse.pdf", "m5_pulse"),
    SheetSpec("M6-tone.pdf", "m6_tone"),
    SheetSpec("M7-output.pdf", "m7_output"),
)


def validate_registry(sheets=SHEETS):
    names = [sheet.filename for sheet in sheets]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ValueError("duplicate sheet output names: " + ", ".join(duplicates))


def main(argv):
    check = "--check" in argv
    phases = [arg.split("=", 1)[1] for arg in argv if arg.startswith("--phase=")]
    unknown = {arg for arg in argv if arg != "--check" and not arg.startswith("--phase=")}
    if unknown:
        print("Unknown option(s): " + ", ".join(sorted(unknown)))
        return 2
    if check and phases:
        print("--check and --phase cannot be combined")
        return 2
    if len(phases) > 1 or (phases and phases[0] not in {"pdfs", "previews", "composites"}):
        print("--phase must be one of: pdfs, previews, composites")
        return 2
    validate_registry()
    if check:
        return verify_artifacts()
    return update_artifacts(phases[0] if phases else "all")


def generate_pdfs(out):
    """PDF phase: build every registered sheet into `out`."""
    out.mkdir(parents=True, exist_ok=True)
    for sheet in SHEETS:
        path = out / sheet.filename
        sheet.build(path)
        print("wrote", _display(path))


def render_previews(out=OUT, previews=PREVIEWS, executable=None):
    """Preview phase: render the generated PDFs. Returns False if Poppler is unavailable."""
    executable = executable or shutil.which("pdftoppm")
    if executable is None:
        return False
    previews.mkdir(parents=True, exist_ok=True)
    for sheet in SHEETS:
        path = out / sheet.filename
        try:
            subprocess.run([executable, "-png", "-r", "90", str(path), str(previews / path.stem)], check=True)
        except subprocess.CalledProcessError as error:
            raise RuntimeError(f"preview phase failed for {sheet.filename}") from error
    return True


def update_artifacts(phase="all"):
    """Stage a phase completely, then atomically replace each destination artifact."""
    with tempfile.TemporaryDirectory(prefix="papercircuits-build-") as directory:
        staging = Path(directory)
        staged_out, staged_previews = staging / "out", staging / "img"
        if phase in {"all", "pdfs"}:
            generate_pdfs(staged_out)
        if phase in {"all", "previews"}:
            pdf_source = staged_out if phase == "all" else OUT
            if not render_previews(pdf_source, staged_previews):
                raise RuntimeError("preview phase requires pdftoppm from Poppler")
            write_fingerprints(pdf_source, staged_previews / FINGERPRINTS.name)
        if phase == "all":
            compose_images(staged_previews)
        elif phase == "composites":
            staged_previews.mkdir()
            for stem in set(HERO_PAGES + SYNTH_PAGES):
                source = PREVIEWS / f"{stem}-1.png"
                if source.exists():
                    shutil.copy2(source, staged_previews / source.name)
            compose_images(staged_previews)

        if phase in {"all", "pdfs"}:
            publish_files(staged_out, OUT)
        if phase in {"all", "previews"}:
            publish_files(staged_previews, PREVIEWS)
        elif phase == "composites":
            publish_files(staged_previews, PREVIEWS, names={"hero.png", "synth-table.png"})
    return 0


def publish_files(source, destination, names=None):
    """Publish staged files with an atomic replace for each destination path."""
    destination.mkdir(parents=True, exist_ok=True)
    paths = [path for path in source.iterdir() if path.is_file() and (names is None or path.name in names)]
    for path in paths:
        target = destination / path.name
        temporary = target.with_name(f".{target.name}.tmp")
        shutil.copy2(path, temporary)
        temporary.replace(target)


def verify_artifacts():
    """Non-mutating check: build in a temporary directory and compare committed artifacts."""
    with tempfile.TemporaryDirectory(prefix="papercircuits-check-") as directory:
        generated = Path(directory)
        generate_pdfs(generated)
        problems = compare_pdfs(generated, OUT)
        problems += preview_problems(generated, FINGERPRINTS)
    if problems:
        print("Artifact check failed:")
        for problem in problems:
            print(" -", problem)
        print("Run `uv run build.py` with pdftoppm installed, then commit out/ and docs/img/.")
        return 1
    print("Committed PDFs match the build; previews match their PDFs.")
    return 0


def compare_pdfs(generated, committed):
    expected = {sheet.filename for sheet in SHEETS}
    present = {path.name for path in committed.glob("*.pdf")} if committed.exists() else set()
    problems = [f"missing committed PDF: {name}" for name in sorted(expected - present)]
    problems += [f"unexpected committed PDF: {name}" for name in sorted(present - expected)]
    problems += [
        f"committed PDF differs: {name}"
        for name in sorted(expected & present)
        if (generated / name).read_bytes() != (committed / name).read_bytes()
    ]
    return problems


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_fingerprints(out=OUT, fingerprints=FINGERPRINTS):
    """Record which PDF each preview was rendered from. Poppler's PNGs differ between
    platforms, so CI compares these fingerprints instead of re-rendering."""
    lines = [f"{_sha256(out / sheet.filename)}  out/{sheet.filename}" for sheet in SHEETS]
    fingerprints.write_text("\n".join(lines) + "\n")
    print("wrote", _display(fingerprints))


def preview_problems(out=OUT, fingerprints=FINGERPRINTS):
    """Describe previews whose recorded source hash differs from generated PDFs."""
    recorded = {}
    if not fingerprints.exists():
        return ["preview fingerprint file is missing"]
    for line_number, line in enumerate(fingerprints.read_text().splitlines(), 1):
        try:
            digest, name = line.split("  ", 1)
        except ValueError:
            return [f"malformed preview fingerprint on line {line_number}"]
        recorded[name] = digest
    return [
        f"preview is stale or unrecorded: {sheet.filename}"
        for sheet in SHEETS
        if recorded.get(f"out/{sheet.filename}") != _sha256(out / sheet.filename)
    ]


def _display(path):
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


HERO_PAGES = ("L01-led-polarity", "L02-and-or", "L03-pencil-resistor", "L08-capacitor")
# The paper synth laid out on the table in signal order: controller, beat, tone, filter, output.
SYNTH_PAGES = ("M2-keyboard", "M5-pulse", "M1-oscillator", "M6-tone", "M7-output")


def _page_row(stems, name, width, gap, border, previews=PREVIEWS):
    """A row of page previews on a light backdrop. Returns the canvas and each page's frame
    (x0, x1), or None if a preview is missing."""
    pages = [previews / f"{stem}-1.png" for stem in stems]
    missing = [path.name for path in pages if not path.exists()]
    if missing:
        raise FileNotFoundError(f"composite phase cannot build {name}; missing previews: {', '.join(missing)}")
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


def _save(canvas, name, previews=PREVIEWS):
    path = previews / name
    canvas.save(path, optimize=True)
    print("wrote", _display(path))


def hero(width=400, gap=28, border=2, previews=PREVIEWS):
    """Four lesson pages, for the top of the README."""
    canvas, _ = _page_row(HERO_PAGES, "hero.png", width, gap, border, previews)
    if canvas:
        _save(canvas, "hero.png", previews)


def synth_table(width=300, gap=56, border=2, previews=PREVIEWS):
    """The synth's pages side by side, with an arrow for the sound in each gap."""
    canvas, frames = _page_row(SYNTH_PAGES, "synth-table.png", width, gap, border, previews)
    if not canvas:
        return
    draw = ImageDraw.Draw(canvas)
    y = canvas.height // 2
    for (_, right), (left, _) in zip(frames, frames[1:]):
        x0, x1 = right + 10, left - 10
        draw.line([(x0, y), (x1 - 14, y)], fill="#b87333", width=6)
        draw.polygon([(x1, y), (x1 - 18, y - 12), (x1 - 18, y + 12)], fill="#b87333")
    _save(canvas, "synth-table.png", previews)


def compose_images(previews=PREVIEWS):
    """Composite phase: rebuild the two README images from rendered previews."""
    hero(previews=previews)
    synth_table(previews=previews)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
