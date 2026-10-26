"""L04: Resistors set the current.

Three branches, each a resistor and an LED, hang off the switched V+ rail. The resistors
are 220 Ω, 1 kΩ and 4.7 kΩ, so the LEDs glow bright, medium and dim. Learners sort the
resistors by colour code, then measure the voltage across each one and work out the
current with Ohm's law. The voltage across each resistor comes out nearly the same; the
current is what changes.

Layout follows L01: V+ climbs to the corner switch, and the switched rail and GND rail
pass every branch, so each node is one strip.

The page is built in three layers: CIRCUIT says what it is, the functions below say
where things go, and l04_resistors.md holds the words.
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

PAGE_ID = "L04"

CIRCUIT = Circuit(
    SW("S1", "V+", "VSW"),
    # Provisional with the power page (standard §7): about 12, 2.7 and 0.6 mA from 4.5 V.
    R("R1", 220, "VSW", "N1"),
    R("R2", 1e3, "VSW", "N2"),
    R("R3", 4.7e3, "VSW", "N3"),
    LED("LED1", anode="N1", cathode="GND", note="red, 5 mm"),
    LED("LED2", anode="N2", cathode="GND", note="red, 5 mm"),
    LED("LED3", anode="N3", cathode="GND", note="red, 5 mm"),
)
WORDS = Words.beside(__file__, CIRCUIT)

# Each branch: its node's net, resistor, LED, test point, and x.
BRANCHES = (("N1", "R1", "LED1", "TP2", 85.0), ("N2", "R2", "LED2", "TP3", 125.0), ("N3", "R3", "LED3", "TP4", 165.0))
RAIL_TOP, RAIL_SW, RAIL_GND = 46.0, 62.0, 124.5
NODE = (74.5, 112.0)
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
        (54.0, 136.0, 104.0, 162.0),
        (110.0, 136.0, 202.0, 196.0),
    )
    E.colour_code_key(sh, 54, 167)
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
        "VSW", [(sw_out, S.SWITCH_LANE_TOP), (sw_out, jog_y), (jog_x, jog_y), (jog_x, RAIL_SW), (70, RAIL_SW)]
    )
    lay.sh.allow(v_in, v_sw, S.SWITCH_PAD_GAP)
    for net, _, _, _, bx in BRANCHES:
        lay.lane(net, [(bx, NODE[0]), (bx, NODE[1])])
    lay.lane("GND", [(x_in, S.hole_y("H3")), (45, S.hole_y("H3")), (45, RAIL_GND), (180, RAIL_GND)])
    lay.fold_switch("S1", stubs=False)
    label_x = sw_in - S.TAPE_W / 2 - 2
    lay.sh.text(label_x, 29.5, "S1", size=7, bold=True, align="right")
    lay.sh.text(label_x, 33, WORDS.fields("Labels")["switch"], size=6, color=MUTED, align="right")


def _parts(lay):
    for net, r, led, tp, bx in BRANCHES:
        lay.resistor(r, bx, R_CY, vertical=True, lead=12, label="value")
        lay.led(led, bx, LED_CY, anode="up", lead_anode=13, lead_cathode=11)
        lay.test_point(net, bx, TP_NODE_Y, tp)
    lay.test_point("VSW", 74, RAIL_SW, "TP1", side="above")
    lay.test_point("GND", 176, RAIL_GND, "TP5")


def _schematic(sh, lay):
    lesson.schematic_panel(sh)
    top, node, bottom = 216.0, 238.0, 268.0
    xs = (52.0, 68.0, 84.0)
    sch.terminal(sh, 40, top, "V+", label_y=top - 3.4)
    sch.switch(sh, 40.8, 49, top, lay.symbol("S1").ref)
    sch.wire(sh, [(49, top), (xs[-1], top), (xs[-1], top + 0.01)])
    sch.junction(sh, 60, top)
    sch.wire(sh, [(60, top), (60, 213.5)])
    sch.test_point(sh, 60, 212.6, lay.probe("TP1"))
    for i, ((_, r, led, tp, _), bx) in enumerate(zip(BRANCHES, xs), 1):
        if i < len(xs):
            sch.junction(sh, bx, top)
        res = lay.symbol(r)
        sch.resistor(sh, bx, top, node - 4, res.ref, res.text)
        sch.wire(sh, [(bx, node - 4), (bx, node)])
        sch.junction(sh, bx, node)
        sch.wire(sh, [(bx, node), (bx - 4.5, node)])
        sch.test_point(sh, bx - 5.4, node, lay.probe(tp), side="left")
        sch.led(sh, bx, node, bottom, lay.symbol(led).ref)
        if i < len(xs):
            sch.junction(sh, bx, bottom)
    sch.wire(sh, [(40.8, bottom), (xs[-1], bottom), (xs[-1], bottom - 0.01)])
    sch.terminal(sh, 40, bottom, "GND", label_y=bottom + 5)
    sch.junction(sh, 60, bottom)
    sch.wire(sh, [(60, bottom), (60, 270.5)])
    sch.test_point(sh, 60, 271.4, lay.probe("TP5"))
    lesson.schematic_note(sh, WORDS.text("Schematic note"))


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2

    _, py0, _, _ = boxes[0]
    predict = WORDS.fields("Predict")
    E.workbook_box(sh, boxes[0], "Predict", predict["prompt"])
    sh.runs(
        tx,
        py0 + 12,
        [
            (f"{predict['brightest']}  ", True),
            ("_________    _________    _________", False),
            (f"  {predict['dimmest']}", True),
        ],
        size=7.5,
    )
    sh.text(tx, py0 + 19.5, predict["why"], size=7, color=MUTED)

    _, my0, _, _ = boxes[1]
    measure = WORDS.fields("Measure", R1_kohm=f"{CIRCUIT['R1'].value / 1e3:g}")
    E.workbook_box(sh, boxes[1], "Measure", measure["prompt"])
    rows = [f"{r}  {CIRCUIT[r].text}" for _, r, _, _, _ in BRANCHES]
    lesson.answer_table(
        sh,
        tx,
        my0 + 9.3,
        measure["across"],
        rows,
        (measure["volts"], measure["current"]),
        label_w=26,
        pitch=20,
        box_w=14,
    )
    sh.text(tx + 70, my0 + 14.1, measure["rule"], size=7, bold=True, color=MUTED)
    sh.text(tx + 70, my0 + 18.9, measure["hint"], size=6.5, color=MUTED)

    _, ey0, _, _ = boxes[2]
    explain = WORDS.fields("Explain")
    E.workbook_box(sh, boxes[2], "Explain", explain["prompt"])
    sh.text(tx, ey0 + 9, explain["question"], size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
