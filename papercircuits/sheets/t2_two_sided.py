"""T2 two-sided tests.

Does a second copper layer on the back of the page work? Four tests:
1. Registration: pins through four front crosshairs show, on 1 mm scales behind them, how
   far double-sided printing shifts the back.
2. Vias: lanes run from A on the front, through to the back and up again to B, by slit,
   wire, eyelet and your own method, against a front-only reference.
3. Edge wraps: 12 mm tape folded over the top edge, measured front to back, joining two
   pages side by side, and through a clipped stack.
4. Stacking shorts: one sheet's back pad, joined to its front by a via, lies on the next
   sheet's front pad. Does it short, and does an interleaf stop it?

Pages 1 and 2 print on the two sides of one card (page 2 is mirrored, so every mark lands
behind its partner when the sheet is flipped on its long edge). Page 3 is the procedure
and results.

The words are in t2_two_sided.md. A section that prints its own heading is named after
it; a test row's words are "name · hint", keyed by its code.
"""

from reportlab.platypus import Paragraph

from .. import elements as E
from .. import standard as S
from .. import testsheet as ts
from ..draw import MUTED, Sheet, style
from ..words import Words

PAGE_ID = "T2"
WORDS = Words.beside(__file__)

REG_MARKS = (("R1", 44.0, 34.0), ("R2", 186.0, 34.0), ("R3", 44.0, 272.0), ("R4", 186.0, 272.0))

# Each via row's code and how its vias are made; the reference has none.
VIAS = [("V0", None), ("V1", "slit"), ("V2", "wire"), ("V3", "eyelet"), ("V4", "mark")]
VIA_Y0, VIA_PITCH = 60.0, 12.0
VIA_A, VIA_B = 80.0, 164.0
VIA_X = (104.0, 140.0)
VIA_OVERLAP = 4.0  # how far a lane runs past a wire or eyelet via, on each side

WRAP_LINE_Y = 6.0
SHORT_Y = 182.0
FRONT_PAD = (105.0, 200.0)
BACK_PAD_TURN_X = 128.0
SHORT_VIA = (BACK_PAD_TURN_X, 204.0)
TP_X = 196.0


def build(path):
    sh = Sheet(path, WORDS.text("PDF title"))
    _front(sh)
    sh.next_page(mirrored=True)
    _back(sh)
    sh.next_page()
    _procedure(sh)
    sh.save()


def _wrap_guide(sh):
    sh.line(3, WRAP_LINE_Y, S.PAGE_W - 3, WRAP_LINE_Y, width=0.25, color=MUTED, dash=(1.5, 1))
    sh.text(4, WRAP_LINE_Y + 4, WORDS.fields("Labels")["wrap"], size=6, color=MUTED)


def _via_lanes(sh, y, kind, face):
    """The front's two pieces, or the back's one, for a row whose vias are `kind`."""
    reach = 0.0 if kind == "slit" else VIA_OVERLAP
    a, b = VIA_X
    if face == "front":
        E.lane(sh, [(VIA_A - 4, y), (a + reach, y)])
        E.lane(sh, [(b - reach, y), (VIA_B + 4, y)])
    else:
        E.lane(sh, [(a - reach, y), (b + reach, y)])
    for x in VIA_X:
        E.via(sh, x, y, kind)


def _front(sh):
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, part="1/3")
    E.spine(sh)
    _wrap_guide(sh)
    for label, x, y in REG_MARKS:
        E.registration_mark(sh, x, y, label)

    vias = WORDS.fields("Via fixtures")
    sh.text(34, 50, vias["title"], size=10, bold=True)
    for i, (code, kind) in enumerate(VIAS):
        name, hint = ts.row(vias[code])
        y = VIA_Y0 + VIA_PITCH * i
        if kind is None:
            E.lane(sh, [(VIA_A - 4, y), (VIA_B + 4, y)])
        else:
            _via_lanes(sh, y, kind, "front")
        for x, end in ((VIA_A, "A"), (VIA_B, "B")):
            E.test_point(sh, x, y)
            sh.text(x, y - 4.6, end, size=6, color=MUTED, align="center")
        sh.text(34, y - 0.4, f"{code}  {name}", size=7, bold=True)
        if hint:
            sh.text(34, y + 3.2, hint, size=6.5, color=MUTED)

    front = WORDS.fields("Front fixtures")
    for y, test in ((126, "registration"), (142, "wraps")):
        sh.text(34, y, front[test], size=10, bold=True)
        sh.text(34, y + 5, front[test + "_hint"], size=7, color=MUTED)

    sh.text(34, 166, front["shorts"], size=10, bold=True)
    sh.paragraph(34, 168, 66, front["shorts_hint"], style(6.5, leading=8, color=MUTED))
    E.lane(sh, [(FRONT_PAD[0], SHORT_Y), (FRONT_PAD[1], SHORT_Y)], width=S.WIDE_TAPE_W)
    E.lane(sh, [SHORT_VIA, (FRONT_PAD[1], SHORT_VIA[1])])
    E.via(sh, *SHORT_VIA, "wire")
    E.test_point(sh, TP_X, SHORT_Y, "S2", side="left")
    E.test_point(sh, TP_X, SHORT_VIA[1], "S1", side="left")
    sh.text(FRONT_PAD[0], SHORT_Y - S.WIDE_TAPE_W / 2 - 1.5, front["pad"], size=6, color=MUTED)
    E.footer(sh, f"{PAGE_ID} {WORDS.fields('Sheet 1')['footer']}")


def _back(sh):
    sheet = WORDS.fields("Sheet 2")
    with sh.unmirrored():
        E.header(sh, PAGE_ID, sheet["title"], sheet["subtitle"], part="2/3")
    E.spine(sh)
    _wrap_guide(sh)
    for label, x, y in REG_MARKS:
        E.registration_mark(sh, x, y, label, scale=True)
    for i, (code, kind) in enumerate(VIAS):
        if kind is None:
            continue
        y = VIA_Y0 + VIA_PITCH * i
        _via_lanes(sh, y, kind, "back")
        sh.text(VIA_X[0] - VIA_OVERLAP - 3, y + 1.1, code, size=6.5, bold=True, align="right")
    E.lane(sh, [(FRONT_PAD[0], SHORT_Y), (BACK_PAD_TURN_X, SHORT_Y), SHORT_VIA], width=S.WIDE_TAPE_W)
    E.via(sh, *SHORT_VIA, "wire")
    sh.text(FRONT_PAD[0], SHORT_Y - S.WIDE_TAPE_W / 2 - 1.5, sheet["pad"], size=6, color=MUTED)
    with sh.unmirrored():
        E.footer(sh, f"{PAGE_ID} {sheet['footer']}")


def _procedure(sh):
    sheet = WORDS.fields("Sheet 3")
    E.header(sh, PAGE_ID, sheet["title"], sheet["subtitle"], part="3/3")
    E.spine(sh)
    h, note = ts.H, ts.NOTE
    left = ts.section(WORDS, "You need", ts.bullets)
    *reg_steps, reg_note = WORDS.items("1 · Registration", via_overlap=f"{VIA_OVERLAP:g}")
    left += [Paragraph("1 · Registration", h)] + ts.steps(reg_steps)
    left += [ts.table([[""] + WORDS.items("Registration table")] + [[m[0], "", ""] for m in REG_MARKS],
                      [20, 30, 30], 6.5)]
    left += [Paragraph(reg_note, note)]
    left += ts.section(WORDS, "2 · Vias", ts.steps)
    left += [ts.table([[""] + WORDS.items("Via table")] + [[v[0], "", "", ""] for v in VIAS], [20, 20, 20, 20], 6.5)]

    right = ts.section(WORDS, "3 · Edge wraps", ts.steps)
    right += [ts.table([[r, ""] for r in WORDS.items("Edge wrap table")], [50, 30], 6.5)]
    right += ts.section(WORDS, "4 · Stacking shorts", ts.steps)
    right += [ts.table([[r, ""] for r in WORDS.items("Stacking table")], [50, 30], 6.5)]
    right += ts.section(WORDS, "Pass or fail", ts.bullets)
    right += ts.section(WORDS, "Results for the standard",
                      lambda questions: [ts.decision_table(questions, widths=(38, 42), row_height=7.5)])
    rest = sh.flow([(S.ZONE_BUILD[0], 27.0, 115.0, 282.0)], left) + sh.flow([(121.0, 27.0, S.ZONE_BUILD[2], 282.0)], right)
    if rest:
        raise RuntimeError(f"T2 sheet 3 overflowed by {len(rest)} items")
    E.footer(sh, f"{PAGE_ID} {sheet['footer']}")
