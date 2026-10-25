"""L05: Two ways to add a resistor.

Three LED branches off the switched rail, all with 470 Ω resistors:
- One: R1 alone, the reference.
- Two in a row: R2 then R3, joined by a middle lane, about 940 Ω.
- Two side by side: R4 and R5 bridge the same gap, about 235 Ω.

The LEDs rank side by side > one > in a row. With BT1 off, the meter reads each group
from TP1 to that branch's test point.

R4 and R5 land on one rail and one node strip, both passing by, so the parallel pair
needs no branching tape (standard §4).

The page is built in three layers: CIRCUIT says what it is, the functions below say
where things go, and l05_series_parallel.md holds the words.
"""

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..circuit import LED, SW, Circuit, R
from ..draw import MUTED, Sheet
from ..placement import Placement
from ..provisional import HEADER_STATUS
from ..words import Words, number

PAGE_ID = "L05"

CIRCUIT = Circuit(
    SW("S1", "V+", "VSW"),
    # Provisional with the power page (standard §7): about 5, 3 and 11 mA from 4.5 V.
    # One: R1 alone.
    R("R1", 470, "VSW", "N1"),
    # Two in a row: R2 then R3, joined by the middle lane.
    R("R2", 470, "VSW", "MID"),
    R("R3", 470, "MID", "N2"),
    # Two side by side: R4 and R5 bridge the same gap.
    R("R4", 470, "VSW", "N3"),
    R("R5", 470, "VSW", "N3"),
    LED("LED1", anode="N1", cathode="GND", note="red, 5 mm"),
    LED("LED2", anode="N2", cathode="GND", note="red, 5 mm"),
    LED("LED3", anode="N3", cathode="GND", note="red, 5 mm"),
)
WORDS = Words.beside(__file__, CIRCUIT)

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
    sh = Sheet(path, " ".join(WORDS.title.split()))
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, status=HEADER_STATUS)
    lay = Placement(sh, CIRCUIT)
    _lanes(lay)
    E.spine(sh, connected=("H2", "H3"))
    _parts(lay)
    lesson.need_and_steps(
        sh, PAGE_ID, WORDS.items("You need"),
        WORDS.items("Build it", lanes=number(lay.laid)),
        (54.0, 151.0, 104.0, 196.0), (110.0, 151.0, 202.0, 196.0))
    _schematic(sh, lay)
    _workbook(sh)
    E.footer(sh, PAGE_ID)
    lay.check(listed=WORDS.refs("You need"))
    sh.save()


def _lanes(lay):
    sw_in, sw_out = S.SWITCH_LANE_X
    jog_y, jog_x = SW_JOG
    x_in = S.NET_STRIP_START_X
    rail_gap = RAIL_SW + S.TAPE_W / 2 + 10
    v_in = lay.lane("V+", [(x_in, S.hole_y("H2")), (40, S.hole_y("H2")), (40, RAIL_TOP), (sw_in, RAIL_TOP),
                           (sw_in, S.SWITCH_LANE_TOP)])
    v_sw = lay.lane("VSW", [(sw_out, S.SWITCH_LANE_TOP), (sw_out, jog_y), (jog_x, jog_y), (jog_x, RAIL_SW),
                            (70, RAIL_SW)])
    lay.sh.allow(v_in, v_sw, S.SWITCH_PAD_GAP)
    lay.lane("N1", [(A_X, rail_gap), (A_X, NODE_END)])
    lay.lane("MID", [(B_X, rail_gap), (B_X, B_M[1])])
    lay.lane("N2", [(B_X, B_M[1] + 10), (B_X, NODE_END)])
    lay.lane("N3", [(C_R_X[0] - 4, C_NODE_Y), (C_X, C_NODE_Y), (C_X, NODE_END)])
    lay.lane("GND", [(x_in, S.hole_y("H3")), (45, S.hole_y("H3")), (45, RAIL_GND), (180, RAIL_GND)])
    lay.fold_switch("S1", stubs=False)
    labels = WORDS.fields("Labels")
    label_x = sw_in - S.TAPE_W / 2 - 2
    lay.sh.text(label_x, 29.5, "S1", size=7, bold=True, align="right")
    lay.sh.text(label_x, 33, labels["switch"], size=6, color=MUTED, align="right")
    lay.sh.text(92, 55, labels["values"], size=6.5, color=MUTED)


def _parts(lay):
    rail_edge = RAIL_SW + S.TAPE_W / 2
    lay.resistor("R1", A_X, rail_edge + 5, vertical=True, lead=12, label="value")
    lay.resistor("R2", B_X, rail_edge + 5, vertical=True, lead=12)
    lay.resistor("R3", B_X, B_M[1] + 5, vertical=True, lead=12)
    c_cy = (rail_edge + C_NODE_Y - S.TAPE_W / 2) / 2
    for ref, x in zip(("R4", "R5"), C_R_X):
        lay.resistor(ref, x, c_cy, vertical=True, lead=12)
    for ref, x in zip(("LED1", "LED2", "LED3"), (A_X, B_X, C_X)):
        lay.led(ref, x, LED_CY, anode="up", lead_anode=13, lead_cathode=11)
    lay.test_point("VSW", 75, RAIL_SW, "TP1", side="above")
    lay.test_point("N1", A_X, 100, "TP2")
    lay.test_point("N2", B_X, 112, "TP3")
    lay.test_point("N3", sum(C_R_X) / 2, C_NODE_Y, "TP4", side="below")
    lay.test_point("GND", 176, RAIL_GND, "TP5")
    labels = WORDS.fields("Labels")
    for x, name in ((A_X, labels["one"]), (B_X, labels["in_a_row"]), (C_X - 8, labels["side_by_side"])):
        lay.sh.text(x, RAIL_GND + 8, name, size=6.5, bold=True, color=MUTED, align="center")


def _schematic(sh, lay):
    lesson.schematic_panel(sh)
    top, bottom = 214.0, 268.0
    a, b, c, c_r = 48.0, 62.0, 83.0, (78.0, 88.0)
    sch.terminal(sh, 38, top, "V+", label_y=top + 5)
    sch.switch(sh, 38.8, 45.5, top, lay.symbol("S1").ref)
    sch.wire(sh, [(45.5, top), (c_r[1], top), (c_r[1], top + 0.01)])
    for x in (a, b, c_r[0]):
        sch.junction(sh, x, top)
    sch.junction(sh, 55, top)
    sch.wire(sh, [(55, top), (55, 211.5)])
    sch.test_point(sh, 55, 210.6, lay.probe("TP1"))

    r1 = lay.symbol("R1")
    sch.resistor(sh, a, top, 232, r1.ref, r1.text)
    sch.wire(sh, [(a, 232), (a, 236)])
    sch.junction(sh, a, 236)
    sch.wire(sh, [(a, 236), (a - 4.5, 236)])
    sch.test_point(sh, a - 5.4, 236, lay.probe("TP2"), side="left")
    sch.led(sh, a, 236, bottom, lay.symbol("LED1").ref)

    sch.resistor(sh, b, top, 230, lay.symbol("R2").ref, "")
    sch.resistor(sh, b, 230, 246, lay.symbol("R3").ref, "")
    sch.wire(sh, [(b, 246), (b, 248)])
    sch.junction(sh, b, 248)
    sch.wire(sh, [(b, 248), (b + 4.5, 248)])
    sch.test_point(sh, b + 5.4, 248, lay.probe("TP3"))
    sch.led(sh, b, 248, bottom, lay.symbol("LED2").ref)

    for ref, x in zip(("R4", "R5"), c_r):
        sch.resistor(sh, x, top, 232, lay.symbol(ref).ref, "")
    sch.wire(sh, [(c_r[0], 232), (c_r[0], 236), (c_r[1], 236), (c_r[1], 232)])
    sch.junction(sh, c, 236)
    sch.wire(sh, [(c, 236), (c, 240)])
    sch.junction(sh, c, 238)
    sch.wire(sh, [(c, 238), (c + 4.5, 238)])
    sch.test_point(sh, c + 5.4, 238, lay.probe("TP4"))
    sch.led(sh, c, 240, bottom, lay.symbol("LED3").ref)

    sch.wire(sh, [(38.8, bottom), (c, bottom), (c, bottom - 0.01)])
    sch.terminal(sh, 38, bottom, "GND", label_y=bottom + 5)
    for x in (a, b):
        sch.junction(sh, x, bottom)
    sch.junction(sh, 55, bottom)
    sch.wire(sh, [(55, bottom), (55, 270.5)])
    sch.test_point(sh, 55, 271.4, lay.probe("TP5"))
    lesson.schematic_note(sh, WORDS.text("Schematic note"))


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2

    _, py0, _, _ = boxes[0]
    predict = WORDS.fields("Predict")
    E.workbook_box(sh, boxes[0], "Predict", predict["prompt"])
    sh.runs(tx, py0 + 12, [(f"{predict['brightest']}  ", True), ("_________    _________    _________", False),
                           (f"  {predict['dimmest']}", True)], size=7.5)
    sh.text(tx, py0 + 19.5, predict["question"], size=7, color=MUTED)

    _, my0, _, _ = boxes[1]
    measure = WORDS.fields("Measure")
    E.workbook_box(sh, boxes[1], "Measure", measure["prompt"])
    lesson.answer_table(sh, tx, my0 + 9.3, measure["table"],
                        (measure["one"], measure["in_a_row"], measure["side_by_side"]), (measure["ohms"],),
                        label_w=40, pitch=24, box_w=16, unit="Ω")
    sh.text(tx + 66, my0 + 14.1, measure["then"], size=7, bold=True, color=MUTED)
    sh.text(tx + 66, my0 + 18.9, measure["match"], size=6.5, color=MUTED)

    _, ey0, _, _ = boxes[2]
    explain = WORDS.fields("Explain")
    E.workbook_box(sh, boxes[2], "Explain", explain["prompt"])
    sh.text(tx, ey0 + 9, explain["question"], size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
