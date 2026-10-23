"""Build every sheet into out/ and PNG previews into docs/img/.

Run with: uv run build.py
"""

import shutil
import subprocess
from pathlib import Path

from papercircuits.sheets import l01_led_polarity, p1_power, t0_contact_tests, template

ROOT = Path(__file__).parent
OUT = ROOT / "out"
PREVIEWS = ROOT / "docs" / "img"

SHEETS = {
    "template.pdf": template.build,
    "T0-contact-tests.pdf": t0_contact_tests.build,
    "P1-power.pdf": p1_power.build,
    "L01-led-polarity.pdf": l01_led_polarity.build,
}


def main():
    OUT.mkdir(exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    for name, build in SHEETS.items():
        path = OUT / name
        build(path)
        print("wrote", path.relative_to(ROOT))
        if shutil.which("pdftoppm"):
            prefix = PREVIEWS / path.stem
            subprocess.run(["pdftoppm", "-png", "-r", "90", str(path), str(prefix)], check=True)
        else:
            print("  pdftoppm not found; skipped previews")


if __name__ == "__main__":
    main()
