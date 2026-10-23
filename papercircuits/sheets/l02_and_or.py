"""L02: Two switches, two ways.

Top circuit: tab switches A1 and B1 in series feed R1 and LED1, so LED1 needs both (AND).
Bottom circuit: A2 and B2 in parallel feed R2 and LED2, so either will do (OR).

Each tab switch folds over a switch pair (standard §6). In series the chain zig-zags
between the pair's two rows: V+ on the lower row, M on the upper, N back on the lower.
One V+ strip serves both circuits: it passes A1, drops between A1 and B1, then runs
under both OR flaps as the upper lane of the bottom pair.
"""

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..draw import Sheet
from ..provisional import HEADER_STATUS, HOLE_STEP, POWER, T0

PAGE_ID = "L02"

# Waiting on the T0 contact tests.
LEAD_STEP = f"Hold each lead flat on its lane with a small patch of copper tape. {T0}"
LANE_STEP = (f"Lay the seven lanes, one piece of tape each. Where two lanes run close, keep the "
             f"{S.SWITCH_PAD_GAP:g} mm gap clear. {T0}")
PAD_STEP = (f"Stick a {S.FLAP_PAD_LEN:g} mm piece of tape on each flap where shown. Folded down, "
            f"it must cross both lanes. {T0}")

# Provisional with the power page (standard §7): 220 Ω gives about 11 mA from 4.5 V.
RESISTOR = "220 Ω"
RESISTOR_BANDS = "red-red-brown"

AND_UPPER = 56.0                      # M, between A1 and B1
AND_LOWER = AND_UPPER + S.PAIR_PITCH  # V+ into A1, then N out of B1
OR_UPPER = 120.0                      # V+ past A2 and B2
OR_LOWER = OR_UPPER + S.PAIR_PITCH    # OUT, past A2 and B2
A1_X, B1_X = 70.0, 110.0
A2_X, B2_X = 110.0, 140.0
V_DROP_X = 86.0                       # V+ drops from the AND row to the OR row here
GND_X = 194.0
LED_X = 186.0
R1_X, R2_X = 145.0, 165.0


def build(path):
    sh = Sheet(path, "L02 Two switches, two ways")
    E.header(
        sh, PAGE_ID, "L02  Two switches, two ways",
        "Wire the same two switches in a row, then side by side, and compare.",
        status=HEADER_STATUS,
    )
    _lanes(sh)
    E.spine(sh, connected=("H2", "H3"))
    _switches(sh)
    _parts(sh)
    _instructions(sh)
    _schematic(sh)
    _workbook(sh)
    E.footer(sh, PAGE_ID)
    sh.save()


def _lanes(sh):
    x_in = S.NET_STRIP_START_X
    v_plus, gnd = S.hole_y("H2"), S.hole_y("H3")
    v_in = E.lane(sh, [(x_in, v_plus), (40, v_plus), (40, AND_LOWER), (V_DROP_X, AND_LOWER),
                (V_DROP_X, OR_UPPER), (B2_X + 6, OR_UPPER)])
    m = E.lane(sh, [(A1_X - 8, AND_UPPER), (B1_X + 8, AND_UPPER)])
    n = E.lane(sh, [(B1_X - 8, AND_LOWER), (R1_X - 5, AND_LOWER)])
    E.lane(sh, [(R1_X + 5, AND_LOWER), (LED_X - 5, AND_LOWER)])
    out = E.lane(sh, [(A2_X - 8, OR_LOWER), (R2_X - 5, OR_LOWER)])
    for a, b in ((v_in, m), (m, n), (v_in, out)):
        sh.allow(a, b, S.SWITCH_PAD_GAP)
    E.lane(sh, [(R2_X + 5, OR_LOWER), (LED_X - 5, OR_LOWER)])
    E.lane(sh, [(x_in, gnd), (GND_X, gnd), (GND_X, AND_UPPER)])


def _switches(sh):
    for x, upper, label in ((A1_X, AND_UPPER, "A1"), (B1_X, AND_UPPER, "B1"),
                            (A2_X, OR_UPPER, "A2"), (B2_X, OR_UPPER, "B2")):
        E.tab_switch(sh, x, upper, label)


def _parts(sh):
    E.resistor(sh, R1_X, AND_LOWER, vertical=False, lead=12, label=f"R1 · {RESISTOR}")
    E.resistor(sh, R2_X, OR_LOWER, vertical=False, lead=10, label=f"R2 · {RESISTOR}")
    for y, label in ((AND_LOWER, "LED1"), (OR_LOWER, "LED2")):
        E.led(sh, LED_X, y, anode="left", lead_anode=13, lead_cathode=11, label=label)
    E.test_point(sh, 124, AND_LOWER, "TP1", side="above")
    E.test_point(sh, 151, OR_LOWER, "TP2", side="below")
    E.test_point(sh, GND_X, 95, "TP3", side="left")


def _instructions(sh):
    lesson.need_and_steps(sh, PAGE_ID, [
        "2 red LEDs, 5 mm",
        f"2 resistors, {RESISTOR} ({RESISTOR_BANDS}) {POWER}",
        "5 mm copper tape and scissors",
        "Power page P1 in the binder",
        "A multimeter for Test",
    ], [
        LANE_STEP,
        "Cut each flap along its solid line and crease it along the dotted hinge.",
        PAD_STEP,
        HOLE_STEP,
        "Place R1 and R2 either way round, and LED1 and LED2 as printed: long leg on the +.",
        LEAD_STEP,
        "Bind this page with P1 and switch BT1 on. Press the flaps down to test.",
    ], (38.0, 137.0, 90.0, 184.0), (96.0, 137.0, 189.0, 184.0))


def _schematic(sh):
    lesson.schematic_panel(sh)

    rail, and_y, or_a, or_b, gnd = 44.0, 218.0, 232.0, 242.0, 270.0
    and_x, or_x, join_x = 84.0, 70.0, 60.0
    sch.terminal(sh, rail, 212, "", 0)
    sh.text(rail - 2, 213.2, "V+", size=6.5, bold=True, align="right")
    sch.wire(sh, [(rail, 212.8), (rail, or_b)])
    sch.junction(sh, rail, and_y)
    sch.junction(sh, rail, or_a)

    sch.switch(sh, rail, 55, and_y, "A1")
    sch.switch(sh, 55, 66, and_y, "B1")
    sch.wire(sh, [(66, and_y), (and_x, and_y)])
    sch.resistor(sh, and_x, and_y, 238, "R1", RESISTOR)
    sch.junction(sh, and_x, 238)
    sch.wire(sh, [(and_x, 238), (and_x + 4, 238)])
    sch.test_point(sh, and_x + 4.9, 238, "TP1")
    sch.led(sh, and_x, 238, gnd, "LED1")

    sch.switch(sh, rail, 56, or_a, "A2")
    sch.switch(sh, rail, 56, or_b, "B2")
    sch.wire(sh, [(56, or_b), (join_x, or_b), (join_x, or_a)])
    sch.wire(sh, [(56, or_a), (or_x, or_a)])
    sch.junction(sh, join_x, or_a)
    sch.resistor(sh, or_x, or_a, 250, "R2", RESISTOR)
    sch.junction(sh, or_x, 250)
    sch.wire(sh, [(or_x, 250), (or_x - 4, 250)])
    sch.test_point(sh, or_x - 4.9, 250, "TP2", side="left")
    sch.led(sh, or_x, 250, gnd, "LED2")

    sch.terminal(sh, rail, gnd, "", 0)
    sh.text(rail - 2, gnd + 1.2, "GND", size=6.5, bold=True, align="right")
    sch.wire(sh, [(rail + 0.8, gnd), (and_x, gnd), (and_x, gnd - 0.01)])
    sch.junction(sh, or_x, gnd)
    sch.junction(sh, 56, gnd)
    sch.wire(sh, [(56, gnd), (56, 274.5)])
    sch.test_point(sh, 56, 275.4, "TP3")
    lesson.schematic_note(sh, "V+ and GND come from P1.")


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2
    and_rows = ("A1 only", "B1 only", "A1 and B1")
    or_rows = ("A2 only", "B2 only", "A2 and B2")

    _, py0, _, _ = boxes[0]
    E.workbook_box(sh, boxes[0], "Predict", "Will the LED light? Write Y or N.")
    lesson.answer_table(sh, tx, py0 + 9.3, "Top", and_rows, ("LED1",))
    lesson.answer_table(sh, tx + 50, py0 + 9.3, "Bottom", or_rows, ("LED2",))

    _, ty0, _, _ = boxes[1]
    E.workbook_box(sh, boxes[1], "Test", "Press the flaps. Black probe on TP3.")
    lesson.answer_table(sh, tx, ty0 + 9.3, "Top", and_rows, ("LED1", "TP1 V"))
    lesson.answer_table(sh, tx + 50, ty0 + 9.3, "Bottom", or_rows, ("LED2", "TP2 V"))

    _, ey0, ex1, _ = boxes[2]
    E.workbook_box(sh, boxes[2], "Explain", "One circuit is called AND, the other OR.")
    sh.text(tx, ey0 + 9, "Which is which? Which one is like a door with two locks?", size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
