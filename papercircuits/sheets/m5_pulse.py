"""M5: Pulse, a beat for the paper synth.

The same two-transistor oscillator as M1, slowed right down: 10 µF capacitors in place of
100 nF, so Q1 and Q2 take turns about twice a second instead of hundreds of times. LED1
sits in Q2's collector path, so it lights whenever Q2 is on.

Q3 is the gate. While Q2 is off, its collector is high, current flows through R5 into
Q3's base, and Q3 holds GATE at GND. Patched to M1's PITCH, that starves Q2 on M1 of base
current, so M1 goes quiet: a rest. While Q2 is on, Q3 lets go, the controller's note
plays, and LED1 lights. The result is the note chopped into a beat.

Q3 only ever sinks the controller's current, under 0.5 mA because M2, M3 and M4 all keep
at least 10 kΩ between V+ and PITCH. R5 (100 kΩ) limits Q3 to a few mA even if GATE is
patched somewhere it shouldn't be. LED1 may glow faintly in the rests: R5's small current
flows through it.

On paper the note lasts about a quarter of a second (R3, 47 kΩ, with C2) and the rest
about a sixth (R4, 22 kΩ, with C1). The same crossing as M1 is needed.

The page is built in three layers: CIRCUIT says what it is, _lanes(), _parts() and
_schematic() say where things go, and m5_pulse.md holds the words.
"""

from .. import elements as E
from .. import lesson, module
from .. import schematic as sch
from .. import standard as S
from ..circuit import CE, LED, Circuit, Q, R
from ..draw import Sheet
from ..placement import Placement
from ..provisional import HEADER_STATUS
from ..words import Words, number

PAGE_ID = "M5"
CIRCUIT = Circuit(
    R("R1", 1e3, "V+", "Q1C"),
    R("R2", 470, "V+", "N1"),
    LED("LED1", anode="N1", cathode="Q2C", note="red, 5 mm"),  # in Q2's collector path
    R("R3", 47e3, "V+", "Q1B"),
    R("R4", 22e3, "V+", "Q2B"),
    CE("C1", 10e-6, plus="Q1C", minus="Q2B"),
    CE("C2", 10e-6, plus="Q2C", minus="Q1B"),
    Q("Q1", "2N3904", e="GND", b="Q1B", c="Q1C"),
    Q("Q2", "2N3904", e="GND", b="Q2B", c="Q2C"),
    R("R5", 100e3, "Q2C", "Q3B"),
    Q("Q3", "2N3904", e="GND", b="Q3B", c="GATE"),
)
WORDS = Words.beside(__file__, CIRCUIT)

COL_A, COL_B, COL_C, COL_D = 60.0, 76.0, 136.0, 151.5  # Q1 collector, Q2 base, Q1 base, Q2 collector
Q3B_X, GATE_X = 167.5, 179.5
RAIL_EDGE = S.RING_TOP + S.TAPE_W / 2
LANE_TOP = RAIL_EDGE + 10
CAP_Y = 114.0
R5_Y = 140.0
B1_Y, B2_Y = 153.0, 163.0  # where Q1's and Q2's base lanes run sideways
Q1, Q2, Q3 = (66.0, 165.0), (146.0, 168.0), (173.5, 166.0)
GATE_LOOPS = (68.0, 90.0)


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
    lay.lane("Q1C", [(COL_A, LANE_TOP), (COL_A, 158)])  # Q1 collector
    b1 = lay.lane("Q1B", [(COL_C, LANE_TOP), (COL_C, B1_Y), (Q1[0] + 2, B1_Y)])  # Q1 base, the lower lane
    E.crossing(lay.sh, COL_B, B1_Y)
    b2 = lay.lane("Q2B", [(COL_B, LANE_TOP), (COL_B, B2_Y), (Q2[0] - 4, B2_Y)])  # Q2 base, crossing over it
    lay.sh.allow(b1, b2, 0)
    lay.lane("N1", [(COL_D, LANE_TOP), (COL_D, 75)])  # R2 to LED1
    lay.lane("Q2C", [(COL_D, 85), (COL_D, 158)])  # Q2 collector
    lay.lane("Q3B", [(Q3B_X, R5_Y - 4), (Q3B_X, 158)])  # Q3 base
    lay.lane("GATE", [(GATE_X, LANE_TOP), (GATE_X, 158)])  # Q3 collector, GATE


def _parts(lay):
    r_cy = (RAIL_EDGE + LANE_TOP) / 2
    for x, ref in ((COL_A, "R1"), (COL_B, "R4"), (COL_C, "R3"), (COL_D, "R2")):
        lay.resistor(ref, x, r_cy, vertical=True, lead=12)
    lay.led("LED1", COL_D, 80, anode="up", lead_anode=12, lead_cathode=11)
    lay.radial_cap("C1", COL_A, COL_B, CAP_Y)
    lay.radial_cap("C2", COL_D, COL_C, CAP_Y)
    lay.resistor("R5", (COL_D + Q3B_X) / 2, R5_Y, vertical=False, lead=8)
    gnd = S.RING_BOTTOM - 1
    lay.transistor("Q1", *Q1, {"E": (Q1[0], gnd), "B": (Q1[0] + 2, B1_Y), "C": (COL_A, 157)})
    lay.transistor("Q2", *Q2, {"E": (Q2[0], gnd), "B": (Q2[0] - 7, B2_Y), "C": (COL_D, 157)})
    lay.transistor("Q3", *Q3, {"E": (Q3[0], gnd), "B": (Q3B_X, 157), "C": (GATE_X, 157)})
    for y in GATE_LOOPS:
        lay.loop("GATE", GATE_X, y, side="left")


def _schematic(sh, lay):
    lesson.schematic_panel(sh)
    top, bottom = 214.0, 272.0
    a, b, c, d = 44.0, 56.0, 67.0, 78.0
    sch.terminal(sh, 40, top, "V+", label_y=top - 3.4)
    sch.wire(sh, [(40.8, top), (d, top), (d, top + 0.01)])
    for x in (a, b, c):
        sch.junction(sh, x, top)

    r1 = lay.symbol("R1")
    sch.resistor(sh, a, top, 232, r1.ref, r1.text)
    _, c1, e1 = sch.npn(sh, a + 1.6, 256, lay.symbol("Q1").ref, base="right")
    sch.wire(sh, [(a, 232), c1])
    sch.wire(sh, [e1, (a, bottom)])

    r3 = lay.symbol("R3")
    sch.resistor(sh, b, top, 232, r3.ref, r3.text)
    sch.wire(sh, [(b, 232), (b, 256), (a + 1.6 + 4.5, 256)])

    r4 = lay.symbol("R4")
    sch.resistor(sh, c, top, 232, r4.ref, r4.text)
    b2, c2, e2 = sch.npn(sh, d - 1.6, 256, lay.symbol("Q2").ref, base="left")
    sch.wire(sh, [(c, 232), (c, 256), b2])

    r2 = lay.symbol("R2")
    sch.resistor(sh, d, top, 226, r2.ref, r2.text)
    sch.led(sh, d, 226, 238, lay.symbol("LED1").ref)
    sch.wire(sh, [(d, 238), c2])
    sch.wire(sh, [e2, (d, bottom)])

    sch.wire(sh, [(a, 248), (58, 248)])
    sch.capacitor_h(sh, 58, c, 248, lay.symbol("C1").ref, plus="left")
    cap2 = lay.symbol("C2")
    sch.capacitor_h(sh, 68, d, 240, cap2.ref, cap2.text, plus="right")
    sch.wire(sh, [(68, 240), (b, 240)])
    for x, y in ((a, 248), (c, 248), (d, 240), (b, 240)):
        sch.junction(sh, x, y)

    b3, c3, e3 = sch.npn(sh, 90.0, 244, lay.symbol("Q3").ref, base="left")
    sch.resistor_h(sh, d, b3[0], 244, lay.symbol("R5").ref, box_w=4.2)
    sch.junction(sh, d, 244)
    sch.wire(sh, [c3, (c3[0], 231.6)])
    sch.terminal(sh, c3[0], 230, "GATE", label_y=226.2, align="right")
    sch.wire(sh, [e3, (c3[0], bottom)])

    sch.wire(sh, [(40.8, bottom), (c3[0], bottom), (c3[0], bottom - 0.01)])
    sch.terminal(sh, 40, bottom, "GND", label_y=bottom + 5)
    lesson.schematic_note(sh, WORDS.text("Schematic note"))
