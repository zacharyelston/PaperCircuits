"""T0 contact tests.

Sheet 1 holds the fixtures: print three copies on card, because test 3 needs a stack.
Sheet 2 is the procedure and the binder results: print one on plain paper.
Sheet 3 is test 4, switch contacts, with its own steps and results: print one on card.
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

# Test 4: the corner switch, then three tab switches that differ only in the pair's gap.
SWITCH_TABS = [
    ("TA", "2 mm gap, the standard", S.SWITCH_PAD_GAP),
    ("TB", "3 mm gap", 3.0),
    ("TC", "your version", S.SWITCH_PAD_GAP),
]
TAB_X = (60.0, 108.0, 156.0)
TAB_UPPER = 80.0
SWITCH_ROWS = ("S1 corner", "TA 2 mm", "TB 3 mm", "TC yours")
SWITCH_COLS = (("Open", "OL?"), ("Light press", "Ω"), ("Firm press", "Ω"),
               ("Flicker?", "Y / N"), ("After 20", "Ω"), ("Day 7", "Ω"))

H = style(9, bold=True, spaceBefore=5, spaceAfter=2)
NOTE = style(7, leading=9.2, color=MUTED, spaceBefore=2)


def _bullets(items):
    return [Paragraph(t, style(7.5, leading=9.6, leftIndent=7, bulletIndent=0.5, bulletFontSize=7.5, spaceAfter=1.2), bulletText="•") for t in items]


def _steps(items):
    return [Paragraph(t, style(7.5, leading=9.6, leftIndent=9, bulletIndent=0, bulletFontName=FONT_BOLD, bulletFontSize=7.5, spaceAfter=1.5), bulletText=f"{i}.") for i, t in enumerate(items, 1)]


def build(path):
    sh = Sheet(path, "T0 contact tests")
    _fixtures(sh)
    sh.next_page()
    _procedure(sh)
    sh.next_page()
    _switch_tests(sh)
    sh.save()


def _fixtures(sh):
    E.header(
        sh, PAGE_ID, "T0  Contact tests",
        "Which joints, part contacts and binder contacts stay reliable? Build on 160–200 gsm card.",
        part="1/3",
    )
    _hole_tests(sh)
    _tape_joints(sh)
    _part_joints(sh)
    sh.rect(LEFT, 264, RIGHT, 281, stroke=GUIDE, width=0.25, radius=1.2)
    sh.text(LEFT + 2, 268, "Notes", size=6.5, bold=True, color=MUTED)
    E.footer(sh, f"{PAGE_ID} sheet 1 of 3")


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
        "Print this sheet once on plain paper. Print sheet 1 on card three times and sheet 3 once.",
        part="2/3",
    )
    E.spine(sh)
    h, note, bullets, steps = H, NOTE, _bullets, _steps

    story = [Paragraph("You need", h)]
    story += bullets([
        "5 mm copper tape, plus about 15 cm of 12 mm tape for H3",
        "Five 10 Ω resistors per sheet (brown-black-black)",
        "Plain brass eyelets for a 6 mm hole, and a setting tool. Not painted aluminium.",
        "A 2- or 4-hole punch with 80 mm pitch",
        "A ring binder, and four brass Chicago screws (binding posts) long enough for three sheets",
        "A multimeter with a 200 Ω range",
        "A soldering iron for J3, M4 and H4; clear tape; scissors for sheet 3",
    ])
    story += [Paragraph("Before you start", h)]
    story += steps([
        "Print sheets 1 and 3 at 100 % on 160–200 gsm card. Check a footer bar measures 100 mm with a ruler.",
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
    story += [Paragraph("4 · Switch contacts", h),
              Paragraph("Build, test and record the switches on sheet 3; its steps and pass rule are there.",
                        style(7.5, leading=9.6))]

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
    E.footer(sh, f"{PAGE_ID} sheet 2 of 3")


def _table(data, col_widths, row_height):
    t = Table(data, colWidths=[w * mm for w in col_widths], rowHeights=row_height * mm, hAlign="LEFT")
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
    rows = ["Tape overlaps OK?", "Lead attachment", "Hole treatment", "Binding", "Switch gap", "Corner switch OK?"]
    return _table([[r, ""] for r in rows], [33, 47], 8.5)


def _switch_tests(sh):
    E.header(
        sh, PAGE_ID, "T0  Switch contacts",
        "Do fold switches close every time, and does the gap stay open? Build on 160–200 gsm card.",
        part="3/3",
    )
    E.spine(sh)
    x0, _, x1, _ = S.ZONE_BUILD
    sh.text(x0, 31, "4  Switch contacts", size=10, bold=True)
    sh.paragraph(x0, 33, 106, "Each switch joins lane A to lane B while its flap is pressed. "
                 "Measure A to B with the meter on its 200 Ω range.", style(7, color=MUTED))
    _corner_switch_test(sh)
    for (tab_id, desc, gap), x in zip(SWITCH_TABS, TAB_X):
        _tab_station(sh, x, TAB_UPPER, tab_id, desc, gap)

    rest = sh.flow([(x0, 104.0, x1, 146.0)], [_switch_table()])
    story = [Paragraph("How to test", H)] + _steps([
        "Lay each switch's A and B lanes as separate pieces of tape. Keep the gap between them clear.",
        "S1: stick a 10 mm piece of tape on the corner flap where shown. Tabs: cut the solid lines, "
        "crease the dotted hinges and stick a 10 mm piece on each flap.",
        "<b>Open:</b> with nothing pressed, measure A to B. It must read OL; a number means the gap is bridged.",
        "<b>Light and firm:</b> rest one finger on the flap and read the meter. Then press hard with a thumb.",
        "<b>Flicker:</b> keep pressing and rock your finger. Write Y if the reading jumps or drops to OL.",
        "<b>After 20:</b> press and release 20 times, then take a firm reading. <b>Day 7:</b> repeat a week later.",
    ])
    left_story, story = story, [Paragraph("Pass or fail", H)] + _bullets([
        "<b>Pass:</b> open reads OL, and pressed reads under 10 Ω with no flicker.",
        "<b>Fail:</b> any reading when open, OL or flicker when pressed, or a rise by day 7.",
    ])
    story += [
        Paragraph("Why 10 Ω: lesson LEDs use 220 Ω, so 10 Ω changes their current by under 5 %. "
                  "Flicker matters more: it shows up as a flickering LED.", NOTE),
        Paragraph("If TB passes as well as TA, standard v0.2 can widen switch gaps to 3 mm and drop "
                  "the 2 mm exception. Write the result on sheet 2.", NOTE),
    ]
    rest += sh.flow([(x0, 150.0, 115.0, 210.0)], left_story) + sh.flow([(121.0, 150.0, x1, 210.0)], story)
    if rest:
        raise RuntimeError(f"T0 sheet 3 overflowed by {len(rest)} items")
    sh.rect(x0, 214, x1, 281, stroke=GUIDE, width=0.25, radius=1.2)
    sh.text(x0 + 2, 218, "Notes", size=6.5, bold=True, color=MUTED)
    E.footer(sh, f"{PAGE_ID} sheet 3 of 3")


def _corner_switch_test(sh):
    """The standard corner switch, with its pair's lanes led out to two test points."""
    lane_a, lane_b = S.SWITCH_LANE_X
    top = S.SWITCH_LANE_TOP
    E.lane(sh, [(lane_a, top), (lane_a, 31), (146, 31)])
    E.lane(sh, [(lane_b, top), (lane_b, 40), (156, 40)])
    E.fold_switch(sh, stubs=False)
    for x, y, label in ((150.0, 31.0, "A"), (160.0, 40.0, "B")):
        E.test_point(sh, x, y)
        sh.text(x - 4.7, y + 1.1, label, size=6, color=MUTED, align="right")
    sh.text(156, 48.5, "S1 · corner switch", size=7, bold=True)
    sh.text(156, 52, "fold the corner down to press", size=6.5, color=MUTED)


def _tab_station(sh, x, upper, tab_id, desc, gap):
    """A tab switch whose pair lanes overlap only under the landing, then lead apart to A and B."""
    pitch = S.TAPE_W + gap
    lower = upper + pitch
    E.lane(sh, [(x + 5, upper), (x - 20, upper)])
    E.lane(sh, [(x - 5, lower), (x + 20, lower)])
    E.tab_switch(sh, x, upper, tab_id, pitch=pitch)
    E.test_point(sh, x - 17, upper)
    E.test_point(sh, x + 17, lower)
    sh.text(x - 17, upper - 4.7, "A", size=6, color=MUTED, align="center")
    sh.text(x + 17, lower + 6.7, "B", size=6, color=MUTED, align="center")
    sh.text(x, lower + 9.5, desc, size=6.5, color=MUTED, align="center")


def _switch_table():
    head = style(6.5, leading=7.5, bold=True)
    data = [[""] + [Paragraph(f"{name}<br/><font color='#666666'>{unit}</font>", head) for name, unit in SWITCH_COLS]]
    data += [[row] + [""] * len(SWITCH_COLS) for row in SWITCH_ROWS]
    return _table(data, [27] + [23] * len(SWITCH_COLS), 8)
