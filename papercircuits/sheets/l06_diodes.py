"""L06: Diodes are one-way valves.

Two branches off the switched rail, each a resistor, a small diode and an LED. D1 points
the way current flows, so LED1 lights, a little dimmer than it would without D1. D2 is
printed reversed on purpose, so LED2 stays dark. Measuring both sides of each diode shows
D1 takes about 0.7 V while D2 blocks almost the whole supply, and that the voltages
round a loop add up to the supply.

The page is built in three layers: CIRCUIT says what it is (D2's reversal included), the
functions below say where things go, and l06_diodes.md holds the words.
"""

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..circuit import LED, SW, Circuit, D, R
from ..draw import MUTED, Sheet
from ..placement import Placement
from ..provisional import HEADER_STATUS
from ..words import Words, number

PAGE_ID = "L06"

CIRCUIT = Circuit(
    SW("S1", "V+", "VSW"),
    # Provisional with the power page (standard §7): about 9 mA through branch 1 at 4.5 V.
    R("R1", 220, "VSW", "N1"),
    R("R2", 220, "VSW", "N3"),
    D("D1", anode="N1", cathode="N2", note="1N4148"),
    D("D2", anode="N4", cathode="N3", note="1N4148"),  # backwards on purpose
    LED("LED1", anode="N2", cathode="GND", note="red, 5 mm"),
    LED("LED2", anode="N4", cathode="GND", note="red, 5 mm"),
)
WORDS = Words.beside(__file__, CIRCUIT)

# Each branch: its x; resistor, diode and LED; and the nets above and below the diode,
# each with its test point.
BRANCHES = (
    (95.0, "R1", "D1", "LED1", ("N1", "TP2"), ("N2", "TP3")),
    (150.0, "R2", "D2", "LED2", ("N3", "TP4"), ("N4", "TP5")),
)
RAIL_TOP, RAIL_SW, RAIL_GND = 46.0, 62.0, 137.5
SW_JOG = (34.0, 194.0)
NODE_X = (74.5, 95.0)  # resistor to diode
NODE_Y = (105.0, 125.0)  # diode to LED
R_CY = (RAIL_SW + S.TAPE_W / 2 + NODE_X[0]) / 2
D_CY = (NODE_X[1] + NODE_Y[0]) / 2
LED_CY = (NODE_Y[1] + RAIL_GND - S.TAPE_W / 2) / 2


def build(path):
    sh = Sheet(path, " ".join(WORDS.title.split()))
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, status=HEADER_STATUS)
    lay = Placement(sh, CIRCUIT)
    _lanes(lay)
    E.spine(sh, connected=("H2", "H3"))
    _parts(lay)
    lesson.need_and_steps(
        sh,
        PAGE_ID,
        WORDS.items("You need"),
        WORDS.items("Build it", lanes=number(lay.laid)),
        (54.0, 151.0, 104.0, 196.0),
        (110.0, 151.0, 202.0, 196.0),
    )
    _schematic(sh, lay)
    _workbook(sh)
    E.footer(sh, PAGE_ID)
    lay.check(listed=WORDS.refs("You need"))
    sh.save()


def _lanes(lay):
    sw_in, sw_out = S.SWITCH_LANE_X
    jog_y, jog_x = SW_JOG
    x_in = S.NET_STRIP_START_X
    v_in = lay.lane(
        "V+",
        [(x_in, S.hole_y("H2")), (40, S.hole_y("H2")), (40, RAIL_TOP), (sw_in, RAIL_TOP), (sw_in, S.SWITCH_LANE_TOP)],
    )
    v_sw = lay.lane(
        "VSW", [(sw_out, S.SWITCH_LANE_TOP), (sw_out, jog_y), (jog_x, jog_y), (jog_x, RAIL_SW), (75, RAIL_SW)]
    )
    lay.sh.allow(v_in, v_sw, S.SWITCH_PAD_GAP)
    for bx, _, _, _, (upper, _), (lower, _) in BRANCHES:
        lay.lane(upper, [(bx, NODE_X[0]), (bx, NODE_X[1])])
        lay.lane(lower, [(bx, NODE_Y[0]), (bx, NODE_Y[1])])
    lay.lane("GND", [(x_in, S.hole_y("H3")), (45, S.hole_y("H3")), (45, RAIL_GND), (180, RAIL_GND)])
    lay.fold_switch("S1", stubs=False)
    label_x = sw_in - S.TAPE_W / 2 - 2
    lay.sh.text(label_x, 29.5, "S1", size=7, bold=True, align="right")
    lay.sh.text(label_x, 33, WORDS.fields("Labels")["switch"], size=6, color=MUTED, align="right")


def _parts(lay):
    for bx, r, d, led, (upper, tp_upper), (lower, tp_lower) in BRANCHES:
        lay.resistor(r, bx, R_CY, vertical=True, lead=11, label="value")
        cathode = "down" if CIRCUIT[d].pins["cathode"] == lower else "up"
        lay.diode(d, bx, D_CY, lead=9, cathode=cathode)
        lay.led(led, bx, LED_CY, anode="up", lead_anode=12, lead_cathode=11)
        lay.test_point(upper, bx, (R_CY + 11 + D_CY - 9) / 2, tp_upper)
        lay.test_point(lower, bx, (D_CY + 9 + LED_CY - 12) / 2, tp_lower)
    lay.test_point("VSW", 80, RAIL_SW, "TP1", side="above")
    lay.test_point("GND", 176, RAIL_GND, "TP6")
    labels = WORDS.fields("Labels")
    for (bx, *_), name in zip(BRANCHES, (labels["forward"], labels["reversed"])):
        lay.sh.text(bx, RAIL_GND + 8, name, size=6.5, bold=True, color=MUTED, align="center")


def _schematic(sh, lay):
    lesson.schematic_panel(sh)
    top, x_node, y_node, bottom = 216.0, 232.0, 248.0, 268.0
    branches = (58.0, 82.0)
    sch.terminal(sh, 40, top, "V+", label_y=top - 3.4)
    sch.switch(sh, 40.8, 52, top, lay.symbol("S1").ref)
    sch.wire(sh, [(52, top), (branches[1], top), (branches[1], top + 0.01)])
    sch.junction(sh, branches[0], top)
    sch.junction(sh, 70, top)
    sch.wire(sh, [(70, top), (70, 213.5)])
    sch.test_point(sh, 70, 212.6, lay.probe("TP1"))
    for i, ((_, r, d, led, (_, tp_upper), (lower, tp_lower)), bx) in enumerate(zip(BRANCHES, branches), 1):
        res, diode = lay.symbol(r), lay.symbol(d)
        sch.resistor(sh, bx, top, x_node, res.ref, res.text)
        sch.diode(sh, bx, x_node, y_node, diode.ref, cathode_bottom=diode.pins["cathode"] == lower)
        sch.led(sh, bx, y_node, bottom, lay.symbol(led).ref)
        side = -1 if i == 1 else 1
        for y, tp in ((x_node, tp_upper), (y_node, tp_lower)):
            sch.junction(sh, bx, y)
            sch.wire(sh, [(bx, y), (bx + side * 4.5, y)])
            sch.test_point(sh, bx + side * 5.4, y, lay.probe(tp), side="left" if i == 1 else "right")
    sch.wire(sh, [(40.8, bottom), (branches[1], bottom), (branches[1], bottom - 0.01)])
    sch.terminal(sh, 40, bottom, "GND", label_y=bottom + 5)
    sch.junction(sh, branches[0], bottom)
    sch.junction(sh, 70, bottom)
    sch.wire(sh, [(70, bottom), (70, 270.5)])
    sch.test_point(sh, 70, 271.4, lay.probe("TP6"))
    lesson.schematic_note(sh, WORDS.text("Schematic note"))


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2
    leds = [led for _, _, _, led, _, _ in BRANCHES]

    _, py0, _, _ = boxes[0]
    predict = WORDS.fields("Predict")
    E.workbook_box(sh, boxes[0], "Predict", predict["prompt"])
    sh.text(tx, py0 + 9.5, predict["question"], size=7)
    for j, led in enumerate(leds):
        sh.runs(tx + 50 * j, py0 + 17, [(f"{led}  ", True), (predict["choices"], False)], size=7.5)
    sh.text(tx, py0 + 22.5, predict["why"], size=7, color=MUTED)

    _, my0, _, _ = boxes[1]
    measure = WORDS.fields("Measure")
    E.workbook_box(sh, boxes[1], "Measure", measure["prompt"])
    lesson.answer_table(
        sh,
        tx,
        my0 + 9.3,
        measure["table"],
        (measure["D1"], measure["D2"]),
        (measure["before"], measure["after"], measure["across"]),
        label_w=26,
        pitch=22,
        box_w=14,
        row_h=5.4,
        unit="V",
    )
    sh.text(tx + 26, my0 + 23.2, measure["rule"], size=6.5, color=MUTED)

    _, ey0, _, _ = boxes[2]
    explain = WORDS.fields("Explain")
    E.workbook_box(sh, boxes[2], "Explain", explain["prompt"])
    sh.text(tx, ey0 + 9, explain["question"], size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
