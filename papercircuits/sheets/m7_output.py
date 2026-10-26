"""M7: Output, the only page that talks to the world outside the table.

Up to three signals come in at IN1 to IN3, each through its own resistor (R1 to R3) onto
the MIX lane, so they add without fighting. C1 passes the sound but blocks the battery's
DC, and R4 to GND sets the level: R1 and R4 divide a 0–4.5 V square wave from M1 down to
about 0.8 V peak to peak at OUT, around line level. OUT and GND go to a 3.5 mm plug, tip
and ring together, sleeve to GND, into a powered speaker's or an amp's line input. With
R4 as its load, C1 lets through everything above about 34 Hz, well below M2's lowest C.

The page is built in three layers: CIRCUIT says what it is, _copper() and _schematic()
say where things go, and m7_output.md holds the words.
"""

from .. import elements as E
from .. import lesson, module
from .. import schematic as sch
from .. import standard as S
from ..circuit import C, Circuit, R
from ..draw import INK, Sheet, style
from ..placement import Placement
from ..provisional import HEADER_STATUS
from ..words import Words, number

PAGE_ID = "M7"
CIRCUIT = Circuit(
    R("R1", 22e3, "IN1", "MIX"),
    R("R2", 22e3, "IN2", "MIX"),
    R("R3", 22e3, "IN3", "MIX"),
    C("C1", 1e-6, "MIX", "OUT"),
    R("R4", 4.7e3, "OUT", "GND"),
)
WORDS = Words.beside(__file__, CIRCUIT)

INPUTS = (("IN1", "R1", 68.0), ("IN2", "R2", 92.0), ("IN3", "R3", 116.0))
IN_X = (56.0, 94.5)
MIX_X = 107.0
OUT_X = 122.0
OUT_SPAN = (128.0, 160.0)
CAP_Y = 136.0
SAFETY = (134.0, 56.0, 183.0, 94.0)


def build(path):
    sh = Sheet(path, " ".join(WORDS.title.split()))
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, status=HEADER_STATUS)
    E.spine(sh)
    lay = Placement(sh, CIRCUIT)
    _copper(lay)
    _safety(sh)
    need = WORDS.items("You need", loops=len(lay.loops))
    module.need(sh, PAGE_ID, need[:3], need[3:])
    module.caption(sh, WORDS.text("Caption"))
    _schematic(sh, lay)
    module.steps(sh, PAGE_ID, WORDS.items("Build it", lanes=number(lay.laid)), WORDS.items("Play it"))
    E.footer(sh, PAGE_ID)
    lay.check(listed=WORDS.refs("You need"))
    sh.save()


def _copper(lay):
    lay.ring()
    for net, _, y in INPUTS:
        lay.lane(net, [(IN_X[0], y), (IN_X[1], y)])
    lay.lane("MIX", [(MIX_X, INPUTS[0][2] - 8), (MIX_X, CAP_Y + 8)])
    lay.lane("OUT", [(OUT_X, OUT_SPAN[0]), (OUT_X, OUT_SPAN[1])])
    for net, ref, y in INPUTS:
        lay.loop(net, IN_X[0] + 8, y, side="above")
        lay.resistor(ref, (IN_X[1] + MIX_X - S.TAPE_W / 2) / 2, y, vertical=False, lead=12)
    lay.ceramic_cap("C1", (MIX_X + OUT_X) / 2, CAP_Y, lead=8)
    gnd_edge = S.RING_BOTTOM - S.TAPE_W / 2
    lay.resistor("R4", OUT_X, (OUT_SPAN[1] + gnd_edge) / 2, vertical=True, lead=12)
    lay.loop("OUT", OUT_X, 146)
    lay.loop("GND", 150, S.RING_BOTTOM)


def _safety(sh):
    x0, y0, x1, y1 = SAFETY
    sh.rect(x0, y0, x1, y1, stroke=INK, width=0.4, radius=1.2)
    h = sh.paragraph(x0 + 2.5, y0 + 2.5, x1 - x0 - 5, "<b>Before you plug in</b>", style(7.5))
    sh.paragraph(
        x0 + 2.5, y0 + 3.5 + h, x1 - x0 - 5, "<br/><br/>".join(WORDS.items("Before you plug in")), style(7, leading=8.6)
    )


def _schematic(sh, lay):
    lesson.schematic_panel(sh)
    rows, mix, out_x, gnd = (218.0, 230.0, 242.0), 62.0, 80.0, 270.0
    for i, ((net, ref, _), y) in enumerate(zip(INPUTS, rows), 1):
        r = lay.symbol(ref)
        sch.terminal(sh, 40, y, "", 0)
        sh.text(40, y - 3.4, net, size=6.5, bold=True, align="center")
        sch.resistor_h(sh, 40.8, mix, y, r.ref, r.text if i == len(rows) else "", box_w=7)
        if i > 1:
            sch.junction(sh, mix, y)
    sch.wire(sh, [(mix, rows[0]), (mix, 254)])
    c1 = lay.symbol("C1")
    sch.capacitor_h(sh, mix, out_x, 254, c1.ref, c1.text)
    sch.junction(sh, out_x, 254)
    sch.wire(sh, [(out_x, 254), (93.2, 254)])
    sch.terminal(sh, 94, 254, "OUT", label_y=250.4, align="right")
    r4 = lay.symbol("R4")
    sch.resistor(sh, out_x, 254, gnd, r4.ref, r4.text)
    sch.wire(sh, [(40.8, gnd), (out_x, gnd)])
    sch.terminal(sh, 40, gnd, "GND", label_y=gnd + 5)
    lesson.schematic_note(sh, WORDS.text("Schematic note"))
