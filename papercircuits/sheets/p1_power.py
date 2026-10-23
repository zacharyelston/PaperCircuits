"""P1: the power page.

BT1 (3 × AA with its own on/off switch) feeds V+ through F1, a resettable fuse, into H2.
BT1's negative goes straight to H3. LED1 and R1 sit after the fuse as a "book is on"
light: it shows the bus is live and the fuse hasn't tripped, and reminds learners to
switch off.

Each node is one strip (standard §4): the wire ends lie along their lanes, and R1 and
LED1 land on the V+ and GND strips as those pass.
"""

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..draw import COPPER, GUIDE, MUTED, Sheet, style
from ..provisional import HEADER_STATUS, HOLE_STEP, POWER, T0

PAGE_ID = "P1"

# Waiting on the power decision (standard §7). 1 kΩ keeps LED1 near 2.4 mA at 4.5 V.
SUPPLY = "4.5 V"
CELLS = "3 AA alkaline cells"
FUSE = "0.1 A hold"
INDICATOR_R = "1 kΩ"
INDICATOR_R_BANDS = "brown-black-red"

# Waiting on the T0 contact tests.
WIRE_STEP = f"Strip 8 mm from each wire and twist it. Lay red along BAT+ and black along GND. {T0}"
LEAD_STEP = f"Hold every lead and wire end flat with a patch of copper tape. {T0}"
BINDER_NOTE = (
    f"BT1 is about 16 mm thick, so P1 goes last in the binder with the holder facing the back "
    f"cover. Check the rings or posts still close over it. {T0}"
)

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
    sh = Sheet(path, "P1 power page")
    E.header(
        sh, PAGE_ID, "P1  Power page",
        "3 × AA through a resettable fuse into V+ (H2) and GND (H3). Build it first.",
        status=HEADER_STATUS,
    )
    _lanes(sh)
    E.spine(sh, connected=("H2", "H3"))
    _parts(sh)
    _instructions(sh)
    _binder_note(sh)
    _schematic(sh)
    _workbook(sh)
    E.footer(sh, PAGE_ID)
    sh.save()


def _lanes(sh):
    x_in = S.NET_STRIP_START_X
    E.lane(sh, [(x_in, V_PLUS_Y), (FUSE_GAP[0], V_PLUS_Y)])
    E.lane(sh, [(FUSE_GAP[1], V_PLUS_Y), (BAT_PLUS_END, V_PLUS_Y)])
    E.lane(sh, [(x_in, GND_Y), (GND_TURN_X, GND_Y), (GND_TURN_X, GND_WIRE_Y), (BAT_PLUS_END, GND_WIRE_Y)])
    E.lane(sh, [(IND_X, IND_NODE[0]), (IND_X, IND_NODE[1])])
    sh.text(122, V_PLUS_Y + 6, "BAT+", size=6, bold=True, color=COPPER, align="center")
    sh.text(122, GND_WIRE_Y + 6, "GND", size=6, bold=True, color=COPPER, align="center")


def _parts(sh):
    hx, hy = HOLDER
    E.battery_holder(sh, hx, hy, label="BT1 · 3 × AA holder with on/off switch")
    E.wire_lead(sh, hx, 118, V_PLUS_Y)
    E.wire_lead(sh, hx, 120, GND_WIRE_Y)
    sh.text(hx - 1, V_PLUS_Y - 3.2, "red", size=6, color=MUTED, align="right")
    sh.text(hx - 1, GND_WIRE_Y + 5.2, "black", size=6, color=MUTED, align="right")

    E.ptc(sh, sum(FUSE_GAP) / 2, V_PLUS_Y, label=f"F1 · {FUSE}")
    r_cy = (V_PLUS_Y + S.TAPE_W / 2 + IND_NODE[0]) / 2
    E.resistor(sh, IND_X, r_cy, vertical=True, lead=12, label=f"R1 · {INDICATOR_R}")
    led_cy = (IND_NODE[1] + GND_Y - S.TAPE_W / 2) / 2
    E.led(sh, IND_X, led_cy, anode="up", lead_anode=13, lead_cathode=11, label="LED1 · green")

    E.test_point(sh, 110, V_PLUS_Y, "TP1", side="above")
    E.test_point(sh, 74, V_PLUS_Y, "TP2", side="above")
    E.test_point(sh, GND_TURN_X, 162, "TP3")


def _instructions(sh):
    lesson.need_and_steps(sh, PAGE_ID, [
        f"BT1: 3 × AA holder with an on/off switch and wire leads {POWER}",
        f"{CELLS} {POWER}",
        f"F1: resettable fuse (PTC), {FUSE} {POWER}",
        f"R1: {INDICATOR_R} ({INDICATOR_R_BANDS}) {POWER}",
        "LED1: green LED, 5 mm",
        "5 mm copper tape, double-sided foam tape",
    ], [
        "Lay the four lanes, one piece of tape each. Fold at the creases; never cut.",
        HOLE_STEP,
        "Stick BT1 down with foam tape, wires toward the spine.",
        WIRE_STEP,
        "Place F1 and R1 across their gaps, either way round. Place LED1 as printed: long leg on the +.",
        LEAD_STEP,
        "Fit the cells, switch BT1 on and fill in Check. Then switch it off.",
    ], (38.0, 31.0, 92.0, 99.0), (98.0, 31.0, 170.0, 99.0))


def _binder_note(sh):
    x0, y0, x1, y1 = 126.0, 159.0, S.ZONE_BUILD[2], 196.0
    sh.rect(x0, y0, x1, y1, stroke=GUIDE, width=0.25, radius=1.2)
    h = sh.paragraph(x0 + 2, y0 + 2, x1 - x0 - 4, "<b>Where P1 goes</b>", style(7.5))
    h += sh.paragraph(x0 + 2, y0 + 3 + h, x1 - x0 - 4, BINDER_NOTE, style(7, leading=8.8))
    sh.paragraph(x0 + 2, y0 + 4.5 + h, x1 - x0 - 4,
                 "Switch BT1 off after each lesson. LED1 is lit whenever the book is on, as a reminder.",
                 style(7, leading=8.8))


def _schematic(sh):
    lesson.schematic_panel(sh)

    top, bottom = 218.0, 266.0
    bx, ind_x, out_x = 42.0, 84.0, 94.0
    sch.battery(sh, bx, top, bottom, "BT1", SUPPLY)
    sch.switch(sh, bx, 54, top, "SW")
    sch.fuse(sh, 58, 72, top, "F1", FUSE.replace(" hold", ""))
    sch.wire(sh, [(54, top), (58, top)])
    sch.wire(sh, [(72, top), (out_x - 0.8, top)])
    for x, label in ((56.0, "TP1"), (76.0, "TP2")):
        sch.junction(sh, x, top)
        sch.wire(sh, [(x, top), (x, 213.5)])
        sch.test_point(sh, x, 212.6, label)

    sch.junction(sh, ind_x, top)
    sch.resistor(sh, ind_x, top, 236, "R1", INDICATOR_R)
    sch.led(sh, ind_x, 236, bottom, "LED1")
    sch.terminal(sh, out_x, top, "V+", label_y=top - 3.4, align="right")

    sch.wire(sh, [(bx, bottom), (out_x - 0.8, bottom)])
    sch.junction(sh, ind_x, bottom)
    sch.terminal(sh, out_x, bottom, "GND", label_y=bottom + 5, align="right")
    sch.junction(sh, 62, bottom)
    sch.wire(sh, [(62, bottom), (62, 270.5)])
    sch.test_point(sh, 62, 271.4, "TP3")
    lesson.schematic_note(sh, "SW is the switch built into the holder.")


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2

    _, cy0, _, _ = boxes[0]
    E.workbook_box(sh, boxes[0], "Check", "Switch BT1 on. Black probe on TP3.")
    for i, label in enumerate(("TP1", "TP2")):
        sh.runs(tx + i * 32, cy0 + 11, [(label + "  ", True), ("_______ V", False)], size=7.5)
    sh.runs(tx + 64, cy0 + 11, [("LED1 lit?  ", True), ("Y / N", False)], size=7.5)
    sh.text(tx, cy0 + 18.5, "Fresh cells read about 4.5–4.8 V. TP1 and TP2 should match.", size=7, color=MUTED)

    _, ey0, ex1, _ = boxes[1]
    E.workbook_box(sh, boxes[1], "Explain", "F1 is a fuse that resets itself.")
    sh.text(tx, ey0 + 9, "What could happen to the book if something shorted and F1 wasn't there?", size=7)
    lesson.write_lines(sh, boxes[1], (15.5, 21.5))

    _, by0, _, _ = boxes[2]
    E.workbook_box(sh, boxes[2], "Before you bind it", "Tick each one.")
    for i, item in enumerate((
        "BT1 is switched off.",
        "No bare wire end touches the other lane.",
        "P1 is the last page in the binder.",
    )):
        y = by0 + 10.5 + i * 5.5
        E.checkbox(sh, tx, y)
        sh.text(tx + 5, y, item, size=7)
