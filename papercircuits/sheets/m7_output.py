"""M7: Output, the only page that talks to the world outside the table.

Up to three signals come in at IN1 to IN3, each through a 22 kΩ resistor onto the MIX lane,
so they add without fighting. C1 (1 µF, no polarity) passes the sound but blocks the
battery's DC, and R4 (4.7 kΩ) to GND sets the level: a 0–4.5 V square wave from M1 arrives
at OUT as about 0.8 V peak to peak, around line level. OUT and GND go to a 3.5 mm plug,
tip and ring together, sleeve to GND, into a powered speaker's or an amp's line input.

With R4 as the load, C1 lets through everything above about 34 Hz, well below M2's lowest C.
"""

from .. import elements as E
from .. import lesson
from .. import module
from .. import schematic as sch
from .. import standard as S
from ..draw import INK, Sheet, style
from ..provisional import HEADER_STATUS, T0

PAGE_ID = "M7"

# Waiting on the T0 contact tests.
LEAD_STEP = f"Solder every lead to its lane, or hold it flat with a small patch of copper tape. {T0}"
LOOP_STEP = f"Solder a patch loop upright on each loop mark: IN1 to IN3, OUT and GND. {T0}"

R_MIX, R_LOAD, CAP = "22 kΩ", "4.7 kΩ", "1 µF"

IN_Y = (68.0, 92.0, 116.0)
IN_X = (56.0, 94.5)
MIX_X = 107.0
OUT_X = 122.0
OUT_SPAN = (128.0, 160.0)
CAP_Y = 136.0
SAFETY = (134.0, 56.0, 183.0, 94.0)


def build(path):
    sh = Sheet(path, "M7 Output")
    E.header(sh, PAGE_ID, "M7  Output",
             "Mix up to three signals and send them to a real amp.", status=HEADER_STATUS)
    E.spine(sh)
    module.power_ring(sh)
    _lanes(sh)
    _parts(sh)
    _safety(sh)
    module.need(sh, PAGE_ID, [
        f"R1, R2, R3 {R_MIX} · R4 {R_LOAD}",
        f"C1: {CAP}, no polarity (film or ceramic)",
        "Bare wire for 5 patch loops",
    ], [
        "A 3.5 mm plug-to-clip lead",
        "A powered speaker or amp with a line input",
        "Copper tape, solder, 2-core cable",
    ])
    module.caption(sh, "Patch an oscillator's OUT to IN1. Clip OUT and GND to the 3.5 mm plug, then plug into the amp.")
    _schematic(sh)
    module.steps(sh, PAGE_ID, [
        "Lay the power ring and the five lanes inside it, one piece of tape each.",
        "Place R1 to R3 from each IN lane to the MIX lane, C1 from MIX to OUT, and R4 from OUT down to "
        "the GND rail. All go either way round.",
        LEAD_STEP,
        LOOP_STEP,
        "Join the edge connectors to the pages either side with 2-core cable, or with red and black clip leads.",
    ], [
        "Turn the amp's volume right down. Clip OUT to the plug's tip and ring, and GND to its sleeve. "
        "Plug into the amp's line or AUX input.",
        "Patch M1's OUT to IN1 and play a key, then bring the volume up slowly.",
        "A second oscillator on IN2 plays at the same time: the two notes mix.",
    ])
    E.footer(sh, PAGE_ID)
    sh.save()


def _lanes(sh):
    for y in IN_Y:
        E.lane(sh, [(IN_X[0], y), (IN_X[1], y)])
    E.lane(sh, [(MIX_X, IN_Y[0] - 8), (MIX_X, CAP_Y + 8)])
    E.lane(sh, [(OUT_X, OUT_SPAN[0]), (OUT_X, OUT_SPAN[1])])


def _parts(sh):
    for i, y in enumerate(IN_Y, 1):
        E.patch_loop(sh, IN_X[0] + 8, y, f"IN{i}", side="above")
        E.resistor(sh, (IN_X[1] + MIX_X - S.TAPE_W / 2) / 2, y, vertical=False, lead=12, label=f"R{i}")
    E.ceramic_cap(sh, (MIX_X + OUT_X) / 2, CAP_Y, lead=8, label="C1")
    gnd_edge = S.RING_BOTTOM - S.TAPE_W / 2
    E.resistor(sh, OUT_X, (OUT_SPAN[1] + gnd_edge) / 2, vertical=True, lead=12, label="R4")
    E.patch_loop(sh, OUT_X, 146, "OUT")
    E.patch_loop(sh, 150, S.RING_BOTTOM, "GND")


def _safety(sh):
    x0, y0, x1, y1 = SAFETY
    sh.rect(x0, y0, x1, y1, stroke=INK, width=0.4, radius=1.2)
    h = sh.paragraph(x0 + 2.5, y0 + 2.5, x1 - x0 - 5, "<b>Before you plug in</b>", style(7.5))
    sh.paragraph(x0 + 2.5, y0 + 3.5 + h, x1 - x0 - 5,
                 "Only a powered speaker's or an amp's line (AUX) input.<br/><br/>"
                 "Turn its volume right down first, then bring it up slowly.<br/><br/>"
                 "Never headphones, and never a bare speaker.",
                 style(7, leading=8.6))


def _schematic(sh):
    lesson.schematic_panel(sh)
    rows, mix, out_x, gnd = (218.0, 230.0, 242.0), 62.0, 80.0, 270.0
    for i, y in enumerate(rows, 1):
        sch.terminal(sh, 40, y, "", 0)
        sh.text(40, y - 3.4, f"IN{i}", size=6.5, bold=True, align="center")
        sch.resistor_h(sh, 40.8, mix, y, f"R{i}", R_MIX if i == len(rows) else "", box_w=7)
        if i > 1:
            sch.junction(sh, mix, y)
    sch.wire(sh, [(mix, rows[0]), (mix, 254)])
    sch.capacitor_h(sh, mix, out_x, 254, "C1", CAP)
    sch.junction(sh, out_x, 254)
    sch.wire(sh, [(out_x, 254), (93.2, 254)])
    sch.terminal(sh, 94, 254, "OUT", label_y=250.4, align="right")
    sch.resistor(sh, out_x, 254, gnd, "R4", R_LOAD)
    sch.wire(sh, [(40.8, gnd), (out_x, gnd)])
    sch.terminal(sh, 40, gnd, "GND", label_y=gnd + 5)
    lesson.schematic_note(sh, "OUT and GND go to the plug: tip and ring to OUT.")
