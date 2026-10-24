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
"""

from reportlab.platypus import Paragraph

from .. import elements as E
from .. import standard as S
from .. import testsheet as ts
from ..draw import MUTED, Sheet, style

PAGE_ID = "T2"

REG_MARKS = (("R1", 44.0, 34.0), ("R2", 186.0, 34.0), ("R3", 44.0, 272.0), ("R4", 186.0, 272.0))

VIAS = [
    ("V0", "Front only", "the reference", None),
    ("V1", "Slit vias", "tape threads through", "slit"),
    ("V2", "Wire vias", "leg through, soldered", "wire"),
    ("V3", "Eyelet vias", "eyelet through both", "eyelet"),
    ("V4", "Your version", "", "mark"),
]
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
    sh = Sheet(path, "T2 two-sided tests")
    _front(sh)
    sh.next_page(mirrored=True)
    _back(sh)
    sh.next_page()
    _procedure(sh)
    sh.save()


def _wrap_guide(sh):
    sh.line(3, WRAP_LINE_Y, S.PAGE_W - 3, WRAP_LINE_Y, width=0.25, color=MUTED, dash=(1.5, 1))
    sh.text(4, WRAP_LINE_Y + 4, "edge wrap", size=6, color=MUTED)


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
    E.header(sh, PAGE_ID, "T2  Two-sided tests",
             "Print pages 1 and 2 on the two sides of one card, flipping on the long edge.", part="1/3")
    E.spine(sh)
    _wrap_guide(sh)
    for label, x, y in REG_MARKS:
        E.registration_mark(sh, x, y, label)

    sh.text(34, 50, "2  Vias", size=10, bold=True)
    for i, (code, name, hint, kind) in enumerate(VIAS):
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

    for y, title, text in ((126, "1  Registration", "Push a pin through each corner mark, R1 to R4, and read the offset on the back."),
                           (142, "3  Edge wraps", "Fold 12 mm tape over the top edge, down to the dashed line on both sides.")):
        sh.text(34, y, title, size=10, bold=True)
        sh.text(34, y + 5, text, size=7, color=MUTED)

    sh.text(34, 166, "4  Stacking shorts", size=10, bold=True)
    sh.paragraph(34, 168, 66, "The 12 mm front pad ends at S2. Behind it, a back pad joins S1 through a "
                 "wire via. Sheet 3 says how to stack two sheets.", style(6.5, leading=8, color=MUTED))
    E.lane(sh, [(FRONT_PAD[0], SHORT_Y), (FRONT_PAD[1], SHORT_Y)], width=S.WIDE_TAPE_W)
    E.lane(sh, [SHORT_VIA, (FRONT_PAD[1], SHORT_VIA[1])])
    E.via(sh, *SHORT_VIA, "wire")
    E.test_point(sh, TP_X, SHORT_Y, "S2", side="left")
    E.test_point(sh, TP_X, SHORT_VIA[1], "S1", side="left")
    sh.text(FRONT_PAD[0], SHORT_Y - S.WIDE_TAPE_W / 2 - 1.5, "front pad, 12 mm tape", size=6, color=MUTED)
    E.footer(sh, f"{PAGE_ID} sheet 1 of 3 (front)")


def _back(sh):
    with sh.unmirrored():
        E.header(sh, PAGE_ID, "T2  Two-sided tests: back",
                 "This side prints on the back of page 1. Each mark should sit behind its partner.",
                 part="2/3")
    E.spine(sh)
    _wrap_guide(sh)
    for label, x, y in REG_MARKS:
        E.registration_mark(sh, x, y, label, scale=True)
    for i, (code, _, _, kind) in enumerate(VIAS):
        if kind is None:
            continue
        y = VIA_Y0 + VIA_PITCH * i
        _via_lanes(sh, y, kind, "back")
        sh.text(VIA_X[0] - VIA_OVERLAP - 3, y + 1.1, code, size=6.5, bold=True, align="right")
    E.lane(sh, [(FRONT_PAD[0], SHORT_Y), (BACK_PAD_TURN_X, SHORT_Y), SHORT_VIA], width=S.WIDE_TAPE_W)
    E.via(sh, *SHORT_VIA, "wire")
    sh.text(FRONT_PAD[0], SHORT_Y - S.WIDE_TAPE_W / 2 - 1.5, "back pad, 12 mm tape", size=6, color=MUTED)
    with sh.unmirrored():
        E.footer(sh, f"{PAGE_ID} sheet 2 of 3 (back of sheet 1)")


def _procedure(sh):
    E.header(sh, PAGE_ID, "T2  Running the two-sided tests",
             "Print this sheet once on plain paper. Print pages 1 and 2 double-sided on card, four copies.",
             part="3/3")
    E.spine(sh)
    h, note = ts.H, ts.NOTE
    left = [Paragraph("You need", h)] + ts.bullets([
        "Four cards printed double-sided (pages 1 and 2)",
        "5 mm and 12 mm copper tape, a craft knife and a pin",
        "Cut-off resistor legs and solder; small eyelets, about 3 mm",
        "A binder clip, a sheet of plain paper and one of vellum",
        "A multimeter with a 200 Ω range",
    ])
    left += [Paragraph("1 · Registration", h)] + ts.steps([
        "Check the 100 mm bar on both sides of one card.",
        "Push a pin straight through the centre of each front mark, R1 to R4.",
        "On the back, read where each hole landed on the 1 mm scale, across and up or down.",
    ])
    left += [ts.table([["", "Across", "Up / down"]] + [[m[0], "", ""] for m in REG_MARKS], [20, 30, 30], 6.5)]
    left += [Paragraph("Pass: within 1.5 mm everywhere. Lanes overlap 4 mm at wire and eyelet vias.", note)]
    left += [Paragraph("2 · Vias", h)] + ts.steps([
        "<b>V1:</b> cut the two slits. Lay one piece of tape from A, through the first slit, along the back "
        "and up through the second slit, to B.",
        "<b>V2:</b> lay the three pieces. Push a resistor leg through each via mark, bend it flat on both "
        "sides and solder it.",
        "<b>V3:</b> lay the three pieces, pierce a small hole through both at each eyelet mark, and set an eyelet.",
        "Measure A to B. <b>Flexed</b> and <b>Day 7</b> work as on T0.",
    ])
    left += [ts.table([["", "Day 0", "Flexed", "Day 7"]] + [[v[0], "", "", ""] for v in VIAS], [20, 20, 20, 20], 6.5)]

    right = [Paragraph("3 · Edge wraps", h)] + ts.steps([
        "Lay 12 mm tape along the top edge so half overhangs, fold it onto the back down to the dashed line, "
        "and burnish it.",
        "<b>One sheet:</b> measure from the front wrap to the back wrap.",
        "<b>Side join:</b> overlap two sheets' top corners by 10 mm, wrap on wrap. Measure from one to the "
        "other, with and without a binder clip.",
        "<b>Stack:</b> stack three sheets, top edges level, and clip along the edge. Measure from the top "
        "sheet's front wrap to the bottom sheet's back wrap, then again while turning the pages.",
    ])
    right += [ts.table([[r, ""] for r in ("One sheet, front to back", "Side join, clipped", "Side join, no clip",
                                          "Stack, clipped", "Stack, turning pages")], [50, 30], 6.5)]
    right += [Paragraph("4 · Stacking shorts", h)] + ts.steps([
        "On two sheets, lay the front pad and the S1 lane, the back pad on the back, and the wire via.",
        "Lay sheet A on sheet B, shifted 15 mm to the left so B's S2 shows. A's back pad now lies on B's front pad.",
        "Measure from A's S1 to B's S2, as listed below.",
    ])
    right += [ts.table([[r, ""] for r in ("No interleaf", "Pressing hard", "Plain paper between",
                                          "Vellum between")], [50, 30], 6.5)]
    right += [Paragraph("Pass or fail", h)] + ts.bullets([
        "<b>Vias and wraps:</b> within 1 Ω of V0 and steady; flicker or OL fails.",
        "<b>Shorts:</b> any reading without an interleaf means stacked two-sided pages need one. "
        "With an interleaf it must read OL.",
    ])
    right += [Paragraph("Results for the standard", h),
              ts.decision_table(["Duplex within 1.5 mm?", "Best via", "Edge rails reliable?", "Interleaf needed?"],
                                widths=(38, 42), row_height=7.5)]
    rest = sh.flow([(S.ZONE_BUILD[0], 27.0, 115.0, 282.0)], left) + sh.flow([(121.0, 27.0, S.ZONE_BUILD[2], 282.0)], right)
    if rest:
        raise RuntimeError(f"T2 sheet 3 overflowed by {len(rest)} items")
    E.footer(sh, f"{PAGE_ID} sheet 3 of 3")
