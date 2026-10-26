"""L01: LEDs only work one way.

Two identical branches, a resistor and an LED, hang off the switched V+ rail. LED2 is
printed reversed on purpose: the learner predicts, sees one LED stay dark, then measures
why. Nothing has to be lifted and re-attached, so the page works with any lead method T0
picks.

Each node is one continuous strip routed past every lead on it, so the page has no
T-junctions (standard §4).

The page is built in three layers: CIRCUIT says what it is (LED2's reversal included),
the functions below say where things go, and l01_led_polarity.md holds the words.
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

PAGE_ID = "L01"

CIRCUIT = Circuit(
    SW("S1", "V+", "VSW"),
    # Provisional with the power page (standard §7): 220 Ω gives about 11 mA from 4.5 V.
    R("R1", 220, "VSW", "N1"),
    R("R2", 220, "VSW", "N2"),
    LED("LED1", anode="N1", cathode="GND", note="red, 5 mm"),
    LED("LED2", anode="GND", cathode="N2", note="red, 5 mm"),  # backwards on purpose
)
WORDS = Words.beside(__file__, CIRCUIT)

# Each branch: its node's net, resistor, LED, test point, and x.
BRANCHES = (("N1", "R1", "LED1", "TP2", 95.0), ("N2", "R2", "LED2", "TP3", 150.0))
RAIL_TOP = 46.0  # unswitched V+, on its way to the switch
RAIL_SW = 62.0  # switched V+, past R1 and R2
RAIL_GND = 124.5  # GND, past LED1 and LED2
NODE = (74.5, 112.0)  # each branch's lane between its resistor and LED
SW_JOG = (34.0, 194.0)

R_CY = (RAIL_SW + S.TAPE_W / 2 + NODE[0]) / 2
LED_CY = (NODE[1] + RAIL_GND - S.TAPE_W / 2) / 2
TP_NODE_Y = (NODE[0] + NODE[1]) / 2


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
        (54.0, 137.0, 104.0, 196.0),
        (110.0, 137.0, 202.0, 196.0),
    )
    _schematic(sh, lay)
    _workbook(sh)
    E.footer(sh, PAGE_ID)
    lay.check(listed=WORDS.refs("You need"))
    sh.save()


def _lanes(lay):
    sw_in, sw_out = S.SWITCH_LANE_X
    jog_y, jog_x = SW_JOG
    v_plus, gnd = S.hole_y("H2"), S.hole_y("H3")
    x_in = S.NET_STRIP_START_X
    # V+ from H2, up the left side and along the top into the switch.
    v_in = lay.lane("V+", [(x_in, v_plus), (40, v_plus), (40, RAIL_TOP), (sw_in, RAIL_TOP), (sw_in, S.SWITCH_LANE_TOP)])
    # Switched V+: out of the switch, jog clear of the V+ lane, then along the rail.
    v_sw = lay.lane(
        "VSW", [(sw_out, S.SWITCH_LANE_TOP), (sw_out, jog_y), (jog_x, jog_y), (jog_x, RAIL_SW), (75, RAIL_SW)]
    )
    lay.sh.allow(v_in, v_sw, S.SWITCH_PAD_GAP)
    for net, _, _, _, bx in BRANCHES:
        lay.lane(net, [(bx, NODE[0]), (bx, NODE[1])])
    lay.lane("GND", [(x_in, gnd), (45, gnd), (45, RAIL_GND), (170, RAIL_GND)])

    lay.fold_switch("S1", stubs=False)
    label_x = sw_in - S.TAPE_W / 2 - 2
    lay.sh.text(label_x, 29.5, "S1", size=7, bold=True, align="right")
    lay.sh.text(label_x, 33, WORDS.fields("Labels")["switch"], size=6, color=MUTED, align="right")


def _parts(lay):
    for net, r, led, tp, bx in BRANCHES:
        lay.resistor(r, bx, R_CY, vertical=True, lead=12, label="value")
        anode = "up" if CIRCUIT[led].pins["anode"] == net else "down"
        lay.led(led, bx, LED_CY, anode=anode, lead_anode=13, lead_cathode=11)
        lay.test_point(net, bx, TP_NODE_Y, tp)
    lay.test_point("VSW", 78, RAIL_SW, "TP1", side="above")
    lay.test_point("GND", 166, RAIL_GND, "TP4")


def _schematic(sh, lay):
    lesson.schematic_panel(sh)

    top, node, bottom = 218.0, 238.0, 266.0
    xs = (60.0, 84.0)
    sch.terminal(sh, 40, top, "V+", label_y=top - 3.4)
    sch.switch(sh, 40.8, 53, top, lay.symbol("S1").ref)
    sch.wire(sh, [(53, top), (xs[1], top), (xs[1], top + 0.01)])
    sch.junction(sh, xs[0], top)
    sch.wire(sh, [(70, top), (70, 213.5)])
    sch.junction(sh, 70, top)
    sch.test_point(sh, 70, 212.6, lay.probe("TP1"))

    for (net, r, led, tp, _), bx in zip(BRANCHES, xs):
        res = lay.symbol(r)
        sch.resistor(sh, bx, top, node - 4, res.ref, res.text)
        sch.wire(sh, [(bx, node - 4), (bx, node)])
        sch.junction(sh, bx, node)
        sch.wire(sh, [(bx, node), (bx - 4.5, node)])
        sch.test_point(sh, bx - 5.4, node, lay.probe(tp), side="left")
        diode = lay.symbol(led)
        sch.led(sh, bx, node, bottom, diode.ref, anode_top=diode.pins["anode"] == net)

    sch.wire(sh, [(40.8, bottom), (xs[1], bottom), (xs[1], bottom - 0.01)])
    sch.terminal(sh, 40, bottom, "GND", label_y=bottom + 5)
    sch.junction(sh, xs[0], bottom)
    sch.wire(sh, [(70, bottom), (70, 270.5)])
    sch.junction(sh, 70, bottom)
    sch.test_point(sh, 70, 271.4, lay.probe("TP4"))
    lesson.schematic_note(sh, WORDS.text("Schematic note"))


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2
    leds = [led for _, _, led, _, _ in BRANCHES]

    _, by0, _, _ = boxes[0]
    predict = WORDS.fields("Predict")
    E.workbook_box(sh, boxes[0], "Predict", predict["prompt"])
    sh.text(tx, by0 + 9.5, predict["question"], size=7)
    for j, led in enumerate(leds):
        sh.runs(tx + 50 * j, by0 + 17, [(f"{led}  ", True), (predict["choices"], False)], size=7.5)
    sh.text(tx, by0 + 22.5, predict["why"], size=7, color=MUTED)

    _, my0, _, _ = boxes[1]
    measure = WORDS.fields("Measure")
    E.workbook_box(sh, boxes[1], "Measure", measure["prompt"])
    for i, label in enumerate(("TP1", "TP2", "TP3")):
        sh.runs(tx + i * 32, my0 + 11, [(label + "  ", True), ("_______ V", False)], size=7.5)
    sh.runs(
        tx,
        my0 + 19,
        [
            (f"{measure['lit']}   {leds[0]}  ", True),
            (measure["yes_no"], False),
            (f"      {leds[1]}  ", True),
            (measure["yes_no"], False),
        ],
        size=7.5,
    )

    _, ey0, _, _ = boxes[2]
    explain = WORDS.fields("Explain")
    E.workbook_box(sh, boxes[2], "Explain", explain["prompt"])
    sh.text(tx, ey0 + 9, explain["question"], size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
