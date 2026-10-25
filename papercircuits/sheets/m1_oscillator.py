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
"""

from .. import elements as E
from .. import lesson
from .. import module
from .. import schematic as sch
from .. import standard as S
from ..draw import Sheet
from ..provisional import HEADER_STATUS, T0

PAGE_ID = "M1"

# Waiting on the T0 contact tests.
LEAD_STEP = f"Solder every lead to its lane, or hold it flat with a small patch of copper tape. {T0}"
LOOP_STEP = f"Solder a patch loop upright on each loop mark: V+, PITCH and OUT. {T0}"

R_COLLECTOR, R_BASE, R_SAFE, CAP = "1 kΩ", "10 kΩ", "4.7 kΩ", "100 nF"
TRANSISTOR = "2N3904"

COL_A, COL_B, COL_C, COL_D = 64.0, 80.0, 140.0, 155.5  # Q1 collector, PITCH, Q1 base, Q2 collector
RAIL_EDGE = S.RING_TOP + S.TAPE_W / 2
LANE_TOP = RAIL_EDGE + 10
CAP_Y = 110.0
B1_Y, B2_Y = 153.0, 163.0  # where Q1's and Q2's base lanes run sideways
Q1, Q2 = (70.0, 165.0), (150.0, 168.0)


def build(path):
    sh = Sheet(path, "M1 Oscillator")
    E.header(sh, PAGE_ID, "M1  Oscillator",
             "Two transistors switch each other on and off: that's a tone.", status=HEADER_STATUS)
    E.spine(sh)
    module.power_ring(sh)
    _lanes(sh)
    _parts(sh)
    module.need(sh, PAGE_ID, [
        f"Q1, Q2: {TRANSISTOR} transistors",
        f"C1, C2: {CAP} capacitors, no polarity",
        f"R1, R2 {R_COLLECTOR} · R3 {R_BASE} · R4 {R_SAFE}",
    ], [
        "LED1: red, 5 mm",
        "Bare wire for 3 patch loops; 22 kΩ to test",
        "Copper tape, solder, 2-core cable",
    ])
    module.caption(sh, "Patch PITCH to a controller such as M2's keyboard, and OUT to an IN on M7.")
    _schematic(sh)
    module.steps(sh, PAGE_ID, [
        "Lay the power ring, then the six lanes inside it, one piece of tape each. Fold at the creases.",
        "Where two lanes cross, lay the lower one, stick the insulating patch over it, then lay the upper one.",
        "Place R1 to R4, C1 and C2 across their gaps, either way round. Place LED1 as printed: long leg on the +.",
        "Lay Q1 and Q2 flat face up and bend each leg to its letter: E, B and C.",
        LEAD_STEP,
        LOOP_STEP,
        "Join the edge connectors to the pages either side with 2-core cable, or with red and black clip leads.",
    ], [
        "To test, clip a 22 kΩ resistor between the V+ and PITCH loops: M7 should play a steady note, and LED1 glows.",
        "Then patch PITCH to M2's stylus. More resistance on PITCH gives a lower note.",
    ])
    E.footer(sh, PAGE_ID)
    sh.save()


def _lanes(sh):
    E.lane(sh, [(COL_A, LANE_TOP), (COL_A, 75)])                  # R1 to LED1
    E.lane(sh, [(COL_A, 85), (COL_A, 158)])                       # Q1 collector
    E.lane(sh, [(COL_B, RAIL_EDGE + 3.5), (COL_B, 70)])            # PITCH
    b1 = E.lane(sh, [(COL_C, LANE_TOP), (COL_C, B1_Y), (70, B1_Y)])  # Q1 base, the lower lane
    E.crossing(sh, COL_B, B1_Y)
    b2 = E.lane(sh, [(COL_B, 80), (COL_B, B2_Y), (146, B2_Y)])      # Q2 base, crossing over it
    sh.allow(b1, b2, 0)
    E.lane(sh, [(COL_D, LANE_TOP), (COL_D, 158)])                 # Q2 collector, OUT


def _parts(sh):
    r_cy = (RAIL_EDGE + LANE_TOP) / 2
    E.resistor(sh, COL_A, r_cy, vertical=True, lead=12, label="R1")
    E.led(sh, COL_A, 80, anode="up", lead_anode=12, lead_cathode=11, label="LED1")
    E.resistor(sh, COL_B, 75, vertical=True, lead=12, label="R4")
    E.resistor(sh, COL_C, r_cy, vertical=True, lead=12, label="R3")
    E.resistor(sh, COL_D, r_cy, vertical=True, lead=12, label="R2")
    E.ceramic_cap(sh, (COL_A + COL_B) / 2, CAP_Y, lead=8, label="C1")
    E.ceramic_cap(sh, (COL_C + COL_D) / 2, CAP_Y, lead=8, label="C2")
    gnd = S.RING_BOTTOM - 1
    E.transistor(sh, *Q1, {"E": (Q1[0], gnd), "B": (Q1[0] + 2, B1_Y), "C": (COL_A, 157)}, label="Q1")
    E.transistor(sh, *Q2, {"E": (Q2[0], gnd), "B": (Q2[0] - 7, B2_Y), "C": (COL_D, 157)}, label="Q2")
    E.patch_loop(sh, COL_B, 60, "PITCH")
    E.patch_loop(sh, 104, S.RING_TOP, "V+")
    E.patch_loop(sh, COL_D, 72, "OUT")


def _schematic(sh):
    lesson.schematic_panel(sh)
    top, bottom = 214.0, 272.0
    a, b, c, d = 44.0, 58.0, 72.0, 88.0
    sch.terminal(sh, 40, top, "V+", label_y=top - 3.4)
    sch.wire(sh, [(40.8, top), (d, top), (d, top + 0.01)])
    for x in (a, b):
        sch.junction(sh, x, top)

    sch.resistor(sh, a, top, 228, "R1", R_COLLECTOR)
    sch.led(sh, a, 228, 244, "LED1")
    _, c1, e1 = sch.npn(sh, a + 1.6, 256, "Q1", base="right")
    sch.wire(sh, [(a, 244), c1])
    sch.wire(sh, [e1, (a, bottom)])

    sch.resistor(sh, b, top, 230, "R3", R_BASE)
    sch.wire(sh, [(b, 230), (b, 256), (a + 1.6 + 4.5, 256)])

    sch.terminal(sh, c, 218, "", 0)
    sh.text(c + 2, 218.6, "PITCH", size=6.5, bold=True)
    sch.resistor(sh, c, 218.8, 233, "R4", R_SAFE)
    b2, c2, e2 = sch.npn(sh, d - 1.6, 256, "Q2", base="left")
    sch.wire(sh, [(c, 233), (c, 256), b2])

    sch.resistor(sh, d, top, 230, "R2", R_COLLECTOR)
    sch.wire(sh, [(d, 230), c2])
    sch.wire(sh, [e2, (d, bottom)])

    sch.capacitor_h(sh, a, 60, 247, "C1")
    sch.wire(sh, [(60, 247), (c, 247)])
    sch.capacitor_h(sh, 76, d, 237, "C2")
    sch.wire(sh, [(76, 237), (b, 237)])
    for x, y in ((a, 247), (c, 247), (d, 237), (b, 237)):
        sch.junction(sh, x, y)
    sch.wire(sh, [(d, 241), (93.2, 241)])
    sch.junction(sh, d, 241)
    sch.terminal(sh, 94, 241, "OUT", label_y=246.4, align="right")

    sch.wire(sh, [(40.8, bottom), (d, bottom), (d, bottom - 0.01)])
    sch.terminal(sh, 40, bottom, "GND", label_y=bottom + 5)
    lesson.schematic_note(sh, f"C1 and C2 ({CAP}) flip Q1 and Q2 in turn.")
