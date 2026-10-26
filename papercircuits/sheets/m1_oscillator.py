"""M1: Oscillator, the paper synth's sound source.

A two-transistor astable multivibrator. Q1 and Q2 take turns: each one's collector, through
a capacitor, switches the other off for a while, so OUT (Q2's collector) flips between GND
and V+ hundreds of times a second. That square wave is the tone.

Q1's base gets its current from R3, a fixed 10 kΩ. Q2's base gets it only through PITCH:
a controller (M2's keyboard, M3's pencil ribbon, M4's light sensor) puts a resistance
between V+ and PITCH. More resistance makes Q2's off-time longer, so the note is lower.
Nothing patched means no current, so the oscillator is silent: touching a key starts the
note. R4 keeps PITCH from ever reaching Q2's base with no resistance at all.

With C = 100 nF: f ≈ 1 / (0.693 × 100 nF × (10 kΩ + 4.7 kΩ + R_pitch)), about 980 Hz with
nothing in the way, 260 Hz at 40 kΩ.

The circuit can't be laid in tape without one crossing: both rails come from outside the
loop of parts. Q1's base lane passes under Q2's at one insulated crossing.

The page is built in three layers: CIRCUIT says what it is, _lanes(), _parts() and
_schematic() say where things go, and m1_oscillator.md holds the words.
"""

from .. import elements as E
from .. import lesson, module
from .. import schematic as sch
from .. import standard as S
from ..circuit import LED, C, Circuit, Q, R
from ..draw import Sheet
from ..placement import Placement
from ..provisional import HEADER_STATUS
from ..words import Words, number

PAGE_ID = "M1"
CIRCUIT = Circuit(
    R("R1", 1e3, "V+", "N1"),
    LED("LED1", anode="N1", cathode="Q1C", note="red, 5 mm"),  # in Q1's collector path
    R("R2", 1e3, "V+", "OUT"),
    R("R3", 10e3, "V+", "Q1B"),
    R("R4", 4.7e3, "PITCH", "Q2B"),
    C("C1", 100e-9, "Q1C", "Q2B"),
    C("C2", 100e-9, "Q1B", "OUT"),
    Q("Q1", "2N3904", e="GND", b="Q1B", c="Q1C"),
    Q("Q2", "2N3904", e="GND", b="Q2B", c="OUT"),
)
WORDS = Words.beside(__file__, CIRCUIT)

COL_A, COL_B, COL_C, COL_D = 64.0, 80.0, 140.0, 155.5  # Q1 collector, PITCH, Q1 base, Q2 collector
RAIL_EDGE = S.RING_TOP + S.TAPE_W / 2
LANE_TOP = RAIL_EDGE + 10
CAP_Y = 110.0
B1_Y, B2_Y = 153.0, 163.0  # where Q1's and Q2's base lanes run sideways
Q1, Q2 = (70.0, 165.0), (150.0, 168.0)


def build(path):
    sh = Sheet(path, " ".join(WORDS.title.split()))
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, status=HEADER_STATUS)
    E.spine(sh)
    lay = Placement(sh, CIRCUIT)
    lay.ring()
    _lanes(lay)
    _parts(lay)
    need = WORDS.items("You need", loops=len(lay.loops))
    module.need(sh, PAGE_ID, need[:3], need[3:])
    module.caption(sh, WORDS.text("Caption"))
    _schematic(sh, lay)
    module.steps(sh, PAGE_ID, WORDS.items("Build it", lanes=number(lay.laid)), WORDS.items("Play it"))
    E.footer(sh, PAGE_ID)
    lay.check(listed=WORDS.refs("You need"))
    sh.save()


def _lanes(lay):
    lay.lane("N1", [(COL_A, LANE_TOP), (COL_A, 75)])  # R1 to LED1
    lay.lane("Q1C", [(COL_A, 85), (COL_A, 158)])  # Q1 collector
    lay.lane("PITCH", [(COL_B, RAIL_EDGE + 3.5), (COL_B, 70)])  # PITCH
    b1 = lay.lane("Q1B", [(COL_C, LANE_TOP), (COL_C, B1_Y), (70, B1_Y)])  # Q1 base, the lower lane
    E.crossing(lay.sh, COL_B, B1_Y)
    b2 = lay.lane("Q2B", [(COL_B, 80), (COL_B, B2_Y), (146, B2_Y)])  # Q2 base, crossing over it
    lay.sh.allow(b1, b2, 0)
    lay.lane("OUT", [(COL_D, LANE_TOP), (COL_D, 158)])  # Q2 collector, OUT


def _parts(lay):
    r_cy = (RAIL_EDGE + LANE_TOP) / 2
    lay.resistor("R1", COL_A, r_cy, vertical=True, lead=12)
    lay.led("LED1", COL_A, 80, anode="up", lead_anode=12, lead_cathode=11)
    lay.resistor("R4", COL_B, 75, vertical=True, lead=12)
    lay.resistor("R3", COL_C, r_cy, vertical=True, lead=12)
    lay.resistor("R2", COL_D, r_cy, vertical=True, lead=12)
    lay.ceramic_cap("C1", (COL_A + COL_B) / 2, CAP_Y, lead=8)
    lay.ceramic_cap("C2", (COL_C + COL_D) / 2, CAP_Y, lead=8)
    gnd = S.RING_BOTTOM - 1
    lay.transistor("Q1", *Q1, {"E": (Q1[0], gnd), "B": (Q1[0] + 2, B1_Y), "C": (COL_A, 157)})
    lay.transistor("Q2", *Q2, {"E": (Q2[0], gnd), "B": (Q2[0] - 7, B2_Y), "C": (COL_D, 157)})
    lay.loop("PITCH", COL_B, 60)
    lay.loop("V+", 104, S.RING_TOP)
    lay.loop("OUT", COL_D, 72)


def _schematic(sh, lay):
    lesson.schematic_panel(sh)
    top, bottom = 214.0, 272.0
    a, b, c, d = 44.0, 58.0, 72.0, 88.0
    sch.terminal(sh, 40, top, "V+", label_y=top - 3.4)
    sch.wire(sh, [(40.8, top), (d, top), (d, top + 0.01)])
    for x in (a, b):
        sch.junction(sh, x, top)

    r1 = lay.symbol("R1")
    sch.resistor(sh, a, top, 228, r1.ref, r1.text)
    sch.led(sh, a, 228, 244, lay.symbol("LED1").ref)
    _, c1, e1 = sch.npn(sh, a + 1.6, 256, lay.symbol("Q1").ref, base="right")
    sch.wire(sh, [(a, 244), c1])
    sch.wire(sh, [e1, (a, bottom)])

    r3 = lay.symbol("R3")
    sch.resistor(sh, b, top, 230, r3.ref, r3.text)
    sch.wire(sh, [(b, 230), (b, 256), (a + 1.6 + 4.5, 256)])

    sch.terminal(sh, c, 218, "", 0)
    sh.text(c + 2, 218.6, "PITCH", size=6.5, bold=True)
    r4 = lay.symbol("R4")
    sch.resistor(sh, c, 218.8, 233, r4.ref, r4.text)
    b2, c2, e2 = sch.npn(sh, d - 1.6, 256, lay.symbol("Q2").ref, base="left")
    sch.wire(sh, [(c, 233), (c, 256), b2])

    r2 = lay.symbol("R2")
    sch.resistor(sh, d, top, 230, r2.ref, r2.text)
    sch.wire(sh, [(d, 230), c2])
    sch.wire(sh, [e2, (d, bottom)])

    sch.capacitor_h(sh, a, 60, 247, lay.symbol("C1").ref)
    sch.wire(sh, [(60, 247), (c, 247)])
    sch.capacitor_h(sh, 76, d, 237, lay.symbol("C2").ref)
    sch.wire(sh, [(76, 237), (b, 237)])
    for x, y in ((a, 247), (c, 247), (d, 237), (b, 237)):
        sch.junction(sh, x, y)
    sch.wire(sh, [(d, 241), (93.2, 241)])
    sch.junction(sh, d, 241)
    sch.terminal(sh, 94, 241, "OUT", label_y=246.4, align="right")

    sch.wire(sh, [(40.8, bottom), (d, bottom), (d, bottom - 0.01)])
    sch.terminal(sh, 40, bottom, "GND", label_y=bottom + 5)
    lesson.schematic_note(sh, WORDS.text("Schematic note"))
