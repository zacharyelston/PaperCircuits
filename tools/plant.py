"""Plant a mistake in a sheet and see whether the build catches it.

    uv run tools/plant.py l01_led_polarity 'R("R1", 220,' 'R("R1", 4.7e3,'

Builds the sheet with the first argument's text replaced by the second, in memory, into
a scratch PDF; the sheet's file isn't touched. Prints what stopped the build, or says
nothing did. Use it to show a page's check works after moving it to the three layers.
"""

import sys
import tempfile
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import papercircuits.sheets  # noqa: E402, F401


def plant(sheet, old, new):
    path = ROOT / "papercircuits" / "sheets" / f"{sheet}.py"
    src = path.read_text()
    if src.count(old) != 1:
        return f"can't plant: the text is in {path.name} {src.count(old)} times, not once"
    mod = types.ModuleType(f"papercircuits.sheets.{sheet}_planted")
    mod.__package__, mod.__file__ = "papercircuits.sheets", str(path)
    exec(compile(src.replace(old, new), f"{sheet} (planted)", "exec"), mod.__dict__)
    try:
        mod.build(Path(tempfile.mkdtemp()) / f"{sheet}.pdf")
    except Exception as e:
        lines = [line.strip() for line in str(e).splitlines()]
        return f"caught: {type(e).__name__}: " + " / ".join(lines[1:] or lines)
    return "NOT caught: the page built"


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    print(plant(*sys.argv[1:]))
