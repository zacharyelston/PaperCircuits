"""L08: Store some charge.

Two LEDs on the switched rail. LED2 has just a resistor, so it goes out the moment S1
is released. LED1 sits behind node X, where C1 (2200 µF) charges through R1 while S1 is
held. Let go, and C1 keeps LED1 lit through R2, fading over a few seconds.

Node X is one strip passing R1's lower lead, C1's + leg and R2's upper lead. C1 lies on
its side beside the strip, its legs bent up to node X and down to GND.
"""

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..draw import MUTED, Sheet
from ..provisional import HEADER_STATUS, HOLE_STEP, POWER, T0

PAGE_ID = "L08"

# Waiting on the T0 contact tests.
LEAD_STEP = f"Hold each lead flat on its lane with a small patch of copper tape. {T0}"
SWITCH_STEP = f"Stick a {S.FLAP_PAD_LEN:g} mm piece of copper tape on the corner flap, S1. {T0}"

# Provisional with the power page (standard §7): LED1 fades over roughly 3 s at 4.5 V.
R_CHARGE, R_CHARGE_BANDS = "100 Ω", "brown-black-brown"
R_LED, R_LED_BANDS = "470 Ω", "yellow-violet-brown"
CAPACITOR = "2200 µF"

RAIL_TOP, RAIL_SW, RAIL_GND = 46.0, 62.0, 120.0
SW_JOG = (34.0, 194.0)
NODE_X_Y = 80.0
NODE_X_SPAN = (78.0, 132.0)
R1_X, C1_X, R2_X, B2_X = 85.0, 105.0, 125.0, 160.0
NODE_Y = (92.5, 107.5)
NODE_Z = (74.5, 107.5)
LED_CY = (NODE_Y[1] + RAIL_GND - S.TAPE_W / 2) / 2


def build(path):
    sh = Sheet(path, "L08 Store some charge")
    E.header(
        sh, PAGE_ID, "L08  Store some charge",
        "A capacitor keeps an LED lit after the power goes. For how long?",
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
    E.lane(sh, [(NODE_X_SPAN[0], NODE_X_Y), (NODE_X_SPAN[1], NODE_X_Y)])
    E.lane(sh, [(R2_X, NODE_Y[0]), (R2_X, NODE_Y[1])])
    E.lane(sh, [(B2_X, NODE_Z[0]), (B2_X, NODE_Z[1])])
    E.lane(sh, [(x_in, S.hole_y("H3")), (45, S.hole_y("H3")), (45, RAIL_GND), (180, RAIL_GND)])
    E.fold_switch(sh, stubs=False)
    label_x = sw_in - S.TAPE_W / 2 - 2
    sh.text(label_x, 29.5, "S1", size=7, bold=True, align="right")
    sh.text(label_x, 33, "fold the corner down", size=6, color=MUTED, align="right")


def _parts(sh):
    rail_edge, x_edge = RAIL_SW + S.TAPE_W / 2, NODE_X_Y - S.TAPE_W / 2
    E.resistor(sh, R1_X, (rail_edge + x_edge) / 2, vertical=True, lead=12, label=f"R1 · {R_CHARGE}")
    E.electrolytic(sh, C1_X, NODE_X_Y, RAIL_GND, label=f"C1 · {CAPACITOR}")
    E.resistor(sh, R2_X, (NODE_X_Y + S.TAPE_W / 2 + NODE_Y[0]) / 2, vertical=True, lead=12, label=f"R2 · {R_LED}")
    E.resistor(sh, B2_X, (rail_edge + NODE_Z[0]) / 2, vertical=True, lead=12, label=f"R3 · {R_LED}")
    for x, label in ((R2_X, "LED1"), (B2_X, "LED2")):
        E.led(sh, x, LED_CY, anode="up", lead_anode=12, lead_cathode=11, label=label)
    E.test_point(sh, 74, RAIL_SW, "TP1", side="above")
    E.test_point(sh, 115, NODE_X_Y, "TP2", side="above")
    E.test_point(sh, B2_X, 91, "TP3")
    E.test_point(sh, 176, RAIL_GND, "TP4")
    for x, name in ((R2_X, "LED1 · with C1"), (B2_X, "LED2 · no capacitor")):
        sh.text(x, RAIL_GND + 9, name, size=6.5, bold=True, color=MUTED, align="center")


def _instructions(sh):
    lesson.need_and_steps(sh, PAGE_ID, [
        "2 red LEDs, 5 mm",
        f"R1: {R_CHARGE} ({R_CHARGE_BANDS}) {POWER}",
        f"R2, R3: {R_LED} ({R_LED_BANDS}) {POWER}",
        f"C1: {CAPACITOR} electrolytic capacitor, 10 V or more",
        "5 mm copper tape; P1 in the binder; a multimeter",
    ], [
        "Lay the six lanes, one piece of tape each. Fold at the creases; never cut.",
        SWITCH_STEP,
        HOLE_STEP,
        "Place R1, R2 and R3 across their gaps, either way round.",
        "Place C1 <b>exactly as printed</b>: the striped leg (−) down to GND, the other leg up to "
        "the lane. Backwards, a capacitor can heat up and fail.",
        "Place LED1 and LED2 as printed: long leg on the +.",
        LEAD_STEP,
        "Bind with P1. Hold the corner down, then let go and watch both LEDs. "
        "If C1 ever feels warm, switch BT1 off and check it.",
    ], (54.0, 136.0, 104.0, 196.0), (110.0, 136.0, 202.0, 196.0))


def _schematic(sh):
    lesson.schematic_panel(sh)
    top, node_x, node_y, bottom = 216.0, 238.0, 252.0, 268.0
    c1, r1, r2, b2 = 44.0, 52.0, 66.0, 84.0
    sch.terminal(sh, 38, top, "V+", label_y=top - 3.4)
    sch.switch(sh, 38.8, 48, top, "S1")
    sch.wire(sh, [(48, top), (b2, top), (b2, top + 0.01)])
    for x in (r1, 60):
        sch.junction(sh, x, top)
    sch.wire(sh, [(60, top), (60, 213.5)])
    sch.test_point(sh, 60, 212.6, "TP1")

    sch.resistor(sh, r1, top, 234, "R1", R_CHARGE)
    sch.wire(sh, [(r1, 234), (r1, node_x), (c1, node_x), (c1, node_x + 0.01)])
    sch.wire(sh, [(r1, node_x), (r2, node_x)])
    sch.junction(sh, r1, node_x)
    sch.capacitor(sh, c1, node_x, bottom, "C1", CAPACITOR)
    sch.junction(sh, 58, node_x)
    sch.wire(sh, [(58, node_x), (58, 234.5)])
    sch.test_point(sh, 58, 233.6, "TP2")
    sch.resistor(sh, r2, node_x, node_y, "R2", R_LED)
    sch.led(sh, r2, node_y, bottom, "LED1")

    sch.resistor(sh, b2, top, 240, "R3", R_LED)
    sch.junction(sh, b2, 240)
    sch.wire(sh, [(b2, 240), (b2 + 4.5, 240)])
    sch.test_point(sh, b2 + 5.4, 240, "TP3")
    sch.led(sh, b2, 240, bottom, "LED2")

    sch.wire(sh, [(38.8, bottom), (b2, bottom), (b2, bottom - 0.01)])
    sch.terminal(sh, 38, bottom, "GND", label_y=bottom + 5)
    for x in (c1, r2, 60):
        sch.junction(sh, x, bottom)
    sch.wire(sh, [(60, bottom), (60, 270.5)])
    sch.test_point(sh, 60, 271.4, "TP4")
    lesson.schematic_note(sh, "C1 charges while S1 is held down.")


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2

    _, py0, _, _ = boxes[0]
    E.workbook_box(sh, boxes[0], "Predict", "When you let go of the corner, what will each LED do?")
    sh.runs(tx, py0 + 12, [("LED1  ", True), ("goes out at once  /  fades", False)], size=7.5)
    sh.runs(tx + 50, py0 + 12, [("LED2  ", True), ("goes out at once  /  fades", False)], size=7.5)
    sh.text(tx, py0 + 19.5, "Circle one for each. Why do you think so?", size=7, color=MUTED)

    _, my0, _, _ = boxes[1]
    E.workbook_box(sh, boxes[1], "Measure", "Count the seconds each LED glows after you let go.")
    lesson.answer_table(sh, tx, my0 + 9.3, "Press", ("A quick tap", "Hold 1 s", "Hold 5 s"),
                        ("LED1", "LED2"), label_w=22, pitch=18, box_w=11, unit="s")
    sh.text(tx + 64, my0 + 9.3, "Black probe on TP4:", size=6.5, bold=True, color=MUTED)
    sh.text(tx + 64, my0 + 14.1, "TP2 when LED1", size=6.5, color=MUTED)
    sh.runs(tx + 64, my0 + 18.9, [("goes dark  ", False), ("____ V", True)], size=6.5, color=MUTED)

    _, ey0, _, _ = boxes[2]
    E.workbook_box(sh, boxes[2], "Explain", "Where does LED1's light come from after you let go?")
    sh.text(tx, ey0 + 9, "How could you make it glow for longer?", size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
