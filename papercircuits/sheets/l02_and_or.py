"""L02: Two switches, two ways.

Top circuit: tab switches A1 and B1 in series feed R1 and LED1, so LED1 needs both (AND).
Bottom circuit: A2 and B2 in parallel feed R2 and LED2, so either will do (OR).

Each tab switch folds over a switch pair (standard §6). In series the chain zig-zags
between the pair's two rows: V+ on the lower row, M on the upper, N back on the lower.
One V+ strip serves both circuits: it passes A1, drops between A1 and B1, then runs
under both OR flaps as the upper lane of the bottom pair.

The page is built in three layers: CIRCUIT says what it is, the functions below say
where things go, and l02_and_or.md holds the words.
"""

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..circuit import LED, SW, Circuit, R
from ..draw import Sheet
from ..placement import Placement
from ..provisional import HEADER_STATUS
from ..words import Words, number

PAGE_ID = "L02"

CIRCUIT = Circuit(
    SW("A1", "V+", "M"),
    SW("B1", "M", "N"),
    SW("A2", "V+", "OUT"),
    SW("B2", "V+", "OUT"),
    # Provisional with the power page (standard §7): 220 Ω gives about 11 mA from 4.5 V.
    R("R1", 220, "N", "N1"),
    R("R2", 220, "OUT", "N2"),
    LED("LED1", anode="N1", cathode="GND", note="red, 5 mm"),
    LED("LED2", anode="N2", cathode="GND", note="red, 5 mm"),
)
WORDS = Words.beside(__file__, CIRCUIT)

AND_UPPER = 56.0  # M, between A1 and B1
AND_LOWER = AND_UPPER + S.PAIR_PITCH  # V+ into A1, then N out of B1
OR_UPPER = 120.0  # V+ past A2 and B2
OR_LOWER = OR_UPPER + S.PAIR_PITCH  # OUT, past A2 and B2
A1_X, B1_X = 70.0, 110.0
A2_X, B2_X = 110.0, 140.0
V_DROP_X = 86.0  # V+ drops from the AND row to the OR row here
GND_X = 194.0
LED_X = 186.0
R1_X, R2_X = 145.0, 165.0

# Each tab switch: its ref, x and the upper lane of the pair it folds over.
SWITCHES = (("A1", A1_X, AND_UPPER), ("B1", B1_X, AND_UPPER), ("A2", A2_X, OR_UPPER), ("B2", B2_X, OR_UPPER))


def build(path):
    sh = Sheet(path, " ".join(WORDS.title.split()))
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, status=HEADER_STATUS)
    lay = Placement(sh, CIRCUIT)
    _lanes(lay)
    E.spine(sh, connected=("H2", "H3"))
    _switches(lay)
    _parts(lay)
    lesson.need_and_steps(
        sh,
        PAGE_ID,
        WORDS.items("You need"),
        WORDS.items("Build it", lanes=number(lay.laid), pad_gap=f"{S.SWITCH_PAD_GAP:g}"),
        (38.0, 137.0, 90.0, 184.0),
        (96.0, 137.0, 189.0, 184.0),
    )
    _schematic(sh, lay)
    _workbook(sh)
    E.footer(sh, PAGE_ID)
    lay.check(listed=WORDS.refs("You need"))
    sh.save()


def _lanes(lay):
    x_in = S.NET_STRIP_START_X
    v_plus, gnd = S.hole_y("H2"), S.hole_y("H3")
    v_in = lay.lane(
        "V+",
        [
            (x_in, v_plus),
            (40, v_plus),
            (40, AND_LOWER),
            (V_DROP_X, AND_LOWER),
            (V_DROP_X, OR_UPPER),
            (B2_X + 6, OR_UPPER),
        ],
    )
    m = lay.lane("M", [(A1_X - 8, AND_UPPER), (B1_X + 8, AND_UPPER)])
    n = lay.lane("N", [(B1_X - 8, AND_LOWER), (R1_X - 5, AND_LOWER)])
    lay.lane("N1", [(R1_X + 5, AND_LOWER), (LED_X - 5, AND_LOWER)])
    out = lay.lane("OUT", [(A2_X - 8, OR_LOWER), (R2_X - 5, OR_LOWER)])
    for a, b in ((v_in, m), (m, n), (v_in, out)):
        lay.sh.allow(a, b, S.SWITCH_PAD_GAP)
    lay.lane("N2", [(R2_X + 5, OR_LOWER), (LED_X - 5, OR_LOWER)])
    lay.lane("GND", [(x_in, gnd), (GND_X, gnd), (GND_X, AND_UPPER)])


def _switches(lay):
    for ref, x, upper in SWITCHES:
        lay.tab_switch(ref, x, upper)


def _parts(lay):
    lay.resistor("R1", R1_X, AND_LOWER, vertical=False, lead=12, label="value")
    lay.resistor("R2", R2_X, OR_LOWER, vertical=False, lead=10, label="value")
    for y, led in ((AND_LOWER, "LED1"), (OR_LOWER, "LED2")):
        lay.led(led, LED_X, y, anode="left", lead_anode=13, lead_cathode=11)
    lay.test_point("N", 124, AND_LOWER, "TP1", side="above")
    lay.test_point("OUT", 151, OR_LOWER, "TP2", side="below")
    lay.test_point("GND", GND_X, 95, "TP3", side="left")


def _schematic(sh, lay):
    lesson.schematic_panel(sh)

    rail, and_y, or_a, or_b, gnd = 44.0, 218.0, 232.0, 242.0, 270.0
    and_x, or_x, join_x = 84.0, 70.0, 60.0
    sch.terminal(sh, rail, 212, "", 0)
    sh.text(rail - 2, 213.2, "V+", size=6.5, bold=True, align="right")
    sch.wire(sh, [(rail, 212.8), (rail, or_b)])
    sch.junction(sh, rail, and_y)
    sch.junction(sh, rail, or_a)

    sch.switch(sh, rail, 55, and_y, lay.symbol("A1").ref)
    sch.switch(sh, 55, 66, and_y, lay.symbol("B1").ref)
    sch.wire(sh, [(66, and_y), (and_x, and_y)])
    r1 = lay.symbol("R1")
    sch.resistor(sh, and_x, and_y, 238, r1.ref, r1.text)
    sch.junction(sh, and_x, 238)
    sch.wire(sh, [(and_x, 238), (and_x + 4, 238)])
    sch.test_point(sh, and_x + 4.9, 238, lay.probe("TP1"))
    sch.led(sh, and_x, 238, gnd, lay.symbol("LED1").ref)

    sch.switch(sh, rail, 56, or_a, lay.symbol("A2").ref)
    sch.switch(sh, rail, 56, or_b, lay.symbol("B2").ref)
    sch.wire(sh, [(56, or_b), (join_x, or_b), (join_x, or_a)])
    sch.wire(sh, [(56, or_a), (or_x, or_a)])
    sch.junction(sh, join_x, or_a)
    r2 = lay.symbol("R2")
    sch.resistor(sh, or_x, or_a, 250, r2.ref, r2.text)
    sch.junction(sh, or_x, 250)
    sch.wire(sh, [(or_x, 250), (or_x - 4, 250)])
    sch.test_point(sh, or_x - 4.9, 250, lay.probe("TP2"), side="left")
    sch.led(sh, or_x, 250, gnd, lay.symbol("LED2").ref)

    sch.terminal(sh, rail, gnd, "", 0)
    sh.text(rail - 2, gnd + 1.2, "GND", size=6.5, bold=True, align="right")
    sch.wire(sh, [(rail + 0.8, gnd), (and_x, gnd), (and_x, gnd - 0.01)])
    sch.junction(sh, or_x, gnd)
    sch.junction(sh, 56, gnd)
    sch.wire(sh, [(56, gnd), (56, 274.5)])
    sch.test_point(sh, 56, 275.4, lay.probe("TP3"))
    lesson.schematic_note(sh, WORDS.text("Schematic note"))


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2
    tables = WORDS.fields("Tables")
    and_rows, or_rows = WORDS.items("Top rows"), WORDS.items("Bottom rows")

    _, py0, _, _ = boxes[0]
    E.workbook_box(sh, boxes[0], "Predict", WORDS.fields("Predict")["prompt"])
    lesson.answer_table(sh, tx, py0 + 9.3, tables["top"], and_rows, ("LED1",))
    lesson.answer_table(sh, tx + 50, py0 + 9.3, tables["bottom"], or_rows, ("LED2",))

    _, ty0, _, _ = boxes[1]
    E.workbook_box(sh, boxes[1], "Test", WORDS.fields("Test")["prompt"])
    lesson.answer_table(sh, tx, ty0 + 9.3, tables["top"], and_rows, ("LED1", "TP1 V"))
    lesson.answer_table(sh, tx + 50, ty0 + 9.3, tables["bottom"], or_rows, ("LED2", "TP2 V"))

    _, ey0, _, _ = boxes[2]
    explain = WORDS.fields("Explain")
    E.workbook_box(sh, boxes[2], "Explain", explain["prompt"])
    sh.text(tx, ey0 + 9, explain["question"], size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
