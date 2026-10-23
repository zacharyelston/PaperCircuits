"""T0 contact tests.

Sheet 1 holds the fixtures: print three copies on card, because test 3 needs a stack.
Sheet 2 is the procedure and the binder results: print one on plain paper.
"""

from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from .. import elements as E
from .. import standard as S
from ..draw import COPPER, FONT, FONT_BOLD, GUIDE, INK, MUTED, Sheet, style

PAGE_ID = "T0"
LEFT, RIGHT = 62.0, 202.0  # tests 1 and 2 sit right of the hole treatments

HOLE_TREATMENTS = {
    "H1": ("Bare hole", "tape only, no eyelet", S.TAPE_W),
    "H2": ("Eyelet", "clamps the 5 mm strip", S.TAPE_W),
    "H3": ("Eyelet", "on 12 mm tape", S.WIDE_TAPE_W),
    "H4": ("Eyelet", "soldered to the strip", S.TAPE_W),
}

TAPE_JOINTS = [
    ("J1", "Continuous", "the reference", "straight"),
    ("J2", "Overlap", "cut, overlap 10 mm", "joint"),
    ("J3", "Overlap + solder", "solder across it", "joint"),
    ("J4", "Folded corners", "fold, don't cut", "folded"),
    ("J5", "Cut corners", "cut + overlap at each", "cut"),
    ("J6", "Your tape", "e.g. conductive glue", "joint"),
]

PART_JOINTS = [
    ("M1", "Flat leads", "clear tape over"),
    ("M2", "Flat leads", "copper patch over"),
    ("M3", "Spiral leads", "copper patch over"),
    ("M4", "Soldered", ""),
    ("M5", "Your method", ""),
]

RESULT_X = (167.0, 181.0, 195.0)


def build(path):
    sh = Sheet(path, "T0 contact tests")
    _fixtures(sh)
    sh.next_page()
    _procedure(sh)
    sh.save()


def _fixtures(sh):
    E.header(
        sh, PAGE_ID, "T0  Contact tests",
        "Which joints, part contacts and binder contacts stay reliable? Build on 160–200 gsm card.",
        part="1/2",
    )
    _hole_tests(sh)
    _tape_joints(sh)
    _part_joints(sh)
    sh.rect(LEFT, 264, RIGHT, 281, stroke=GUIDE, width=0.25, radius=1.2)
    sh.text(LEFT + 2, 268, "Notes", size=6.5, bold=True, color=MUTED)
    E.footer(sh, f"{PAGE_ID} sheet 1 of 2")


def _hole_tests(sh):
    """Test 3 fixtures: one treatment per hole, each with a test point to probe against the post."""
    for hole_id, (name, how, width) in HOLE_TREATMENTS.items():
        y = S.hole_y(hole_id)
        E.lane(sh, [(S.NET_STRIP_START_X, y), (46, y)], width=width)
        E.test_point(sh, 44, y, f"TP-{hole_id}")
        sh.runs(S.NET_STRIP_START_X, y + width / 2 + 4.5, [(name, True), (" · " + how, False)], size=6.5)
    E.spine(sh, connected=HOLE_TREATMENTS, strip_widths={h: w for h, (_, _, w) in HOLE_TREATMENTS.items()})


def _result_headers(sh, y):
    for x, name in zip(RESULT_X, ("Day 0", "Flexed", "Day 7")):
        sh.text(x, y, name, size=6.5, bold=True, align="center")


def _result_boxes(sh, y):
    for x in RESULT_X:
        sh.rect(x - 6, y - 3, x + 6, y + 3, stroke=INK, width=0.25)


def _tape_joints(sh):
    sh.text(LEFT, 30, "1  Tape joints", size=10, bold=True)
    sh.paragraph(
        LEFT, 32, RIGHT - LEFT,
        "Lay each lane from pad A to pad B as marked, then measure A to B in ohms and subtract the "
        "meter zero. Write OL for an open circuit. Sheet 2 explains Flexed and Day 7.",
        style(7, color=MUTED),
    )
    sh.runs(LEFT, 44, [("Meter zero ", True), ("_______ Ω", False), ("      Built on ", True), ("______________", False)], size=7)
    _result_headers(sh, 44)

    x_a, x_b, x_bend = 102.0, 154.0, 126.0
    y = 51.0
    for jid, name, hint, shape in TAPE_JOINTS:
        y_end = y + 11 if shape in ("folded", "cut") else y
        if y_end != y:
            pts = [(x_a - 2, y), (x_bend, y), (x_bend, y_end), (x_b + 2, y_end)]
        else:
            pts = [(x_a - 2, y), (x_b + 2, y)]
        E.lane(sh, pts, folds=shape == "folded")
        if shape == "joint":
            E.joint(sh, (x_a + x_b) / 2, y)
        elif shape == "cut":
            E.corner_joint(sh, x_bend, y)
            E.corner_joint(sh, x_bend, y_end)
            sh.text(x_bend + 4, y + 1, "J", size=6.5, bold=True)
            sh.text(x_bend - 4, y_end + 1, "J", size=6.5, bold=True, align="right")
        E.test_point(sh, x_a, y)
        E.test_point(sh, x_b, y_end)
        sh.text(x_a, y - 4.6, "A", size=6, color=MUTED, align="center")
        sh.text(x_b, y_end - 4.6, "B", size=6, color=MUTED, align="center")
        sh.text(LEFT, y - 0.4, f"{jid}  {name}", size=7, bold=True)
        sh.text(LEFT, y + 3.2, hint, size=6.5, color=MUTED)
        _result_boxes(sh, (y + y_end) / 2)
        y = y_end + 11


def _part_joints(sh):
    sh.text(LEFT, 140, "2  Part joints", size=10, bold=True)
    sh.paragraph(
        LEFT, 142, RIGHT - LEFT,
        "Bridge each gap with a 10 Ω resistor, leads flat on the tape, attached as labelled. "
        "Measure A to B. Contact resistance is the reading minus R alone.",
        style(7, color=MUTED),
    )
    sh.runs(LEFT, 154, [("R alone ", True), ("_______ Ω", False), ("   one resistor, probes on its leads", False)], size=7)

    col_w, top, gap0, gap1, bottom = 25.0, 172.0, 197.0, 207.0, 232.0
    mid = (gap0 + gap1) / 2
    rows = (("Day 0", 239.0), ("Flexed", 245.0), ("Day 7", 251.0), ("Flicker?", 257.0))
    for label, ry in rows:
        sh.text(LEFT, ry + 1.1, label, size=6.5, bold=True)
    for i, (mid_id, name, how) in enumerate(PART_JOINTS):
        x0 = 77.0 + i * col_w
        cx = x0 + col_w / 2
        sh.text(cx, 160.5, mid_id, size=7.5, bold=True, align="center")
        sh.text(cx, 164.3, name, size=6.5, align="center")
        if how:
            sh.text(cx, 167.6, how, size=6.5, color=MUTED, align="center")
        E.lane(sh, [(cx, top), (cx, gap0)])
        E.lane(sh, [(cx, gap1), (cx, bottom)])
        _attachment_cue(sh, mid_id, cx, mid)
        E.resistor(sh, cx, mid, vertical=True, lead=10 if mid_id == "M3" else 12, label="10 Ω")
        if mid_id == "M3":
            E.spiral(sh, cx, mid - 11)
            E.spiral(sh, cx, mid + 11)
        E.test_point(sh, cx, top + 2.5)
        E.test_point(sh, cx, bottom - 2.5)
        sh.text(cx - 4.7, top + 3.6, "A", size=6, color=MUTED, align="right")
        sh.text(cx - 4.7, bottom - 1.4, "B", size=6, color=MUTED, align="right")
        for _, ry in rows:
            sh.rect(x0 + 2.5, ry - 2.5, x0 + col_w - 2.5, ry + 2.5, stroke=INK, width=0.25)


def _attachment_cue(sh, method, cx, mid):
    """Where the tape patch or solder goes for each attachment method."""
    patches = ((mid - 14.5, mid - 4), (mid + 4, mid + 14.5))
    if method == "M1":
        for y0, y1 in patches:
            sh.rect(cx - 5, y0, cx + 5, y1, stroke=MUTED, width=0.25, dash=(0.6, 0.6))
    elif method in ("M2", "M3"):
        for y0, y1 in patches:
            sh.rect(cx - 5, y0, cx + 5, y1, stroke=COPPER, width=0.3, dash=(0.6, 0.6))
    elif method == "M4":
        for y in (mid - 9, mid + 9):
            sh.circle(cx, y, 1.8, stroke=None, fill=MUTED)


def _procedure(sh):
    E.header(
        sh, PAGE_ID, "T0  Running the contact tests",
        "Print this sheet once on plain paper. Print sheet 1 on 160–200 gsm card, three copies.",
        part="2/2",
    )
    E.spine(sh)

    h = style(9, bold=True, spaceBefore=5, spaceAfter=2)
    note = style(7, leading=9.2, color=MUTED, spaceBefore=2)

    def bullets(items):
        return [Paragraph(t, style(7.5, leading=9.6, leftIndent=7, bulletIndent=0.5, bulletFontSize=7.5, spaceAfter=1.2), bulletText="•") for t in items]

    def steps(items):
        return [Paragraph(t, style(7.5, leading=9.6, leftIndent=9, bulletIndent=0, bulletFontName=FONT_BOLD, bulletFontSize=7.5, spaceAfter=1.5), bulletText=f"{i}.") for i, t in enumerate(items, 1)]

    story = [Paragraph("You need", h)]
    story += bullets([
        "5 mm copper tape, plus about 15 cm of 12 mm tape for H3",
        "Five 10 Ω resistors per sheet (brown-black-black)",
        "Plain brass eyelets for a 6 mm hole, and a setting tool. Not painted aluminium.",
        "A 2- or 4-hole punch with 80 mm pitch",
        "A ring binder, and four brass Chicago screws (binding posts) long enough for three sheets",
        "A multimeter with a 200 Ω range",
        "A soldering iron for J3, M4 and H4; clear tape",
    ])
    story += [Paragraph("Before you start", h)]
    story += steps([
        "Print sheet 1 at 100 %. Check the footer bar measures 100 mm with a ruler.",
        "Lay the four hole lanes (test 3) first, then punch through the crosshairs, through the tape.",
        "Set eyelets in H2, H3 and H4. Leave H1 bare. Solder H4's eyelet to its strip.",
        "Zero the meter: 200 Ω range, probes touching. Write the reading on sheet 1 and subtract it from every reading.",
    ])
    story += [Paragraph("1 · Tape joints", h)]
    story += steps([
        "Lay each lane as one piece of 5 mm tape, except at the marks: J means cut and overlap the two pieces by 10 mm.",
        "J3: solder across the overlap. J4: turn each corner by folding along the printed crease. J5: cut at each corner and overlap.",
        "Measure from pad A to pad B. Write OL if the meter shows an open circuit.",
        "<b>Flexed:</b> bend the card gently over a table edge 10 times, rub each joint firmly with a thumb 5 times, then measure again.",
        "<b>Day 7:</b> leave the sheet in the binder for a week, then measure again.",
    ])
    story += [Paragraph("2 · Part joints", h)]
    story += steps([
        "Measure one resistor on its own and write it as R alone.",
        "Bridge each station's gap with a resistor, leads flat on the tape. M1: clear tape over flat leads. "
        "M2: a copper tape patch over flat leads. M3: coil each lead into a flat spiral, then a copper patch. "
        "M4: solder each lead. M5: your own idea.",
        "Measure A to B. Contact resistance is the reading minus R alone.",
        "<b>Flicker:</b> press on the part while watching the meter. Write Y if the reading jumps.",
        "Repeat after flexing and on day 7.",
    ])
    story += [Paragraph("10 Ω is low on purpose: a contact of a few ohms shows up clearly against it.", note)]

    left_story, story = story, [Paragraph("3 · Binder contacts", h)]
    story += steps([
        "Build the hole treatments on all three copies, as labelled on sheet 1.",
        "Bind the three sheets on rings. On each sheet, measure from TP-H<i>n</i> to the bare metal of ring <i>n</i>. "
        "Write the worst of the three readings below.",
        "<b>Turning:</b> keep the probes on and turn the other sheets back and forth 5 times. Write the highest reading, or OL.",
        "Repeat with Chicago screws, finger-tight.",
    ])
    story += [Spacer(1, 2 * mm), _binder_table()]

    story += [Paragraph("Pass or fail", h)]
    story += bullets([
        "<b>Pass:</b> within 1 Ω of the reference (J1, R alone, or 0 Ω for test 3) and no flicker.",
        "<b>Fail:</b> OL, any flicker, or a reading that drifts by day 7.",
    ])
    story += [Paragraph(
        "Why 1 Ω: lesson circuits use resistors of 100 Ω and up, so 1 Ω changes the current by 1 % or less. "
        "Flicker matters more than the exact value.", note)]
    story += [Paragraph("Results for standard v0.2", h), _decision_table()]

    left = (S.ZONE_BUILD[0], 27.0, 115.0, 282.0)
    right = (121.0, 27.0, S.ZONE_BUILD[2], 282.0)
    rest = sh.flow([left], left_story) + sh.flow([right], story)
    if rest:
        raise RuntimeError(f"T0 sheet 2 overflowed by {len(rest)} items")
    E.footer(sh, f"{PAGE_ID} sheet 2 of 2")


def _table(data, col_widths, row_height):
    t = Table(data, colWidths=[w * mm for w in col_widths], rowHeights=row_height * mm)
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), FONT, 7),
        ("FONT", (0, 0), (0, -1), FONT_BOLD, 7),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("GRID", (0, 0), (-1, -1), 0.6, GUIDE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def _binder_table():
    head = style(6.5, leading=7.5, bold=True)
    short = {"H1": "bare", "H2": "eyelet", "H3": "12 mm", "H4": "solder"}
    data = [[""] + [Paragraph(f"{h}<br/>{short[h]}", head) for h in HOLE_TREATMENTS]]
    for row in ("Rings, still", "Rings, turning", "Screws, still", "Screws, turning"):
        data.append([row, "", "", "", ""])
    return _table(data, [24, 14, 14, 14, 14], 7.5)


def _decision_table():
    rows = ["Tape overlaps OK?", "Lead attachment", "Hole treatment", "Binding"]
    return _table([[r, ""] for r in rows], [33, 47], 8.5)
