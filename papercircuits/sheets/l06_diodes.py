"""L06: Diodes are one-way valves.

Two branches off the switched rail, each a resistor, a small diode and an LED. D1 points
the way current flows, so LED1 lights, a little dimmer than it would without D1. D2 is
printed reversed on purpose, so LED2 stays dark. Measuring both sides of each diode shows
D1 takes about 0.7 V while D2 blocks almost the whole supply, and that the voltages
round a loop add up to the supply.
"""

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..draw import MUTED, Sheet
from ..provisional import HEADER_STATUS, HOLE_STEP, POWER, T0

PAGE_ID = "L06"

# Waiting on the T0 contact tests.
LEAD_STEP = f"Hold each lead flat on its lane with a small patch of copper tape. {T0}"
SWITCH_STEP = f"Stick a {S.FLAP_PAD_LEN:g} mm piece of copper tape on the corner flap, S1. {T0}"

# Provisional with the power page (standard §7): about 9 mA through branch 1 at 4.5 V.
RESISTOR, RESISTOR_BANDS = "220 Ω", "red-red-brown"
DIODE = "1N4148"

BRANCH_X = (95.0, 150.0)
RAIL_TOP, RAIL_SW, RAIL_GND = 46.0, 62.0, 137.5
SW_JOG = (34.0, 194.0)
NODE_X = (74.5, 95.0)   # resistor to diode
NODE_Y = (105.0, 125.0)  # diode to LED
R_CY = (RAIL_SW + S.TAPE_W / 2 + NODE_X[0]) / 2
D_CY = (NODE_X[1] + NODE_Y[0]) / 2
LED_CY = (NODE_Y[1] + RAIL_GND - S.TAPE_W / 2) / 2


def build(path):
    sh = Sheet(path, "L06 Diodes are one-way valves")
    E.header(
        sh, PAGE_ID, "L06  Diodes are one-way valves",
        "A diode lets current through one way only. Which LED gets any?",
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
    v_sw = E.lane(sh, [(sw_out, S.SWITCH_LANE_TOP), (sw_out, jog_y), (jog_x, jog_y), (jog_x, RAIL_SW), (75, RAIL_SW)])
    sh.allow(v_in, v_sw, S.SWITCH_PAD_GAP)
    for bx in BRANCH_X:
        E.lane(sh, [(bx, NODE_X[0]), (bx, NODE_X[1])])
        E.lane(sh, [(bx, NODE_Y[0]), (bx, NODE_Y[1])])
    E.lane(sh, [(x_in, S.hole_y("H3")), (45, S.hole_y("H3")), (45, RAIL_GND), (180, RAIL_GND)])
    E.fold_switch(sh, stubs=False)
    label_x = sw_in - S.TAPE_W / 2 - 2
    sh.text(label_x, 29.5, "S1", size=7, bold=True, align="right")
    sh.text(label_x, 33, "fold the corner down", size=6, color=MUTED, align="right")


def _parts(sh):
    for i, bx in enumerate(BRANCH_X, 1):
        E.resistor(sh, bx, R_CY, vertical=True, lead=11, label=f"R{i} · {RESISTOR}")
        E.diode(sh, bx, D_CY, lead=9, label=f"D{i}", cathode="down" if i == 1 else "up")
        E.led(sh, bx, LED_CY, anode="up", lead_anode=12, lead_cathode=11, label=f"LED{i}")
        E.test_point(sh, bx, (R_CY + 11 + D_CY - 9) / 2, f"TP{2 * i}")
        E.test_point(sh, bx, (D_CY + 9 + LED_CY - 12) / 2, f"TP{2 * i + 1}")
    E.test_point(sh, 80, RAIL_SW, "TP1", side="above")
    E.test_point(sh, 176, RAIL_GND, "TP6")
    for bx, name in zip(BRANCH_X, ("D1 forward", "D2 reversed")):
        sh.text(bx, RAIL_GND + 8, name, size=6.5, bold=True, color=MUTED, align="center")


def _instructions(sh):
    lesson.need_and_steps(sh, PAGE_ID, [
        "2 red LEDs, 5 mm",
        f"2 resistors, {RESISTOR} ({RESISTOR_BANDS}) {POWER}",
        f"2 small diodes, {DIODE} (glass, black band)",
        "5 mm copper tape",
        "Power page P1 in the binder; a multimeter",
    ], [
        "Lay the seven lanes, one piece of tape each. Fold at the creases; never cut.",
        SWITCH_STEP,
        HOLE_STEP,
        "Place R1 and R2 across their gaps, either way round.",
        "Place D1 and D2 <b>exactly as printed</b>, black band on the band mark. D2 points the other way on purpose.",
        "Place LED1 and LED2 as printed: long leg on the +.",
        LEAD_STEP,
        "Bind this page with P1, then fold the corner down to switch on.",
    ], (54.0, 151.0, 104.0, 196.0), (110.0, 151.0, 202.0, 196.0))


def _schematic(sh):
    lesson.schematic_panel(sh)
    top, x_node, y_node, bottom = 216.0, 232.0, 248.0, 268.0
    branches = (58.0, 82.0)
    sch.terminal(sh, 40, top, "V+", label_y=top - 3.4)
    sch.switch(sh, 40.8, 52, top, "S1")
    sch.wire(sh, [(52, top), (branches[1], top), (branches[1], top + 0.01)])
    sch.junction(sh, branches[0], top)
    sch.junction(sh, 70, top)
    sch.wire(sh, [(70, top), (70, 213.5)])
    sch.test_point(sh, 70, 212.6, "TP1")
    for i, bx in enumerate(branches, 1):
        sch.resistor(sh, bx, top, x_node, f"R{i}", RESISTOR)
        sch.diode(sh, bx, x_node, y_node, f"D{i}", cathode_bottom=i == 1)
        sch.led(sh, bx, y_node, bottom, f"LED{i}")
        side = -1 if i == 1 else 1
        for y, n in ((x_node, 2 * i), (y_node, 2 * i + 1)):
            sch.junction(sh, bx, y)
            sch.wire(sh, [(bx, y), (bx + side * 4.5, y)])
            sch.test_point(sh, bx + side * 5.4, y, f"TP{n}", side="left" if i == 1 else "right")
    sch.wire(sh, [(40.8, bottom), (branches[1], bottom), (branches[1], bottom - 0.01)])
    sch.terminal(sh, 40, bottom, "GND", label_y=bottom + 5)
    sch.junction(sh, branches[0], bottom)
    sch.junction(sh, 70, bottom)
    sch.wire(sh, [(70, bottom), (70, 270.5)])
    sch.test_point(sh, 70, 271.4, "TP6")
    lesson.schematic_note(sh, "The triangle points the way current can flow.")


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2

    _, py0, _, _ = boxes[0]
    E.workbook_box(sh, boxes[0], "Predict", "D2 is printed the other way round.")
    sh.text(tx, py0 + 9.5, "When you fold the corner down, which LEDs will light? Circle one for each.", size=7)
    sh.runs(tx, py0 + 17, [("LED1  ", True), ("lights  /  stays dark", False)], size=7.5)
    sh.runs(tx + 50, py0 + 17, [("LED2  ", True), ("lights  /  stays dark", False)], size=7.5)
    sh.text(tx, py0 + 22.5, "Why do you think so?", size=7, color=MUTED)

    _, my0, _, _ = boxes[1]
    E.workbook_box(sh, boxes[1], "Measure", "Hold the corner down. Black probe on TP6.")
    lesson.answer_table(sh, tx, my0 + 9.3, "Diode", ("D1  TP2, TP3", "D2  TP4, TP5"),
                        ("Before", "After", "Across"), label_w=26, pitch=22, box_w=14, row_h=5.4, unit="V")
    sh.text(tx + 26, my0 + 23.2, "Across = before − after", size=6.5, color=MUTED)

    _, ey0, _, _ = boxes[2]
    E.workbook_box(sh, boxes[2], "Explain", "D1 takes about 0.7 V. Where does the rest of the supply go?")
    sh.text(tx, ey0 + 9, "Why is LED2 dark, and why is there so much voltage across D2?", size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
