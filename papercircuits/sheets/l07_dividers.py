"""L07: Share the voltage.

Three voltage dividers hang between the switched rail and GND, each two resistors in a
row with a test point in the middle:
- A: 1 kΩ over 1 kΩ, half the supply.
- B: 2.2 kΩ over 1 kΩ, about a third.
- C: 1 kΩ over 2.2 kΩ, about two thirds.

Learners predict, measure the middles, then work each one out from the ratio. Swapping
top and bottom (B against C) flips the answer. There are no LEDs: this is the page where
the meter does the showing.

The page is built in three layers: CIRCUIT says what it is, the functions below say
where things go, and l07_dividers.md holds the words.
"""

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..circuit import SW, Circuit, R
from ..draw import MUTED, Sheet
from ..placement import Placement
from ..provisional import HEADER_STATUS
from ..words import Words, number

PAGE_ID = "L07"

# Each divider is a top and a bottom resistor with its middle between them, A, B or C.
# The ratios don't depend on the supply.
CIRCUIT = Circuit(
    SW("S1", "V+", "VSW"),
    R("R1", 1e3, "VSW", "A"),
    R("R2", 1e3, "A", "GND"),
    R("R3", 2.2e3, "VSW", "B"),
    R("R4", 1e3, "B", "GND"),
    R("R5", 1e3, "VSW", "C"),
    R("R6", 2.2e3, "C", "GND"),
)
WORDS = Words.beside(__file__, CIRCUIT)

# Each divider: its middle's net, top and bottom resistors, test point, and x.
DIVIDERS = (("A", "R1", "R2", "TP2", 85.0), ("B", "R3", "R4", "TP3", 125.0), ("C", "R5", "R6", "TP4", 165.0))
RAIL_TOP, RAIL_SW, RAIL_GND = 46.0, 62.0, 120.0
SW_JOG = (34.0, 194.0)
MID = (74.5, 105.0)
TOP_CY = (RAIL_SW + S.TAPE_W / 2 + MID[0]) / 2
BOT_CY = (MID[1] + RAIL_GND - S.TAPE_W / 2) / 2
TP_MID_Y = (TOP_CY + 12 + BOT_CY - 12) / 2


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
        (54.0, 136.0, 104.0, 196.0),
        (110.0, 136.0, 202.0, 196.0),
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
        "VSW", [(sw_out, S.SWITCH_LANE_TOP), (sw_out, jog_y), (jog_x, jog_y), (jog_x, RAIL_SW), (70, RAIL_SW)]
    )
    lay.sh.allow(v_in, v_sw, S.SWITCH_PAD_GAP)
    for net, _, _, _, bx in DIVIDERS:
        lay.lane(net, [(bx, MID[0]), (bx, MID[1])])
    lay.lane("GND", [(x_in, S.hole_y("H3")), (45, S.hole_y("H3")), (45, RAIL_GND), (180, RAIL_GND)])
    lay.fold_switch("S1", stubs=False)
    label_x = sw_in - S.TAPE_W / 2 - 2
    lay.sh.text(label_x, 29.5, "S1", size=7, bold=True, align="right")
    lay.sh.text(label_x, 33, WORDS.fields("Labels")["switch"], size=6, color=MUTED, align="right")


def _parts(lay):
    labels = WORDS.fields("Labels")
    for net, r_top, r_bottom, tp, bx in DIVIDERS:
        lay.resistor(r_top, bx, TOP_CY, vertical=True, lead=12, label="value")
        lay.resistor(r_bottom, bx, BOT_CY, vertical=True, lead=12, label="value")
        lay.test_point(net, bx, TP_MID_Y, tp)
        lay.sh.text(bx, RAIL_GND + 9, labels[net], size=6.5, bold=True, color=MUTED, align="center")
    lay.test_point("VSW", 74, RAIL_SW, "TP1", side="above")
    lay.test_point("GND", 176, RAIL_GND, "TP5")


def _schematic(sh, lay):
    lesson.schematic_panel(sh)
    top, mid, bottom = 216.0, 238.0, 262.0
    branches = (52.0, 68.0, 84.0)
    sch.terminal(sh, 40, top, "V+", label_y=top - 3.4)
    sch.switch(sh, 40.8, 49, top, lay.symbol("S1").ref)
    sch.wire(sh, [(49, top), (branches[-1], top), (branches[-1], top + 0.01)])
    sch.junction(sh, 60, top)
    sch.wire(sh, [(60, top), (60, 213.5)])
    sch.test_point(sh, 60, 212.6, lay.probe("TP1"))
    for bx, (_, r_top, r_bottom, tp, _) in zip(branches, DIVIDERS):
        if bx != branches[-1]:
            sch.junction(sh, bx, top)
            sch.junction(sh, bx, bottom)
        upper, lower = lay.symbol(r_top), lay.symbol(r_bottom)
        sch.resistor(sh, bx, top, mid - 4, upper.ref, upper.text)
        sch.wire(sh, [(bx, mid - 4), (bx, mid)])
        sch.junction(sh, bx, mid)
        sch.wire(sh, [(bx, mid), (bx - 4.5, mid)])
        sch.test_point(sh, bx - 5.4, mid, lay.probe(tp), side="left")
        sch.resistor(sh, bx, mid, bottom, lower.ref, lower.text)
    sch.wire(sh, [(40.8, bottom), (branches[-1], bottom), (branches[-1], bottom - 0.01)])
    sch.terminal(sh, 40, bottom, "GND", label_y=bottom + 5)
    sch.junction(sh, 60, bottom)
    sch.wire(sh, [(60, bottom), (60, 264.5)])
    sch.test_point(sh, 60, 265.4, lay.probe("TP5"))
    lesson.schematic_note(sh, WORDS.text("Schematic note"))


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2

    _, py0, _, _ = boxes[0]
    predict = WORDS.fields("Predict")
    E.workbook_box(sh, boxes[0], "Predict", predict["prompt"])
    sh.runs(tx, py0 + 12, [(f"{predict['highest']}  ", True), (predict["choices"], False)], size=7.5)
    sh.text(tx, py0 + 19.5, predict["question"], size=7, color=MUTED)

    _, my0, _, _ = boxes[1]
    measure = WORDS.fields("Measure")
    E.workbook_box(sh, boxes[1], "Measure", measure["prompt"])
    lesson.answer_table(
        sh,
        tx,
        my0 + 9.3,
        measure["table"],
        tuple(measure[net] for net, *_ in DIVIDERS),
        (measure["measured"], measure["worked_out"]),
        label_w=20,
        pitch=21,
        box_w=13,
        unit="V",
    )
    sh.runs(tx + 66, my0 + 9.3, [("TP1  ", True), ("______ V", False)], size=7)
    sh.text(tx + 66, my0 + 15.5, measure["rule"], size=6.5, bold=True, color=MUTED)
    sh.text(tx + 66, my0 + 19.3, measure["rule_top"], size=6.5, color=MUTED)
    sh.text(tx + 66, my0 + 23.1, measure["rule_bottom"], size=6.5, color=MUTED)

    _, ey0, _, _ = boxes[2]
    explain = WORDS.fields("Explain")
    E.workbook_box(sh, boxes[2], "Explain", explain["prompt"])
    sh.text(tx, ey0 + 9, explain["question"], size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
