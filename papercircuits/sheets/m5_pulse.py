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
"""

from .. import elements as E
from .. import lesson
from .. import module
from .. import schematic as sch
from .. import standard as S
from ..draw import Sheet
from ..provisional import HEADER_STATUS, T0

PAGE_ID = "M5"

# Waiting on the T0 contact tests.
LEAD_STEP = f"Solder every lead to its lane, or hold it flat with a small patch of copper tape. {T0}"
LOOP_STEP = f"Solder a patch loop upright on each GATE loop mark. {T0}"

R_COLLECTOR, R_LED, R_NOTE, R_REST, R_GATE = "1 kΩ", "470 Ω", "47 kΩ", "22 kΩ", "100 kΩ"
CAP = "10 µF"
TRANSISTOR = "2N3904"

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
    sh = Sheet(path, "M5 Pulse")
    E.header(sh, PAGE_ID, "M5  Pulse",
             "A slow oscillator blinks an LED and chops the note into a beat.", status=HEADER_STATUS)
    E.spine(sh)
    module.power_ring(sh)
    _lanes(sh)
    _parts(sh)
    module.need(sh, PAGE_ID, [
        f"Q1, Q2, Q3: {TRANSISTOR} transistors",
        f"C1, C2: {CAP} electrolytic, 16 V or more",
        f"R1 {R_COLLECTOR} · R2 {R_LED} · R3 {R_NOTE}",
    ], [
        f"R4 {R_REST} · R5 {R_GATE} · LED1: red, 5 mm",
        "Bare wire for 2 patch loops",
        "Copper tape, solder, 2-core cable",
    ])
    module.caption(sh, "Patch one GATE to M1's PITCH and the controller's lead to the other. LED1 lights for each note.")
    _schematic(sh)
    module.steps(sh, PAGE_ID, [
        "Lay the power ring, then the seven lanes inside it, one piece of tape each. Fold at the creases.",
        "Where two lanes cross, lay the lower one, stick the insulating patch over it, then lay the upper one.",
        "Place R1 to R5 either way round, and LED1 long leg on the +. C1 and C2 go + where printed: "
        "backwards, they can heat up and fail.",
        "Lay Q1 to Q3 flat face up and bend each leg to its letter: E, B and C.",
        LEAD_STEP,
        LOOP_STEP,
        "Join the edge connectors to the pages either side with 2-core cable, or with red and black clip leads.",
    ], [
        "Power up: LED1 should blink about twice a second before anything is patched.",
        "Patch one GATE loop to M1's PITCH, and clip the controller's lead (M2's stylus, M3 or M4) to the other.",
        "For a slower beat, use 22 µF for C1 and C2. Swap R3 and R4 for short notes and long rests.",
    ])
    E.footer(sh, PAGE_ID)
    sh.save()


def _lanes(sh):
    E.lane(sh, [(COL_A, LANE_TOP), (COL_A, 158)])                 # Q1 collector
    b1 = E.lane(sh, [(COL_C, LANE_TOP), (COL_C, B1_Y), (Q1[0] + 2, B1_Y)])  # Q1 base, the lower lane
    E.crossing(sh, COL_B, B1_Y)
    b2 = E.lane(sh, [(COL_B, LANE_TOP), (COL_B, B2_Y), (Q2[0] - 4, B2_Y)])  # Q2 base, crossing over it
    sh.allow(b1, b2, 0)
    E.lane(sh, [(COL_D, LANE_TOP), (COL_D, 75)])                  # R2 to LED1
    E.lane(sh, [(COL_D, 85), (COL_D, 158)])                       # Q2 collector
    E.lane(sh, [(Q3B_X, R5_Y - 4), (Q3B_X, 158)])                 # Q3 base
    E.lane(sh, [(GATE_X, LANE_TOP), (GATE_X, 158)])               # Q3 collector, GATE


def _parts(sh):
    r_cy = (RAIL_EDGE + LANE_TOP) / 2
    for x, label in ((COL_A, "R1"), (COL_B, "R4"), (COL_C, "R3"), (COL_D, "R2")):
        E.resistor(sh, x, r_cy, vertical=True, lead=12, label=label)
    E.led(sh, COL_D, 80, anode="up", lead_anode=12, lead_cathode=11, label="LED1")
    E.radial_cap(sh, COL_A, COL_B, CAP_Y, label="C1")
    E.radial_cap(sh, COL_D, COL_C, CAP_Y, label="C2")
    E.resistor(sh, (COL_D + Q3B_X) / 2, R5_Y, vertical=False, lead=8, label="R5")
    gnd = S.RING_BOTTOM - 1
    E.transistor(sh, *Q1, {"E": (Q1[0], gnd), "B": (Q1[0] + 2, B1_Y), "C": (COL_A, 157)}, label="Q1")
    E.transistor(sh, *Q2, {"E": (Q2[0], gnd), "B": (Q2[0] - 7, B2_Y), "C": (COL_D, 157)}, label="Q2")
    E.transistor(sh, *Q3, {"E": (Q3[0], gnd), "B": (Q3B_X, 157), "C": (GATE_X, 157)}, label="Q3")
    for y in GATE_LOOPS:
        E.patch_loop(sh, GATE_X, y, "GATE", side="left")


def _schematic(sh):
    lesson.schematic_panel(sh)
    top, bottom = 214.0, 272.0
    a, b, c, d = 44.0, 56.0, 67.0, 78.0
    sch.terminal(sh, 40, top, "V+", label_y=top - 3.4)
    sch.wire(sh, [(40.8, top), (d, top), (d, top + 0.01)])
    for x in (a, b, c):
        sch.junction(sh, x, top)

    sch.resistor(sh, a, top, 232, "R1", R_COLLECTOR)
    _, c1, e1 = sch.npn(sh, a + 1.6, 256, "Q1", base="right")
    sch.wire(sh, [(a, 232), c1])
    sch.wire(sh, [e1, (a, bottom)])

    sch.resistor(sh, b, top, 232, "R3", R_NOTE)
    sch.wire(sh, [(b, 232), (b, 256), (a + 1.6 + 4.5, 256)])

    sch.resistor(sh, c, top, 232, "R4", R_REST)
    b2, c2, e2 = sch.npn(sh, d - 1.6, 256, "Q2", base="left")
    sch.wire(sh, [(c, 232), (c, 256), b2])

    sch.resistor(sh, d, top, 226, "R2", R_LED)
    sch.led(sh, d, 226, 238, "LED1")
    sch.wire(sh, [(d, 238), c2])
    sch.wire(sh, [e2, (d, bottom)])

    sch.wire(sh, [(a, 248), (58, 248)])
    sch.capacitor_h(sh, 58, c, 248, "C1", plus="left")
    sch.capacitor_h(sh, 68, d, 240, "C2", CAP, plus="right")
    sch.wire(sh, [(68, 240), (b, 240)])
    for x, y in ((a, 248), (c, 248), (d, 240), (b, 240)):
        sch.junction(sh, x, y)

    b3, c3, e3 = sch.npn(sh, 90.0, 244, "Q3", base="left")
    sch.resistor_h(sh, d, b3[0], 244, "R5", box_w=4.2)
    sch.junction(sh, d, 244)
    sch.wire(sh, [c3, (c3[0], 231.6)])
    sch.terminal(sh, c3[0], 230, "GATE", label_y=226.2, align="right")
    sch.wire(sh, [e3, (c3[0], bottom)])

    sch.wire(sh, [(40.8, bottom), (c3[0], bottom), (c3[0], bottom - 0.01)])
    sch.terminal(sh, 40, bottom, "GND", label_y=bottom + 5)
    lesson.schematic_note(sh, "Q3 holds GATE at GND in the rests.")
