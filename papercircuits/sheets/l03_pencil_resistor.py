"""L03: Draw a resistor.

A heavy 6B pencil track is a resistor. The V+ lane runs alongside track A, and a cut-out
wiper with copper underneath joins the two wherever it's pressed. Current then flows
through the track to R1's lead, which lies across the track's end, and on through LED1.
Sliding the wiper away from R1 puts more pencil in the circuit and dims the LED.

R1 keeps LED1 safe when the wiper sits right on R1's lead. Track B is narrower and only
for measuring, so learners can compare resistance by length and by width.
"""

from reportlab.platypus import Paragraph

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..draw import COPPER, INK, MUTED, Sheet, style
from ..provisional import HEADER_STATUS, HOLE_STEP, POWER, T0, T1, TAG_NOTE_WITH_T1

PAGE_ID = "L03"

# Waiting on the T0 contact tests. T0 doesn't test a lead held on pencil; see the notes.
LEAD_STEP = f"Hold R1's bottom lead and both LED1 leads flat with a patch of copper tape. {T0}"
# Waiting on the T1 pencil tests (K4 is this join).
PENCIL_STEP = (f"Lay R1's top lead flat across the end of track A and hold it down with clear tape. "
               f"Its bottom lead goes on the lane below. Either way round works. {T1}")

# Provisional with the power page (standard §7).
RESISTOR = "220 Ω"
RESISTOR_BANDS = "red-red-brown"

V_PLUS_Y = 50.0
TRACK_A = (46.0, 57.5, 146.0, 72.5)   # 100 × 15 mm
TRACK_B = (46.0, 96.0, 126.0, 100.0)  # 80 × 4 mm
R1_X, R1_CY = 140.0, 80.0
N_TOP, N_Y, N_END = 88.0, 104.0, 165.0
LED_X = 170.0
GND_X = 178.0
WIPER = (156.0, 118.0, 168.0, 154.0)
WIPER_STRIP = 30.0
MEASURE_MARKS = (10, 20, 40, 80)


def build(path):
    sh = Sheet(path, "L03 Draw a resistor")
    E.header(
        sh, PAGE_ID, "L03  Draw a resistor",
        "A pencil line conducts, a little. Slide a wiper along one to dim an LED.",
        status=HEADER_STATUS,
    )
    _tracks(sh)
    _lanes(sh)
    E.spine(sh, connected=("H2", "H3"))
    _parts(sh)
    _need(sh)
    _steps(sh)
    _schematic(sh)
    _workbook(sh)
    E.footer(sh, PAGE_ID)
    sh.save()


def _tracks(sh):
    E.pencil_track(sh, *TRACK_A, last_number=90)
    sh.text(TRACK_A[0], TRACK_A[3] + 9.5, "Track A · 15 mm wide", size=6.5, bold=True, color=MUTED)
    E.pencil_track(sh, *TRACK_B)
    sh.text(TRACK_B[0], TRACK_B[1] - 2, "Track B · 4 mm wide", size=6.5, bold=True, color=MUTED)


def _lanes(sh):
    x_in = S.NET_STRIP_START_X
    E.lane(sh, [(x_in, S.hole_y("H2")), (40, S.hole_y("H2")), (40, V_PLUS_Y), (TRACK_A[2] + 6, V_PLUS_Y)])
    sh.text(TRACK_A[2] + 8, V_PLUS_Y + 1.2, "V+", size=6.5, bold=True, color=COPPER)
    E.lane(sh, [(R1_X, N_TOP), (R1_X, N_Y), (N_END, N_Y)])
    E.lane(sh, [(x_in, S.hole_y("H3")), (GND_X, S.hole_y("H3")), (GND_X, N_Y - 6)])


def _parts(sh):
    E.resistor(sh, R1_X, R1_CY, vertical=True, lead=22, label=f"R1 · {RESISTOR}")
    E.led(sh, LED_X, N_Y, anode="left", lead_anode=13, lead_cathode=11, label="LED1")
    E.wiper_card(sh, *WIPER, WIPER_STRIP)


def _items(texts, numbered):
    return lesson.items(texts, numbered, space_after=1.0)


def _need(sh):
    h = style(8.5, bold=True, spaceAfter=1.2)
    first = [Paragraph("You need", h)] + _items([
        "LED1: bright red LED, 5 mm, clear lens",
        f"R1: {RESISTOR} ({RESISTOR_BANDS}) {POWER}",
        "A soft 6B pencil and an eraser",
    ], numbered=False)
    second = _items([
        "5 mm copper tape and clear tape",
        "Scissors",
        "Power page P1; a multimeter",
    ], numbered=False)
    heading_h = (h.leading + h.spaceAfter) / 72 * 25.4
    rest = sh.flow([(46.0, 27.0, 112.0, 46.0)], first) + sh.flow([(116.0, 27.0 + heading_h, 170.0, 46.0)], second)
    if rest:
        raise RuntimeError(f"L03 parts list overflowed by {len(rest)} items")


def _steps(sh):
    story = [Paragraph("Build it", style(8.5, bold=True, spaceAfter=1.5))] + _items([
        "Shade track A and track B with the 6B pencil. Press hard and go over each one at least 10 times, "
        "until it shines. Stay inside the lines.",
        "Rub out any pencil in the gap between track A and the V+ lane. A smudge there joins them.",
        "Lay the three lanes, one piece of tape each. Fold at the creases; never cut.",
        HOLE_STEP,
        PENCIL_STEP,
        "Place LED1 as printed: long leg on the +.",
        LEAD_STEP,
        f"Cut out the wiper. Stick {WIPER_STRIP:g} mm of tape on it where marked, then turn it copper side down.",
        "Bind this page with P1 and switch BT1 on. Press the wiper across the V+ lane and track A, then slide it.",
    ], numbered=True)
    story.append(lesson.tag_note(TAG_NOTE_WITH_T1))
    rest = sh.flow([(S.ZONE_BUILD[0], 113.0, 150.0, 184.0)], story)
    if rest:
        raise RuntimeError(f"L03 build steps overflowed by {len(rest)} items")


def _schematic(sh):
    lesson.schematic_panel(sh)

    term_x, wiper_x, x = 44.0, 58.0, 66.0
    top, wiper_y, box = 214.0, 232.0, (222.0, 242.0)
    sch.terminal(sh, term_x, top, "", 0)
    sh.text(term_x - 2, top + 1.2, "V+", size=6.5, bold=True, align="right")
    sch.wire(sh, [(term_x + 0.8, top), (wiper_x, top), (wiper_x, wiper_y)])
    sch.rheostat(sh, x, *box, wiper_y, wiper_x, "Track A", "pencil")
    sh.text(wiper_x - 1.2, wiper_y - 2, "wiper", size=6, color=MUTED, align="right")
    sch.resistor(sh, x, box[1], 258, "R1", RESISTOR)
    sch.led(sh, x, 258, 274, "LED1")
    sch.terminal(sh, term_x, 274, "", 0)
    sh.text(term_x - 2, 275.2, "GND", size=6.5, bold=True, align="right")
    sch.wire(sh, [(term_x + 0.8, 274), (x, 274), (x, 273.99)])
    lesson.schematic_note(sh, "The wiper sets how much line is in the loop.")


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2

    _, py0, _, _ = boxes[0]
    E.workbook_box(sh, boxes[0], "Predict", "Where will LED1 be brightest?")
    sh.runs(tx, py0 + 11, [("Wiper  ", True), ("near R1  /  far from R1  /  no difference", False)], size=7.5)
    sh.text(tx, py0 + 18.5, "Circle one. Why do you think so?", size=7, color=MUTED)

    _, my0, _, _ = boxes[1]
    E.workbook_box(sh, boxes[1], "Measure", "Switch BT1 off. Probe each track at 0 and at a mark.")
    col_x, pitch, box_w = tx + 18, 20.0, 13.0
    for j, mark in enumerate(MEASURE_MARKS):
        sh.text(col_x + j * pitch + box_w / 2, my0 + 9.5, f"{mark} mm", size=6.5, bold=True, color=MUTED, align="center")
    for i, row in enumerate(("Track A", "Track B")):
        ry = my0 + 15 + i * 6
        sh.text(tx, ry, row, size=7, bold=True)
        for j in range(len(MEASURE_MARKS)):
            bx = col_x + j * pitch
            sh.rect(bx, ry - 3.6, bx + box_w, ry + 1.2, stroke=INK, width=0.25)
            sh.text(bx + box_w + 1, ry, "kΩ", size=6, color=MUTED)

    _, ey0, ex1, _ = boxes[2]
    E.workbook_box(sh, boxes[2], "Explain", "What does a longer line do to resistance?")
    sh.text(tx, ey0 + 9, "And a narrower one? Use your Measure readings.", size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
