"""L07: Share the voltage.

Three voltage dividers hang between the switched rail and GND, each two resistors in a
row with a test point in the middle:
- A: 1 kΩ over 1 kΩ, half the supply.
- B: 2.2 kΩ over 1 kΩ, about a third.
- C: 1 kΩ over 2.2 kΩ, about two thirds.

Learners predict, measure the middles, then work each one out from the ratio. Swapping
top and bottom (B against C) flips the answer. There are no LEDs: this is the page where
the meter does the showing.
"""

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..draw import MUTED, Sheet
from ..provisional import HEADER_STATUS, HOLE_STEP, T0

PAGE_ID = "L07"

# Waiting on the T0 contact tests.
LEAD_STEP = f"Hold each lead flat on its lane with a small patch of copper tape. {T0}"
SWITCH_STEP = f"Stick a {S.FLAP_PAD_LEN:g} mm piece of copper tape on the corner flap, S1. {T0}"

# Each divider's (name, top, bottom). The ratios don't depend on the supply.
DIVIDERS = (("A", "1 kΩ", "1 kΩ"), ("B", "2.2 kΩ", "1 kΩ"), ("C", "1 kΩ", "2.2 kΩ"))
BANDS = {"1 kΩ": "brown-black-red", "2.2 kΩ": "red-red-red"}

BRANCH_X = (85.0, 125.0, 165.0)
RAIL_TOP, RAIL_SW, RAIL_GND = 46.0, 62.0, 120.0
SW_JOG = (34.0, 194.0)
MID = (74.5, 105.0)
TOP_CY = (RAIL_SW + S.TAPE_W / 2 + MID[0]) / 2
BOT_CY = (MID[1] + RAIL_GND - S.TAPE_W / 2) / 2
TP_MID_Y = (TOP_CY + 12 + BOT_CY - 12) / 2


def build(path):
    sh = Sheet(path, "L07 Share the voltage")
    E.header(
        sh, PAGE_ID, "L07  Share the voltage",
        "Two resistors in a row split the supply between them. Find the rule.",
        status=HEADER_STATUS,
    )
    _lanes(sh)
    E.spine(sh, connected=("H2", "H3"))
    _parts(sh)
    _instructions(sh)
    _schematic(sh)
    _workbook(sh)
    E.footer(sh, PAGE_ID)
    sh.save()


def _lanes(sh):
    sw_in, sw_out = S.SWITCH_LANE_X
    jog_y, jog_x = SW_JOG
    x_in = S.NET_STRIP_START_X
    v_in = E.lane(sh, [(x_in, S.hole_y("H2")), (40, S.hole_y("H2")), (40, RAIL_TOP), (sw_in, RAIL_TOP),
                (sw_in, S.SWITCH_LANE_TOP)])
    v_sw = E.lane(sh, [(sw_out, S.SWITCH_LANE_TOP), (sw_out, jog_y), (jog_x, jog_y), (jog_x, RAIL_SW), (70, RAIL_SW)])
    sh.allow(v_in, v_sw, S.SWITCH_PAD_GAP)
    for bx in BRANCH_X:
        E.lane(sh, [(bx, MID[0]), (bx, MID[1])])
    E.lane(sh, [(x_in, S.hole_y("H3")), (45, S.hole_y("H3")), (45, RAIL_GND), (180, RAIL_GND)])
    E.fold_switch(sh, stubs=False)
    label_x = sw_in - S.TAPE_W / 2 - 2
    sh.text(label_x, 29.5, "S1", size=7, bold=True, align="right")
    sh.text(label_x, 33, "fold the corner down", size=6, color=MUTED, align="right")


def _parts(sh):
    for i, (bx, (name, top, bottom)) in enumerate(zip(BRANCH_X, DIVIDERS)):
        E.resistor(sh, bx, TOP_CY, vertical=True, lead=12, label=f"R{2 * i + 1} · {top}")
        E.resistor(sh, bx, BOT_CY, vertical=True, lead=12, label=f"R{2 * i + 2} · {bottom}")
        E.test_point(sh, bx, TP_MID_Y, f"TP{i + 2}")
        sh.text(bx, RAIL_GND + 9, f"{name} · {top} over {bottom}", size=6.5, bold=True, color=MUTED, align="center")
    E.test_point(sh, 74, RAIL_SW, "TP1", side="above")
    E.test_point(sh, 176, RAIL_GND, "TP5")


def _instructions(sh):
    lesson.need_and_steps(sh, PAGE_ID, [
        f"4 resistors, 1 kΩ ({BANDS['1 kΩ']})",
        f"2 resistors, 2.2 kΩ ({BANDS['2.2 kΩ']})",
        "5 mm copper tape",
        "Power page P1 in the binder",
        "A multimeter",
    ], [
        "Lay the six lanes, one piece of tape each. Fold at the creases; never cut.",
        SWITCH_STEP,
        HOLE_STEP,
        "Sort the resistors by colour: four 1 kΩ and two 2.2 kΩ. Place each one on its labelled gap, "
        "either way round.",
        LEAD_STEP,
        "Bind this page with P1. Hold the corner down while you measure.",
    ], (54.0, 136.0, 104.0, 196.0), (110.0, 136.0, 202.0, 196.0))


def _schematic(sh):
    lesson.schematic_panel(sh)
    top, mid, bottom = 216.0, 238.0, 262.0
    branches = (52.0, 68.0, 84.0)
    sch.terminal(sh, 40, top, "V+", label_y=top - 3.4)
    sch.switch(sh, 40.8, 49, top, "S1")
    sch.wire(sh, [(49, top), (branches[-1], top), (branches[-1], top + 0.01)])
    sch.junction(sh, 60, top)
    sch.wire(sh, [(60, top), (60, 213.5)])
    sch.test_point(sh, 60, 212.6, "TP1")
    for i, (bx, (_, r_top, r_bottom)) in enumerate(zip(branches, DIVIDERS)):
        if bx != branches[-1]:
            sch.junction(sh, bx, top)
            sch.junction(sh, bx, bottom)
        sch.resistor(sh, bx, top, mid - 4, f"R{2 * i + 1}", r_top)
        sch.wire(sh, [(bx, mid - 4), (bx, mid)])
        sch.junction(sh, bx, mid)
        sch.wire(sh, [(bx, mid), (bx - 4.5, mid)])
        sch.test_point(sh, bx - 5.4, mid, f"TP{i + 2}", side="left")
        sch.resistor(sh, bx, mid, bottom, f"R{2 * i + 2}", r_bottom)
    sch.wire(sh, [(40.8, bottom), (branches[-1], bottom), (branches[-1], bottom - 0.01)])
    sch.terminal(sh, 40, bottom, "GND", label_y=bottom + 5)
    sch.junction(sh, 60, bottom)
    sch.wire(sh, [(60, bottom), (60, 264.5)])
    sch.test_point(sh, 60, 265.4, "TP5")
    lesson.schematic_note(sh, "A is R1 and R2, B is R3 and R4, C is R5 and R6.")


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2

    _, py0, _, _ = boxes[0]
    E.workbook_box(sh, boxes[0], "Predict", "Which middle point will read the highest voltage?")
    sh.runs(tx, py0 + 12, [("Highest  ", True), ("A  /  B  /  C", False)], size=7.5)
    sh.text(tx, py0 + 19.5, "Circle one. Which resistor do you think gets the bigger share, and why?",
            size=7, color=MUTED)

    _, my0, _, _ = boxes[1]
    E.workbook_box(sh, boxes[1], "Measure", "Hold the corner down. Black probe on TP5.")
    lesson.answer_table(sh, tx, my0 + 9.3, "Middle", ("A  TP2", "B  TP3", "C  TP4"),
                        ("Measured", "Worked out"), label_w=20, pitch=21, box_w=13, unit="V")
    sh.runs(tx + 66, my0 + 9.3, [("TP1  ", True), ("______ V", False)], size=7)
    sh.text(tx + 66, my0 + 15.5, "Worked out =", size=6.5, bold=True, color=MUTED)
    sh.text(tx + 66, my0 + 19.3, "TP1 × bottom", size=6.5, color=MUTED)
    sh.text(tx + 66, my0 + 23.1, "÷ (top + bottom)", size=6.5, color=MUTED)

    _, ey0, _, _ = boxes[2]
    E.workbook_box(sh, boxes[2], "Explain", "What happens to the middle when you swap top and bottom?")
    sh.text(tx, ey0 + 9, "Compare B and C. Which pair would give you about 3 V from P1?", size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
