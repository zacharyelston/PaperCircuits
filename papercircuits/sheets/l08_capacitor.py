"""L08: Store some charge.

Two LEDs on the switched rail. LED2 has just a resistor, so it goes out the moment S1
is released. LED1 sits behind node X, where C1 (2200 µF) charges through R1 while S1 is
held. Let go, and C1 keeps LED1 lit through R2, fading over a few seconds.

Node X is one strip passing R1's lower lead, C1's + leg and R2's upper lead. C1 lies on
its side beside the strip, its legs bent up to node X and down to GND.

The page is built in three layers: CIRCUIT says what it is, the functions below say
where things go, and l08_capacitor.md holds the words.
"""

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..circuit import CE, LED, SW, Circuit, R
from ..draw import MUTED, Sheet
from ..placement import Placement
from ..provisional import HEADER_STATUS
from ..words import Words, number

PAGE_ID = "L08"

CIRCUIT = Circuit(
    SW("S1", "V+", "VSW"),
    # Provisional with the power page (standard §7): LED1 fades over roughly 3 s at 4.5 V.
    R("R1", 100, "VSW", "X"),
    CE("C1", 2200e-6, plus="X", minus="GND"),
    R("R2", 470, "X", "Y"),
    R("R3", 470, "VSW", "Z"),
    LED("LED1", anode="Y", cathode="GND", note="red, 5 mm"),
    LED("LED2", anode="Z", cathode="GND", note="red, 5 mm"),
)
WORDS = Words.beside(__file__, CIRCUIT)

RAIL_TOP, RAIL_SW, RAIL_GND = 46.0, 62.0, 120.0
SW_JOG = (34.0, 194.0)
NODE_X_Y = 80.0
NODE_X_SPAN = (78.0, 132.0)
R1_X, C1_X, R2_X, B2_X = 85.0, 105.0, 125.0, 160.0
NODE_Y = (92.5, 107.5)
NODE_Z = (74.5, 107.5)
LED_CY = (NODE_Y[1] + RAIL_GND - S.TAPE_W / 2) / 2


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
        (54.0, 136.0, 104.0, 196.0), (110.0, 136.0, 202.0, 196.0))
    _schematic(sh, lay)
    _workbook(sh)
    E.footer(sh, PAGE_ID)
    lay.check(listed=WORDS.refs("You need"))
    sh.save()


def _lanes(lay):
    sw_in, sw_out = S.SWITCH_LANE_X
    jog_y, jog_x = SW_JOG
    x_in = S.NET_STRIP_START_X
    v_in = lay.lane("V+", [(x_in, S.hole_y("H2")), (40, S.hole_y("H2")), (40, RAIL_TOP), (sw_in, RAIL_TOP),
                           (sw_in, S.SWITCH_LANE_TOP)])
    v_sw = lay.lane("VSW", [(sw_out, S.SWITCH_LANE_TOP), (sw_out, jog_y), (jog_x, jog_y), (jog_x, RAIL_SW),
                            (70, RAIL_SW)])
    lay.sh.allow(v_in, v_sw, S.SWITCH_PAD_GAP)
    lay.lane("X", [(NODE_X_SPAN[0], NODE_X_Y), (NODE_X_SPAN[1], NODE_X_Y)])
    lay.lane("Y", [(R2_X, NODE_Y[0]), (R2_X, NODE_Y[1])])
    lay.lane("Z", [(B2_X, NODE_Z[0]), (B2_X, NODE_Z[1])])
    lay.lane("GND", [(x_in, S.hole_y("H3")), (45, S.hole_y("H3")), (45, RAIL_GND), (180, RAIL_GND)])
    lay.fold_switch("S1", stubs=False)
    label_x = sw_in - S.TAPE_W / 2 - 2
    lay.sh.text(label_x, 29.5, "S1", size=7, bold=True, align="right")
    lay.sh.text(label_x, 33, WORDS.fields("Labels")["switch"], size=6, color=MUTED, align="right")


def _parts(lay):
    rail_edge, x_edge = RAIL_SW + S.TAPE_W / 2, NODE_X_Y - S.TAPE_W / 2
    lay.resistor("R1", R1_X, (rail_edge + x_edge) / 2, vertical=True, lead=12, label="value")
    lay.electrolytic("C1", C1_X, NODE_X_Y, RAIL_GND, label="value")
    lay.resistor("R2", R2_X, (NODE_X_Y + S.TAPE_W / 2 + NODE_Y[0]) / 2, vertical=True, lead=12, label="value")
    lay.resistor("R3", B2_X, (rail_edge + NODE_Z[0]) / 2, vertical=True, lead=12, label="value")
    for x, ref in ((R2_X, "LED1"), (B2_X, "LED2")):
        lay.led(ref, x, LED_CY, anode="up", lead_anode=12, lead_cathode=11)
    lay.test_point("VSW", 74, RAIL_SW, "TP1", side="above")
    lay.test_point("X", 115, NODE_X_Y, "TP2", side="above")
    lay.test_point("Z", B2_X, 91, "TP3")
    lay.test_point("GND", 176, RAIL_GND, "TP4")
    labels = WORDS.fields("Labels")
    for x, name in ((R2_X, labels["with"]), (B2_X, labels["without"])):
        lay.sh.text(x, RAIL_GND + 9, name, size=6.5, bold=True, color=MUTED, align="center")


def _schematic(sh, lay):
    lesson.schematic_panel(sh)
    top, node_x, node_y, bottom = 216.0, 238.0, 252.0, 268.0
    c1, r1, r2, b2 = 44.0, 52.0, 66.0, 84.0
    sch.terminal(sh, 38, top, "V+", label_y=top - 3.4)
    sch.switch(sh, 38.8, 48, top, lay.symbol("S1").ref)
    sch.wire(sh, [(48, top), (b2, top), (b2, top + 0.01)])
    for x in (r1, 60):
        sch.junction(sh, x, top)
    sch.wire(sh, [(60, top), (60, 213.5)])
    sch.test_point(sh, 60, 212.6, lay.probe("TP1"))

    res1 = lay.symbol("R1")
    sch.resistor(sh, r1, top, 234, res1.ref, res1.text)
    sch.wire(sh, [(r1, 234), (r1, node_x), (c1, node_x), (c1, node_x + 0.01)])
    sch.wire(sh, [(r1, node_x), (r2, node_x)])
    sch.junction(sh, r1, node_x)
    cap = lay.symbol("C1")
    sch.capacitor(sh, c1, node_x, bottom, cap.ref, cap.text)
    sch.junction(sh, 58, node_x)
    sch.wire(sh, [(58, node_x), (58, 234.5)])
    sch.test_point(sh, 58, 233.6, lay.probe("TP2"))
    res2 = lay.symbol("R2")
    sch.resistor(sh, r2, node_x, node_y, res2.ref, res2.text)
    sch.led(sh, r2, node_y, bottom, lay.symbol("LED1").ref)

    res3 = lay.symbol("R3")
    sch.resistor(sh, b2, top, 240, res3.ref, res3.text)
    sch.junction(sh, b2, 240)
    sch.wire(sh, [(b2, 240), (b2 + 4.5, 240)])
    sch.test_point(sh, b2 + 5.4, 240, lay.probe("TP3"))
    sch.led(sh, b2, 240, bottom, lay.symbol("LED2").ref)

    sch.wire(sh, [(38.8, bottom), (b2, bottom), (b2, bottom - 0.01)])
    sch.terminal(sh, 38, bottom, "GND", label_y=bottom + 5)
    for x in (c1, r2, 60):
        sch.junction(sh, x, bottom)
    sch.wire(sh, [(60, bottom), (60, 270.5)])
    sch.test_point(sh, 60, 271.4, lay.probe("TP4"))
    lesson.schematic_note(sh, WORDS.text("Schematic note"))


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2

    _, py0, _, _ = boxes[0]
    predict = WORDS.fields("Predict")
    E.workbook_box(sh, boxes[0], "Predict", predict["prompt"])
    for j, led in enumerate(("LED1", "LED2")):
        sh.runs(tx + 50 * j, py0 + 12, [(f"{led}  ", True), (predict["choices"], False)], size=7.5)
    sh.text(tx, py0 + 19.5, predict["question"], size=7, color=MUTED)

    _, my0, _, _ = boxes[1]
    measure = WORDS.fields("Measure")
    E.workbook_box(sh, boxes[1], "Measure", measure["prompt"])
    lesson.answer_table(sh, tx, my0 + 9.3, measure["table"], (measure["tap"], measure["hold_1"], measure["hold_5"]),
                        ("LED1", "LED2"), label_w=22, pitch=18, box_w=11, unit="s")
    sh.text(tx + 64, my0 + 9.3, measure["probe"], size=6.5, bold=True, color=MUTED)
    sh.text(tx + 64, my0 + 14.1, measure["when"], size=6.5, color=MUTED)
    sh.runs(tx + 64, my0 + 18.9, [(f"{measure['dark']}  ", False), ("____ V", True)], size=6.5, color=MUTED)

    _, ey0, _, _ = boxes[2]
    explain = WORDS.fields("Explain")
    E.workbook_box(sh, boxes[2], "Explain", explain["prompt"])
    sh.text(tx, ey0 + 9, explain["question"], size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
