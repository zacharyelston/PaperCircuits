"""P1: the power page.

BT1 (3 × AA with its own on/off switch) feeds V+ through F1, a resettable fuse, into H2.
BT1's negative goes straight to H3. LED1 and R1 sit after the fuse as a "book is on"
light: it shows the bus is live and the fuse hasn't tripped, and reminds learners to
switch off.

Each node is one strip (standard §4): the wire ends lie along their lanes, and R1 and
LED1 land on the V+ and GND strips as those pass.

The page is built in three layers: CIRCUIT says what it is, the functions below say
where things go, and p1_power.md holds the words.
"""

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..circuit import BAT, LED, Circuit, F, R
from ..draw import COPPER, GUIDE, MUTED, Sheet, style
from ..placement import Placement
from ..provisional import HEADER_STATUS
from ..words import Words, number

PAGE_ID = "P1"

# Waiting on the power decision (standard §7). 1 kΩ keeps LED1 near 2.4 mA at 4.5 V.
CIRCUIT = Circuit(
    BAT("BT1", plus="BAT+", minus="GND", note="3 × AA holder with on/off switch"),
    F("F1", "BAT+", "V+", note="0.1 A hold"),
    R("R1", 1e3, "V+", "N1"),
    LED("LED1", anode="N1", cathode="GND", note="green"),
)
SUPPLY = "4.5 V"  # BT1's voltage, for the schematic: the circuit layer's BAT takes none
WORDS = Words.beside(__file__, CIRCUIT)

V_PLUS_Y = S.hole_y("H2")
GND_Y = S.hole_y("H3")
FUSE_GAP = (88.0, 98.0)
BAT_PLUS_END = 130.0
GND_TURN_X = 110.0
GND_WIRE_Y = 140.0
HOLDER = (136.0, 102.0)
IND_X = 56.0
IND_NODE = (121.0, 176.0)


def build(path):
    sh = Sheet(path, WORDS.text("PDF title"))
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
        (38.0, 31.0, 92.0, 99.0),
        (98.0, 31.0, 170.0, 99.0),
    )
    _binder_note(sh)
    _schematic(sh, lay)
    _workbook(sh)
    E.footer(sh, PAGE_ID)
    lay.check(listed=WORDS.refs("You need"))
    sh.save()


def _lanes(lay):
    x_in = S.NET_STRIP_START_X
    lay.lane("V+", [(x_in, V_PLUS_Y), (FUSE_GAP[0], V_PLUS_Y)])
    lay.lane("BAT+", [(FUSE_GAP[1], V_PLUS_Y), (BAT_PLUS_END, V_PLUS_Y)])
    lay.lane("GND", [(x_in, GND_Y), (GND_TURN_X, GND_Y), (GND_TURN_X, GND_WIRE_Y), (BAT_PLUS_END, GND_WIRE_Y)])
    lay.lane("N1", [(IND_X, IND_NODE[0]), (IND_X, IND_NODE[1])])
    for net, y in (("BAT+", V_PLUS_Y), ("GND", GND_WIRE_Y)):
        lay.sh.text(122, y + 6, net, size=6, bold=True, color=COPPER, align="center")


def _parts(lay):
    sh = lay.sh
    hx, hy = HOLDER
    lay.battery("BT1", hx, hy, plus=(118, V_PLUS_Y), minus=(120, GND_WIRE_Y), label="value")
    wires = WORDS.fields("Labels")
    sh.text(hx - 1, V_PLUS_Y - 3.2, wires["plus"], size=6, color=MUTED, align="right")
    sh.text(hx - 1, GND_WIRE_Y + 5.2, wires["minus"], size=6, color=MUTED, align="right")

    lay.ptc("F1", sum(FUSE_GAP) / 2, V_PLUS_Y, label="value")
    r_cy = (V_PLUS_Y + S.TAPE_W / 2 + IND_NODE[0]) / 2
    lay.resistor("R1", IND_X, r_cy, vertical=True, lead=12, label="value")
    led_cy = (IND_NODE[1] + GND_Y - S.TAPE_W / 2) / 2
    lay.led("LED1", IND_X, led_cy, anode="up", lead_anode=13, lead_cathode=11, label="value")

    lay.test_point("BAT+", 110, V_PLUS_Y, "TP1", side="above")
    lay.test_point("V+", 74, V_PLUS_Y, "TP2", side="above")
    lay.test_point("GND", GND_TURN_X, 162, "TP3")


def _binder_note(sh):
    x0, y0, x1, y1 = 126.0, 159.0, S.ZONE_BUILD[2], 196.0
    note, reminder = WORDS.items("Where P1 goes")
    sh.rect(x0, y0, x1, y1, stroke=GUIDE, width=0.25, radius=1.2)
    h = sh.paragraph(x0 + 2, y0 + 2, x1 - x0 - 4, "<b>Where P1 goes</b>", style(7.5))
    h += sh.paragraph(x0 + 2, y0 + 3 + h, x1 - x0 - 4, note, style(7, leading=8.8))
    sh.paragraph(x0 + 2, y0 + 4.5 + h, x1 - x0 - 4, reminder, style(7, leading=8.8))


def _schematic(sh, lay):
    lesson.schematic_panel(sh)

    top, bottom = 218.0, 266.0
    bx, ind_x, out_x = 42.0, 84.0, 94.0
    sch.battery(sh, bx, top, bottom, lay.symbol("BT1").ref, SUPPLY)
    sch.switch(sh, bx, 54, top, "SW")
    fuse = lay.symbol("F1")
    sch.fuse(sh, 58, 72, top, fuse.ref, fuse.text.replace(" hold", ""))
    sch.wire(sh, [(54, top), (58, top)])
    sch.wire(sh, [(72, top), (out_x - 0.8, top)])
    for x, label in ((56.0, "TP1"), (76.0, "TP2")):
        sch.junction(sh, x, top)
        sch.wire(sh, [(x, top), (x, 213.5)])
        sch.test_point(sh, x, 212.6, lay.probe(label))

    sch.junction(sh, ind_x, top)
    res = lay.symbol("R1")
    sch.resistor(sh, ind_x, top, 236, res.ref, res.text)
    sch.led(sh, ind_x, 236, bottom, lay.symbol("LED1").ref)
    sch.terminal(sh, out_x, top, "V+", label_y=top - 3.4, align="right")

    sch.wire(sh, [(bx, bottom), (out_x - 0.8, bottom)])
    sch.junction(sh, ind_x, bottom)
    sch.terminal(sh, out_x, bottom, "GND", label_y=bottom + 5, align="right")
    sch.junction(sh, 62, bottom)
    sch.wire(sh, [(62, bottom), (62, 270.5)])
    sch.test_point(sh, 62, 271.4, lay.probe("TP3"))
    lesson.schematic_note(sh, WORDS.text("Schematic note"))


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2

    _, cy0, _, _ = boxes[0]
    check = WORDS.fields("Check")
    E.workbook_box(sh, boxes[0], "Check", check["prompt"])
    for i, label in enumerate(("TP1", "TP2")):
        sh.runs(tx + i * 32, cy0 + 11, [(label + "  ", True), ("_______ V", False)], size=7.5)
    sh.runs(tx + 64, cy0 + 11, [(check["lit"] + "  ", True), (check["yes_no"], False)], size=7.5)
    sh.text(tx, cy0 + 18.5, check["note"], size=7, color=MUTED)

    _, ey0, ex1, _ = boxes[1]
    explain = WORDS.fields("Explain")
    E.workbook_box(sh, boxes[1], "Explain", explain["prompt"])
    sh.text(tx, ey0 + 9, explain["question"], size=7)
    lesson.write_lines(sh, boxes[1], (15.5, 21.5))

    _, by0, _, _ = boxes[2]
    prompt, *ticks = WORDS.items("Before you bind it")
    E.workbook_box(sh, boxes[2], "Before you bind it", prompt)
    for i, item in enumerate(ticks):
        y = by0 + 10.5 + i * 5.5
        E.checkbox(sh, tx, y)
        sh.text(tx + 5, y, item, size=7)
