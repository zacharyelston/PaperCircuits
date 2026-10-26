"""L03: Draw a resistor.

A heavy 6B pencil track is a resistor. The V+ lane runs alongside track A, and a cut-out
wiper with copper underneath joins the two wherever it's pressed. Current then flows
through the track to R1's lead, which lies across the track's end, and on through LED1.
Sliding the wiper away from R1 puts more pencil in the circuit and dims the LED.

R1 keeps LED1 safe when the wiper sits right on R1's lead. Track B is narrower and only
for measuring, so learners can compare resistance by length and by width. It isn't part
of the circuit.

The step laying R1's top lead on track A waits on the T1 pencil tests (K4 is this join).
The step holding the other leads waits on the T0 contact tests, which don't test a lead
held on pencil; see the notes.

The page is built in three layers: CIRCUIT says what it is, the functions below say
where things go, and l03_pencil_resistor.md holds the words.
"""

from reportlab.platypus import Paragraph

from .. import elements as E
from .. import lesson
from .. import schematic as sch
from .. import standard as S
from ..circuit import LED, PENCIL, Circuit, R
from ..draw import COPPER, INK, MUTED, Sheet, style
from ..placement import Placement
from ..provisional import HEADER_STATUS, TAG_NOTE_WITH_T1
from ..words import Words, number

PAGE_ID = "L03"

CIRCUIT = Circuit(
    PENCIL("Track A", track="A", wiper="V+", note="pencil"),
    # Provisional with the power page (standard §7).
    R("R1", 220, "A", "N"),
    LED("LED1", anode="N", cathode="GND", note="bright red, 5 mm, clear lens"),
)
WORDS = Words.beside(__file__, CIRCUIT)

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
    sh = Sheet(path, " ".join(WORDS.title.split()))
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, status=HEADER_STATUS)
    lay = Placement(sh, CIRCUIT)
    _tracks(lay)
    _lanes(lay)
    E.spine(sh, connected=("H2", "H3"))
    _parts(lay)
    _need(sh)
    _steps(sh, lay)
    _schematic(sh, lay)
    _workbook(sh)
    E.footer(sh, PAGE_ID)
    lay.check(listed=WORDS.refs("You need"))
    sh.save()


def _labels():
    """The page's drawing labels, with each track's width measured from its outline."""
    width_a, width_b = (f"{y1 - y0:g}" for _, y0, _, y1 in (TRACK_A, TRACK_B))
    return WORDS.fields("Labels", width_a=width_a, width_b=width_b)


def _tracks(lay):
    labels = _labels()
    lay.pencil("Track A", *TRACK_A, last_number=90)
    lay.sh.text(TRACK_A[0], TRACK_A[3] + 9.5, labels["track_a"], size=6.5, bold=True, color=MUTED)
    # Track B is for measuring only, so it isn't in the circuit.
    E.pencil_track(lay.sh, *TRACK_B)
    lay.sh.text(TRACK_B[0], TRACK_B[1] - 2, labels["track_b"], size=6.5, bold=True, color=MUTED)


def _lanes(lay):
    x_in = S.NET_STRIP_START_X
    lay.lane("V+", [(x_in, S.hole_y("H2")), (40, S.hole_y("H2")), (40, V_PLUS_Y), (TRACK_A[2] + 6, V_PLUS_Y)])
    lay.sh.text(TRACK_A[2] + 8, V_PLUS_Y + 1.2, "V+", size=6.5, bold=True, color=COPPER)
    lay.lane("N", [(R1_X, N_TOP), (R1_X, N_Y), (N_END, N_Y)])
    lay.lane("GND", [(x_in, S.hole_y("H3")), (GND_X, S.hole_y("H3")), (GND_X, N_Y - 6)])


def _parts(lay):
    lay.resistor("R1", R1_X, R1_CY, vertical=True, lead=22, label="value")
    lay.led("LED1", LED_X, N_Y, anode="left", lead_anode=13, lead_cathode=11)
    lay.wiper("Track A", *WIPER, WIPER_STRIP)


def _items(texts, numbered):
    return lesson.items(texts, numbered, space_after=1.0)


def _need(sh):
    need = WORDS.items("You need")
    h = style(8.5, bold=True, spaceAfter=1.2)
    first = [Paragraph("You need", h)] + _items(need[:3], numbered=False)
    second = _items(need[3:], numbered=False)
    heading_h = (h.leading + h.spaceAfter) / 72 * 25.4
    rest = sh.flow([(46.0, 27.0, 112.0, 46.0)], first) + sh.flow([(116.0, 27.0 + heading_h, 170.0, 46.0)], second)
    if rest:
        raise RuntimeError(f"L03 parts list overflowed by {len(rest)} items")


def _steps(sh, lay):
    steps = WORDS.items("Build it", lanes=number(lay.laid), wiper_strip=f"{WIPER_STRIP:g}")
    story = [Paragraph("Build it", style(8.5, bold=True, spaceAfter=1.5))] + _items(steps, numbered=True)
    story.append(lesson.tag_note(TAG_NOTE_WITH_T1))
    rest = sh.flow([(S.ZONE_BUILD[0], 113.0, 150.0, 184.0)], story)
    if rest:
        raise RuntimeError(f"L03 build steps overflowed by {len(rest)} items")


def _schematic(sh, lay):
    lesson.schematic_panel(sh)

    term_x, wiper_x, x = 44.0, 58.0, 66.0
    top, wiper_y, box = 214.0, 232.0, (222.0, 242.0)
    sch.terminal(sh, term_x, top, "", 0)
    sh.text(term_x - 2, top + 1.2, "V+", size=6.5, bold=True, align="right")
    sch.wire(sh, [(term_x + 0.8, top), (wiper_x, top), (wiper_x, wiper_y)])
    track = lay.symbol("Track A")
    sch.rheostat(sh, x, *box, wiper_y, wiper_x, track.ref, track.text)
    sh.text(wiper_x - 1.2, wiper_y - 2, _labels()["wiper"], size=6, color=MUTED, align="right")
    r1 = lay.symbol("R1")
    sch.resistor(sh, x, box[1], 258, r1.ref, r1.text)
    sch.led(sh, x, 258, 274, lay.symbol("LED1").ref)
    sch.terminal(sh, term_x, 274, "", 0)
    sh.text(term_x - 2, 275.2, "GND", size=6.5, bold=True, align="right")
    sch.wire(sh, [(term_x + 0.8, 274), (x, 274), (x, 273.99)])
    lesson.schematic_note(sh, WORDS.text("Schematic note"))


def _workbook(sh):
    boxes = lesson.workbook_boxes()
    tx = boxes[0][0] + 2

    _, py0, _, _ = boxes[0]
    predict = WORDS.fields("Predict")
    E.workbook_box(sh, boxes[0], "Predict", predict["prompt"])
    sh.runs(tx, py0 + 11, [(f"{predict['wiper']}  ", True), (predict["choices"], False)], size=7.5)
    sh.text(tx, py0 + 18.5, predict["why"], size=7, color=MUTED)

    _, my0, _, _ = boxes[1]
    E.workbook_box(sh, boxes[1], "Measure", WORDS.fields("Measure")["prompt"])
    col_x, pitch, box_w = tx + 18, 20.0, 13.0
    for j, mark in enumerate(MEASURE_MARKS):
        sh.text(col_x + j * pitch + box_w / 2, my0 + 9.5, f"{mark} mm", size=6.5, bold=True, color=MUTED, align="center")
    for i, row in enumerate(WORDS.items("Measure rows")):
        ry = my0 + 15 + i * 6
        sh.text(tx, ry, row, size=7, bold=True)
        for j in range(len(MEASURE_MARKS)):
            bx = col_x + j * pitch
            sh.rect(bx, ry - 3.6, bx + box_w, ry + 1.2, stroke=INK, width=0.25)
            sh.text(bx + box_w + 1, ry, "kΩ", size=6, color=MUTED)

    _, ey0, _, _ = boxes[2]
    explain = WORDS.fields("Explain")
    E.workbook_box(sh, boxes[2], "Explain", explain["prompt"])
    sh.text(tx, ey0 + 9, explain["question"], size=7)
    lesson.write_lines(sh, boxes[2], (15.5, 21.5))
