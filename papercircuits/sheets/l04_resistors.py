"""L04: Resistors set the current.

Three branches, each a resistor and an LED, hang off the switched V+ rail. The resistors
are 220 Ω, 1 kΩ and 4.7 kΩ, so the LEDs glow bright, medium and dim. Learners sort the
resistors by colour code, then measure the voltage across each one and work out the
current with Ohm's law. The voltage across each resistor comes out nearly the same; the
current is what changes.

Layout follows L01: V+ climbs to the corner switch, and the switched rail and GND rail
pass every branch, so each node is one strip.
"""

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..draw import MUTED, Sheet
from ..provisional import HEADER_STATUS, HOLE_STEP, POWER, T0

PAGE_ID = "L04"

# Waiting on the T0 contact tests.
LEAD_STEP = f"Hold each lead flat on its lane with a small patch of copper tape. {T0}"
SWITCH_STEP = f"Stick a {S.FLAP_PAD_LEN:g} mm piece of copper tape on the corner flap, S1. {T0}"

# Provisional with the power page (standard §7): about 12, 2.7 and 0.6 mA from 4.5 V.
RESISTORS = (("220 Ω", "red-red-brown"), ("1 kΩ", "brown-black-red"), ("4.7 kΩ", "yellow-violet-red"))

BRANCH_X = (85.0, 125.0, 165.0)
RAIL_TOP, RAIL_SW, RAIL_GND = 46.0, 62.0, 124.5
NODE = (74.5, 112.0)
SW_JOG = (34.0, 194.0)
R_CY = (RAIL_SW + S.TAPE_W / 2 + NODE[0]) / 2
LED_CY = (NODE[1] + RAIL_GND - S.TAPE_W / 2) / 2
TP_NODE_Y = (NODE[0] + NODE[1]) / 2


def build(path):
    sh = Sheet(path, "L04 Resistors set the current")
    E.header(
        sh, PAGE_ID, "L04  Resistors set the current",
        "Same LED, three resistors. Read the colours, then measure the current.",
        status=HEADER_STATUS,
    )
    _lanes(sh)
    E.spine(sh, connected=("H2", "H3"))
    _parts(sh)
    _instructions(sh)
    E.colour_code_key(sh, 54, 167)
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
        E.lane(sh, [(bx, NODE[0]), (bx, NODE[1])])
    E.lane(sh, [(x_in, S.hole_y("H3")), (45, S.hole_y("H3")), (45, RAIL_GND), (180, RAIL_GND)])
    E.fold_switch(sh, stubs=False)
    label_x = sw_in - S.TAPE_W / 2 - 2
    sh.text(label_x, 29.5, "S1", size=7, bold=True, align="right")
    sh.text(label_x, 33, "fold the corner down", size=6, color=MUTED, align="right")


def _parts(sh):
    for i, (bx, (value, _)) in enumerate(zip(BRANCH_X, RESISTORS), 1):
        E.resistor(sh, bx, R_CY, vertical=True, lead=12, label=f"R{i} · {value}")
        E.led(sh, bx, LED_CY, anode="up", lead_anode=13, lead_cathode=11, label=f"LED{i}")
        E.test_point(sh, bx, TP_NODE_Y, f"TP{i + 1}")
    E.test_point(sh, 74, RAIL_SW, "TP1", side="above")
    E.test_point(sh, 176, RAIL_GND, "TP5")


def _instructions(sh):
    lesson.need_and_steps(sh, PAGE_ID, [
        "3 red LEDs, 5 mm",
        f"R1 {RESISTORS[0][0]}, R2 {RESISTORS[1][0]} and R3 {RESISTORS[2][0]} {POWER}",
        "5 mm copper tape",
        "Power page P1 in the binder",
        "A multimeter for Measure",
    ], [
        "Read each resistor's bands with the colour code below, and sort them into R1, R2 and R3.",
        "Lay the six lanes, one piece of tape each. Fold at the creases; never cut.",
        SWITCH_STEP,
        HOLE_STEP,
        "Place R1, R2 and R3 across their gaps, either way round. Check each against its label.",
        "Place LED1, LED2 and LED3 as printed: long leg on the +.",
        LEAD_STEP,
        "Bind this page with P1, then fold the corner down to switch on.",
    ], (54.0, 136.0, 104.0, 162.0), (110.0, 136.0, 202.0, 196.0))


def _schematic(sh):
    lesson.schematic_panel(sh)
    top, node, bottom = 216.0, 238.0, 268.0
    branches = (52.0, 68.0, 84.0)
    sch.terminal(sh, 40, top, "V+", label_y=top - 3.4)
    sch.switch(sh, 40.8, 49, top, "S1")
    sch.wire(sh, [(49, top), (branches[-1], top), (branches[-1], top + 0.01)])
    sch.junction(sh, 60, top)
    sch.wire(sh, [(60, top), (60, 213.5)])
    sch.test_point(sh, 60, 212.6, "TP1")
    for i, (bx, (value, _)) in enumerate(zip(branches, RESISTORS), 1):
        if i < len(branches):
            sch.junction(sh, bx, top)
        sch.resistor(sh, bx, top, node - 4, f"R{i}", value)
        sch.wire(sh, [(bx, node - 4), (bx, node)])
        sch.junction(sh, bx, node)
        sch.wire(sh, [(bx, node), (bx - 4.5, node)])
        sch.test_point(sh, bx - 5.4, node, f"TP{i + 1}", side="left")
        sch.led(sh, bx, node, bottom, f"LED{i}")
        if i < len(branches):
            sch.junction(sh, bx, bottom)
    sch.wire(sh, [(40.8, bottom), (branches[-1], bottom), (branches[-1], bottom - 0.01)])
    sch.terminal(sh, 40, bottom, "GND", label_y=bottom + 5)
    sch.junction(sh, 60, bottom)
    sch.wire(sh, [(60, bottom), (60, 270.5)])
    sch.test_point(sh, 60, 271.4, "TP5")
    lesson.schematic_note(sh, "V+ and GND come from P1 through the binder.")


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2

    _, py0, _, _ = boxes[0]
    E.workbook_box(sh, boxes[0], "Predict", "Rank the LEDs from brightest to dimmest.")
    sh.runs(tx, py0 + 12, [("Brightest  ", True), ("_________    _________    _________", False),
                           ("  Dimmest", True)], size=7.5)
    sh.text(tx, py0 + 19.5, "Which resistor do you think lets the most current through, and why?", size=7, color=MUTED)

    _, my0, _, _ = boxes[1]
    E.workbook_box(sh, boxes[1], "Measure", "Hold the corner down. Red probe on TP1, black on TP2–TP4.")
    rows = [f"R{i}  {value}" for i, (value, _) in enumerate(RESISTORS, 1)]
    lesson.answer_table(sh, tx, my0 + 9.3, "Across", rows, ("Volts", "mA"), label_w=26, pitch=20, box_w=14)
    sh.text(tx + 70, my0 + 14.1, "mA = volts ÷ kΩ", size=7, bold=True, color=MUTED)
    sh.text(tx + 70, my0 + 18.9, "220 Ω is 0.22 kΩ", size=6.5, color=MUTED)

    _, ey0, _, _ = boxes[2]
    E.workbook_box(sh, boxes[2], "Explain", "What happens to the current when the resistance goes up?")
    sh.text(tx, ey0 + 9, "Write it as a rule. Did the voltage across each resistor change much?", size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
