"""L05: Two ways to add a resistor.

Three LED branches off the switched rail, all with 470 Ω resistors:
- One: R1 alone, the reference.
- Two in a row: R2 then R3, joined by a middle lane, about 940 Ω.
- Two side by side: R4 and R5 bridge the same gap, about 235 Ω.

The LEDs rank side by side > one > in a row. With BT1 off, the meter reads each group
from TP1 to that branch's test point.

R4 and R5 land on one rail and one node strip, both passing by, so the parallel pair
needs no branching tape (standard §4).
"""

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..draw import MUTED, Sheet
from ..provisional import HEADER_STATUS, HOLE_STEP, POWER, T0

PAGE_ID = "L05"

# Waiting on the T0 contact tests.
LEAD_STEP = f"Hold each lead flat on its lane with a small patch of copper tape. {T0}"
SWITCH_STEP = f"Stick a {S.FLAP_PAD_LEN:g} mm piece of copper tape on the corner flap, S1. {T0}"

# Provisional with the power page (standard §7): about 5, 3 and 11 mA from 4.5 V.
RESISTOR, RESISTOR_BANDS = "470 Ω", "yellow-violet-brown"

RAIL_TOP, RAIL_SW, RAIL_GND = 46.0, 62.0, 137.5
SW_JOG = (34.0, 194.0)
A_X, B_X = 88.0, 122.0
C_R_X = (148.0, 160.0)
C_X = 168.0
NODE_END = 125.0
B_M = (74.5, 90.0)
C_NODE_Y = 79.5
LED_CY = (NODE_END + RAIL_GND - S.TAPE_W / 2) / 2


def build(path):
    sh = Sheet(path, "L05 Two ways to add a resistor")
    E.header(
        sh, PAGE_ID, "L05  Two ways to add a resistor",
        "One resistor, two in a row, two side by side. Which LED shines brightest?",
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
    rail_gap = RAIL_SW + S.TAPE_W / 2 + 10
    v_in = E.lane(sh, [(x_in, S.hole_y("H2")), (40, S.hole_y("H2")), (40, RAIL_TOP), (sw_in, RAIL_TOP),
                (sw_in, S.SWITCH_LANE_TOP)])
    v_sw = E.lane(sh, [(sw_out, S.SWITCH_LANE_TOP), (sw_out, jog_y), (jog_x, jog_y), (jog_x, RAIL_SW), (70, RAIL_SW)])
    sh.allow(v_in, v_sw, S.SWITCH_PAD_GAP)
    E.lane(sh, [(A_X, rail_gap), (A_X, NODE_END)])
    E.lane(sh, [(B_X, rail_gap), (B_X, B_M[1])])
    E.lane(sh, [(B_X, B_M[1] + 10), (B_X, NODE_END)])
    E.lane(sh, [(C_R_X[0] - 4, C_NODE_Y), (C_X, C_NODE_Y), (C_X, NODE_END)])
    E.lane(sh, [(x_in, S.hole_y("H3")), (45, S.hole_y("H3")), (45, RAIL_GND), (180, RAIL_GND)])
    E.fold_switch(sh, stubs=False)
    label_x = sw_in - S.TAPE_W / 2 - 2
    sh.text(label_x, 29.5, "S1", size=7, bold=True, align="right")
    sh.text(label_x, 33, "fold the corner down", size=6, color=MUTED, align="right")
    sh.text(92, 55, f"All five resistors are {RESISTOR} ({RESISTOR_BANDS}).", size=6.5, color=MUTED)


def _parts(sh):
    rail_edge = RAIL_SW + S.TAPE_W / 2
    E.resistor(sh, A_X, rail_edge + 5, vertical=True, lead=12, label=f"R1 · {RESISTOR}")
    E.resistor(sh, B_X, rail_edge + 5, vertical=True, lead=12, label="R2")
    E.resistor(sh, B_X, B_M[1] + 5, vertical=True, lead=12, label="R3")
    c_cy = (rail_edge + C_NODE_Y - S.TAPE_W / 2) / 2
    for i, x in enumerate(C_R_X, 4):
        E.resistor(sh, x, c_cy, vertical=True, lead=12, label=f"R{i}")
    for i, x in enumerate((A_X, B_X, C_X), 1):
        E.led(sh, x, LED_CY, anode="up", lead_anode=13, lead_cathode=11, label=f"LED{i}")
    E.test_point(sh, 75, RAIL_SW, "TP1", side="above")
    E.test_point(sh, A_X, 100, "TP2")
    E.test_point(sh, B_X, 112, "TP3")
    E.test_point(sh, sum(C_R_X) / 2, C_NODE_Y, "TP4", side="below")
    E.test_point(sh, 176, RAIL_GND, "TP5")
    for x, name in ((A_X, "One"), (B_X, "Two in a row"), (C_X - 8, "Two side by side")):
        sh.text(x, RAIL_GND + 8, name, size=6.5, bold=True, color=MUTED, align="center")


def _instructions(sh):
    lesson.need_and_steps(sh, PAGE_ID, [
        "3 red LEDs, 5 mm",
        f"5 resistors, {RESISTOR} ({RESISTOR_BANDS}) {POWER}",
        "5 mm copper tape",
        "Power page P1 in the binder",
        "A multimeter for Measure",
    ], [
        "Lay the seven lanes, one piece of tape each. Fold at the creases; never cut.",
        SWITCH_STEP,
        HOLE_STEP,
        "Place R1 to R5 across their gaps, either way round. R4 and R5 share one gap, side by side.",
        "Place LED1, LED2 and LED3 as printed: long leg on the +.",
        LEAD_STEP,
        "Bind this page with P1, then fold the corner down to switch on.",
    ], (54.0, 151.0, 104.0, 196.0), (110.0, 151.0, 202.0, 196.0))


def _schematic(sh):
    lesson.schematic_panel(sh)
    top, bottom = 214.0, 268.0
    a, b, c, c_r = 48.0, 62.0, 83.0, (78.0, 88.0)
    sch.terminal(sh, 38, top, "V+", label_y=top + 5)
    sch.switch(sh, 38.8, 45.5, top, "S1")
    sch.wire(sh, [(45.5, top), (c_r[1], top), (c_r[1], top + 0.01)])
    for x in (a, b, c_r[0]):
        sch.junction(sh, x, top)
    sch.junction(sh, 55, top)
    sch.wire(sh, [(55, top), (55, 211.5)])
    sch.test_point(sh, 55, 210.6, "TP1")

    sch.resistor(sh, a, top, 232, "R1", RESISTOR)
    sch.wire(sh, [(a, 232), (a, 236)])
    sch.junction(sh, a, 236)
    sch.wire(sh, [(a, 236), (a - 4.5, 236)])
    sch.test_point(sh, a - 5.4, 236, "TP2", side="left")
    sch.led(sh, a, 236, bottom, "LED1")

    sch.resistor(sh, b, top, 230, "R2", "")
    sch.resistor(sh, b, 230, 246, "R3", "")
    sch.wire(sh, [(b, 246), (b, 248)])
    sch.junction(sh, b, 248)
    sch.wire(sh, [(b, 248), (b + 4.5, 248)])
    sch.test_point(sh, b + 5.4, 248, "TP3")
    sch.led(sh, b, 248, bottom, "LED2")

    for i, x in enumerate(c_r, 4):
        sch.resistor(sh, x, top, 232, f"R{i}", "")
    sch.wire(sh, [(c_r[0], 232), (c_r[0], 236), (c_r[1], 236), (c_r[1], 232)])
    sch.junction(sh, c, 236)
    sch.wire(sh, [(c, 236), (c, 240)])
    sch.junction(sh, c, 238)
    sch.wire(sh, [(c, 238), (c + 4.5, 238)])
    sch.test_point(sh, c + 5.4, 238, "TP4")
    sch.led(sh, c, 240, bottom, "LED3")

    sch.wire(sh, [(38.8, bottom), (c, bottom), (c, bottom - 0.01)])
    sch.terminal(sh, 38, bottom, "GND", label_y=bottom + 5)
    for x in (a, b):
        sch.junction(sh, x, bottom)
    sch.junction(sh, 55, bottom)
    sch.wire(sh, [(55, bottom), (55, 270.5)])
    sch.test_point(sh, 55, 271.4, "TP5")
    lesson.schematic_note(sh, f"R1 to R5 are all {RESISTOR}.")


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2

    _, py0, _, _ = boxes[0]
    E.workbook_box(sh, boxes[0], "Predict", "Rank LED1, LED2 and LED3 from brightest to dimmest.")
    sh.runs(tx, py0 + 12, [("Brightest  ", True), ("_________    _________    _________", False),
                           ("  Dimmest", True)], size=7.5)
    sh.text(tx, py0 + 19.5, "Which group of resistors do you think lets the most current through?", size=7, color=MUTED)

    _, my0, _, _ = boxes[1]
    E.workbook_box(sh, boxes[1], "Measure", "Switch BT1 off. Measure from TP1 to each point.")
    lesson.answer_table(sh, tx, my0 + 9.3, "From TP1 to",
                        ("TP2  one", "TP3  two in a row", "TP4  two side by side"), ("Ohms",),
                        label_w=40, pitch=24, box_w=16, unit="Ω")
    sh.text(tx + 66, my0 + 14.1, "Then switch on.", size=7, bold=True, color=MUTED)
    sh.text(tx + 66, my0 + 18.9, "Did your ranking match?", size=6.5, color=MUTED)

    _, ey0, _, _ = boxes[2]
    E.workbook_box(sh, boxes[2], "Explain", "Two in a row add up.")
    sh.text(tx, ey0 + 9, "What do two side by side do, and why does that LED shine brightest?", size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
