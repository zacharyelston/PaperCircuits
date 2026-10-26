"""T1 pencil contacts.

Can pencil make copper tape's glue conduct? Two tests, each with a control:
1. Tape overlaps: the upper piece's glue is scratched, rubbed with pencil, or both,
   against a plain overlap (the T0 J2 control) and a continuous reference lane. O6 puts
   two glue faces together, so current has to cross both.
2. Tape on pencil: copper joined to a shaded track by plain tape, treated glue, a folded
   copper tab, or L03's bare wire under clear tape.

Sheet 1 holds the fixtures and results: print on card, once per paper being compared.
Sheet 2 is the procedure: print once on plain paper.

The words are in t1_pencil_contacts.md. A section that prints its own heading is named
after it; a test row's words are "name · hint", keyed by its code.
"""

from reportlab.platypus import Paragraph

from .. import elements as E
from .. import standard as S
from .. import testsheet as ts
from ..draw import GUIDE, MUTED, Sheet, style
from ..words import Words

PAGE_ID = "T1"
WORDS = Words.beside(__file__)
LEFT, RIGHT = S.ZONE_BUILD[0], S.ZONE_BUILD[2]

# Each overlap row's code, and whether its lane is two pieces joined at J.
OVERLAPS = [("O0", False), ("O1", True), ("O2", True), ("O3", True), ("O4", True), ("O5", True),
            ("O6", True), ("O7", True)]
OVERLAP_A, OVERLAP_B, OVERLAP_J = 80.0, 152.0, 116.0

JOINS = ("K1", "K2", "K3", "K4", "K5")
TRACK = (96.0, 136.0)            # 40 mm of pencil between the two joins
TRACK_W = 10.0
JOIN_OVERLAP = 10.0
LANE_A, LANE_B = (74.0, TRACK[0] + JOIN_OVERLAP), (TRACK[1] - JOIN_OVERLAP, 158.0)
WIRE_LANE_A, WIRE_LANE_B = (74.0, 92.0), (140.0, 158.0)
PROBE_X = (LANE_A[1] + 2, LANE_B[0] - 2)


def build(path):
    sh = Sheet(path, WORDS.text("PDF title"))
    _fixtures(sh)
    sh.next_page()
    _procedure(sh)
    sh.save()


def _fixtures(sh):
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, part="1/2")
    E.spine(sh)
    _overlaps(sh)
    _joins(sh)
    sh.rect(LEFT, 237, RIGHT, 281, stroke=GUIDE, width=0.25, radius=1.2)
    sh.text(LEFT + 2, 241, WORDS.fields("Labels")["notes"], size=6.5, bold=True, color=MUTED)
    E.footer(sh, f"{PAGE_ID} {WORDS.fields('Sheet 1')['footer']}")


def _row_label(sh, y, code, text):
    name, hint = ts.row(text)
    sh.text(LEFT, y - 0.4, f"{code}  {name}", size=7, bold=True)
    if hint:
        sh.text(LEFT, y + 3.2, hint, size=6.5, color=MUTED)


def _overlaps(sh):
    words = WORDS.fields("Overlap fixtures")
    sh.text(LEFT, 30, words["title"], size=10, bold=True)
    sh.paragraph(LEFT, 32, 136, words["intro"], style(7, color=MUTED))
    sh.runs(LEFT, 43.5, [(words["zero"] + " ", True), ("_______ Ω", False), ("      " + words["built"] + " ", True),
                         ("______________", False)], size=7)
    sh.runs(LEFT, 48.5, [(words["paper"] + " ", True), ("_________________________", False)], size=7)
    ts.result_headers(sh, 48.5)
    for i, (code, joined) in enumerate(OVERLAPS):
        y = 55.0 + 11 * i
        E.lane(sh, [(OVERLAP_A - 2, y), (OVERLAP_B + 2, y)])
        if joined:
            E.joint(sh, OVERLAP_J, y)
        for x, end in ((OVERLAP_A, "A"), (OVERLAP_B, "B")):
            E.test_point(sh, x, y)
            sh.text(x, y - 4.6, end, size=6, color=MUTED, align="center")
        _row_label(sh, y, code, words[code])
        ts.result_boxes(sh, y)


def _joins(sh):
    words = WORDS.fields("Join fixtures")
    sh.text(LEFT, 144, words["title"], size=10, bold=True)
    sh.paragraph(LEFT, 146, 136, words["intro"], style(7, color=MUTED))
    ts.result_headers(sh, 157.5, WORDS.items("Join result columns"))
    for i, code in enumerate(JOINS):
        y = 165.0 + 15 * i
        E.pencil_track(sh, TRACK[0], y - TRACK_W / 2, TRACK[1], y + TRACK_W / 2, tick=None)
        if code == "K4":
            lanes = (WIRE_LANE_A, WIRE_LANE_B)
            for x0, x1 in ((WIRE_LANE_A[1] - 4, TRACK[0] + 8), (TRACK[1] - 8, WIRE_LANE_B[0] + 4)):
                sh.line(x0, y, x1, y, width=0.6, color=MUTED, cap=1)
        else:
            lanes = (LANE_A, LANE_B)
        for x0, x1 in lanes:
            E.lane(sh, [(x0, y), (x1, y)])
        for x in PROBE_X:
            sh.circle(x, y, 3.0, stroke=MUTED, width=0.3)
        for x, end in ((LANE_A[0] + 4, "A"), (LANE_B[1] - 4, "B")):
            E.test_point(sh, x, y)
            sh.text(x, y - 4.6, end, size=6, color=MUTED, align="center")
        _row_label(sh, y, code, words[code])
        ts.result_boxes(sh, y)


def _procedure(sh):
    sheet = WORDS.fields("Sheet 2")
    E.header(sh, PAGE_ID, sheet["title"], sheet["subtitle"], part="2/2")
    E.spine(sh)
    left = ts.section(WORDS, "You need", ts.bullets)
    left += ts.section(WORDS, "Before you start", ts.steps)
    left += ts.section(WORDS, "1 · Tape overlaps", ts.steps)

    right = ts.section(WORDS, "2 · Tape on pencil", ts.steps)
    right += ts.section(WORDS, "Pass or fail", ts.bullets)
    intro, *papers, note = WORDS.items("Trying different papers")
    left += [Paragraph("Trying different papers", ts.H), Paragraph(intro, style(7.5, leading=9.6))]
    left += ts.bullets(papers)
    left += [Paragraph(note, ts.NOTE)]
    right += ts.section(WORDS, "Results for standard v0.2",
                      lambda questions: [ts.decision_table(questions, widths=(38, 42))])

    rest = sh.flow([(LEFT, 27.0, 115.0, 282.0)], left) + sh.flow([(121.0, 27.0, RIGHT, 282.0)], right)
    if rest:
        raise RuntimeError(f"T1 sheet 2 overflowed by {len(rest)} items")
    E.footer(sh, f"{PAGE_ID} {sheet['footer']}")
