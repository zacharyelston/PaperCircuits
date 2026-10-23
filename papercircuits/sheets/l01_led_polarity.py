"""L01: LEDs only work one way.

Two identical branches, a resistor and an LED, hang off the switched V+ rail. LED2 is
printed reversed on purpose: the learner predicts, sees one LED stay dark, then measures
why. Nothing has to be lifted and re-attached, so the page works with any lead method T0
picks.

Each node is one continuous strip routed past every lead on it, so the page has no
T-junctions (standard §4).
"""

from reportlab.platypus import Paragraph

from .. import elements as E
from .. import schematic as sch
from .. import standard as S
from ..draw import GUIDE, INK, MUTED, Sheet, style
from ..provisional import HEADER_STATUS, HOLE_STEP, POWER, T0, TAG_NOTE

PAGE_ID = "L01"

# Waiting on the T0 contact tests. Change these when standard v0.2 lands.
LEAD_STEP = f"Hold each lead flat on its lane with a small patch of copper tape. {T0}"
SWITCH_STEP = f"Stick a {S.FLAP_PAD_LEN:g} mm piece of copper tape on the corner flap, S1. {T0}"

# Provisional with the power page (standard §7): 220 Ω gives about 11 mA from 4.5 V.
RESISTOR = "220 Ω"
RESISTOR_BANDS = "red-red-brown"

BRANCH_X = (95.0, 150.0)
RAIL_TOP = 46.0       # unswitched V+, on its way to the switch
RAIL_SW = 62.0        # switched V+, past R1 and R2
RAIL_GND = 124.5      # GND, past LED1 and LED2
NODE = (74.5, 112.0)  # each branch's lane between its resistor and LED
SW_JOG = (34.0, 194.0)

R_CY = (RAIL_SW + S.TAPE_W / 2 + NODE[0]) / 2
LED_CY = (NODE[1] + RAIL_GND - S.TAPE_W / 2) / 2
TP_NODE_Y = (NODE[0] + NODE[1]) / 2


def build(path):
    sh = Sheet(path, "L01 LEDs only work one way")
    E.header(
        sh, PAGE_ID, "L01  LEDs only work one way",
        "Close the loop, then find out why an LED cares which way round it goes.",
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
    v_plus, gnd = S.hole_y("H2"), S.hole_y("H3")
    x_in = S.NET_STRIP_START_X
    # V+ from H2, up the left side and along the top into the switch.
    E.lane(sh, [(x_in, v_plus), (40, v_plus), (40, RAIL_TOP), (sw_in, RAIL_TOP), (sw_in, S.SWITCH_LANE_TOP)])
    # Switched V+: out of the switch, jog clear of the V+ lane, then along the rail.
    E.lane(sh, [(sw_out, S.SWITCH_LANE_TOP), (sw_out, jog_y), (jog_x, jog_y), (jog_x, RAIL_SW), (75, RAIL_SW)])
    for bx in BRANCH_X:
        E.lane(sh, [(bx, NODE[0]), (bx, NODE[1])])
    E.lane(sh, [(x_in, gnd), (45, gnd), (45, RAIL_GND), (170, RAIL_GND)])

    E.fold_switch(sh, stubs=False)
    label_x = sw_in - S.TAPE_W / 2 - 2
    sh.text(label_x, 29.5, "S1", size=7, bold=True, align="right")
    sh.text(label_x, 33, "fold the corner down", size=6, color=MUTED, align="right")


def _parts(sh):
    for i, bx in enumerate(BRANCH_X, 1):
        E.resistor(sh, bx, R_CY, vertical=True, lead=12, label=f"R{i} · {RESISTOR}")
        E.led(sh, bx, LED_CY, anode="up" if i == 1 else "down", lead_anode=13, lead_cathode=11, label=f"LED{i}")
        E.test_point(sh, bx, TP_NODE_Y, f"TP{i + 1}")
    E.test_point(sh, 78, RAIL_SW, "TP1", side="above")
    E.test_point(sh, 166, RAIL_GND, "TP4")


def _instructions(sh):
    h = style(8.5, bold=True, spaceAfter=1.5)

    def items(texts, numbered):
        out = []
        for i, t in enumerate(texts, 1):
            p_style = style(7, leading=8.8, leftIndent=7 if not numbered else 8, bulletIndent=0,
                            bulletFontSize=7, spaceAfter=1.2)
            out.append(Paragraph(t, p_style, bulletText=f"{i}." if numbered else "•"))
        return out

    need = [Paragraph("You need", h)] + items([
        "2 red LEDs, 5 mm",
        f"2 resistors, {RESISTOR} ({RESISTOR_BANDS}) {POWER}",
        "5 mm copper tape",
        "Power page P1 in the binder",
        "A multimeter for Measure",
    ], numbered=False)
    steps = [Paragraph("Build it", h)] + items([
        "Lay the five lanes, one piece of tape each. Fold at the creases; never cut.",
        SWITCH_STEP,
        HOLE_STEP,
        "Place R1 and R2 across their gaps. Either way round works.",
        "Place LED1 and LED2 <b>exactly as printed</b>: long leg on the +.",
        LEAD_STEP,
        "Bind this page with P1, then fold the corner down to switch on.",
    ], numbered=True)
    steps.append(Paragraph(TAG_NOTE, style(6.5, leading=8.2, color=MUTED, spaceBefore=2)))
    rest = sh.flow([(54.0, 137.0, 104.0, 196.0)], need) + sh.flow([(110.0, 137.0, 202.0, 196.0)], steps)
    if rest:
        raise RuntimeError(f"L01 instructions overflowed by {len(rest)} items")


def _schematic(sh):
    x0, y0, x1, y1 = S.ZONE_SCHEMATIC
    sh.rect(x0, y0, x1, y1, stroke=INK, width=0.3, radius=1.2)
    sh.text(x0 + 2, y0 + 4, "Schematic", size=7, bold=True)

    top, node, bottom = 218.0, 238.0, 266.0
    b1, b2 = 60.0, 84.0
    sch.terminal(sh, 40, top, "V+", label_y=top - 3.4)
    sch.switch(sh, 40.8, 53, top, "S1")
    sch.wire(sh, [(53, top), (b2, top), (b2, top + 0.01)])
    sch.junction(sh, b1, top)
    sch.wire(sh, [(70, top), (70, 213.5)])
    sch.junction(sh, 70, top)
    sch.test_point(sh, 70, 212.6, "TP1")

    for i, bx in enumerate((b1, b2), 1):
        sch.resistor(sh, bx, top, node - 4, f"R{i}", RESISTOR)
        sch.wire(sh, [(bx, node - 4), (bx, node)])
        sch.junction(sh, bx, node)
        sch.wire(sh, [(bx, node), (bx - 4.5, node)])
        sch.test_point(sh, bx - 5.4, node, f"TP{i + 1}", side="left")
        sch.led(sh, bx, node, bottom, f"LED{i}", anode_top=i == 1)

    sch.wire(sh, [(40.8, bottom), (b2, bottom), (b2, bottom - 0.01)])
    sch.terminal(sh, 40, bottom, "GND", label_y=bottom + 5)
    sch.junction(sh, b1, bottom)
    sch.wire(sh, [(70, bottom), (70, 270.5)])
    sch.junction(sh, 70, bottom)
    sch.test_point(sh, 70, 271.4, "TP4")
    sh.text(x0 + 2, y1 - 2.5, "V+ and GND come from P1 through the binder.", size=6, color=MUTED)


def _write_lines(sh, x0, x1, ys):
    for y in ys:
        sh.line(x0, y, x1, y, width=0.2, color=GUIDE)


def _workbook(sh):
    x0, y0, x1, y1 = S.ZONE_WORKBOOK
    h = (y1 - y0 - 4) / 3
    boxes = [(x0, y0 + i * (h + 2), x1, y0 + i * (h + 2) + h) for i in range(3)]
    tx = x0 + 2

    bx0, by0, bx1, _ = boxes[0]
    E.workbook_box(sh, boxes[0], "Predict", "LED2 is printed the other way round.")
    sh.text(tx, by0 + 9.5, "When you fold the corner down, which LEDs will light? Circle one for each.", size=7)
    sh.runs(tx, by0 + 17, [("LED1  ", True), ("lights  /  stays dark", False)], size=7.5)
    sh.runs(tx + 50, by0 + 17, [("LED2  ", True), ("lights  /  stays dark", False)], size=7.5)
    sh.text(tx, by0 + 22.5, "Why do you think so?", size=7, color=MUTED)

    _, my0, _, _ = boxes[1]
    E.workbook_box(sh, boxes[1], "Measure", "Hold the corner down. Black probe on TP4, red on each point.")
    for i, label in enumerate(("TP1", "TP2", "TP3")):
        sh.runs(tx + i * 32, my0 + 11, [(label + "  ", True), ("_______ V", False)], size=7.5)
    sh.runs(tx, my0 + 19, [("Lit?   LED1  ", True), ("Y / N", False), ("      LED2  ", True), ("Y / N", False)], size=7.5)

    _, ey0, _, _ = boxes[2]
    E.workbook_box(sh, boxes[2], "Explain", "Why does only one LED light?")
    sh.text(tx, ey0 + 9, "What would you change to make the other one light?", size=7)
    _write_lines(sh, tx, bx1 - 2, (ey0 + 15.5, ey0 + 21.5))
