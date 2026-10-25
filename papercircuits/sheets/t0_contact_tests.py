"""T0 contact tests.

Sheet 1 holds the fixtures: print three copies on card, because test 3 needs a stack.
Sheet 2 is the procedure and the binder results: print one on plain paper.
Sheet 3 is test 4, switch contacts, with its own steps and results: print one on card.

The words are in t0_contact_tests.md. A section that prints its own heading is named
after it; a test row's words are "name · hint", keyed by its code.
"""

from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer

from .. import elements as E
from .. import standard as S
from .. import testsheet as ts
from ..draw import COPPER, GUIDE, INK, MUTED, Sheet, style
from ..words import Words

PAGE_ID = "T0"
WORDS = Words.beside(__file__)
LEFT, RIGHT = 62.0, 202.0  # tests 1 and 2 sit right of the hole treatments

# Test 3: each hole's treatment, by the width of tape it's built on.
HOLE_TAPE = {"H1": S.TAPE_W, "H2": S.TAPE_W, "H3": S.WIDE_TAPE_W, "H4": S.TAPE_W}

TAPE_JOINTS = [("J1", "straight"), ("J2", "joint"), ("J3", "joint"), ("J4", "folded"), ("J5", "cut"),
               ("J6", "joint")]
PART_JOINTS = ("M1", "M2", "M3", "M4", "M5")

# Test 4: the corner switch, then three tab switches that differ only in the pair's gap.
SWITCH_TABS = [("TA", S.SWITCH_PAD_GAP), ("TB", 3.0), ("TC", S.SWITCH_PAD_GAP)]
TAB_X = (60.0, 108.0, 156.0)
TAB_UPPER = 80.0


def build(path):
    sh = Sheet(path, WORDS.text("PDF title"))
    _fixtures(sh)
    sh.next_page()
    _procedure(sh)
    sh.next_page()
    _switch_tests(sh)
    sh.save()


def _fixtures(sh):
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, part="1/3")
    _hole_tests(sh)
    _tape_joints(sh)
    _part_joints(sh)
    sh.rect(LEFT, 264, RIGHT, 281, stroke=GUIDE, width=0.25, radius=1.2)
    sh.text(LEFT + 2, 268, WORDS.fields("Labels")["notes"], size=6.5, bold=True, color=MUTED)
    E.footer(sh, f"{PAGE_ID} {WORDS.fields('Sheet 1')['footer']}")


def _hole_tests(sh):
    """Test 3 fixtures: one treatment per hole, each with a test point to probe against the post."""
    words = WORDS.fields("Hole fixtures")
    for hole_id, width in HOLE_TAPE.items():
        name, how = ts.row(words[hole_id])
        y = S.hole_y(hole_id)
        E.lane(sh, [(S.NET_STRIP_START_X, y), (46, y)], width=width)
        E.test_point(sh, 44, y, f"TP-{hole_id}")
        sh.runs(S.NET_STRIP_START_X, y + width / 2 + 4.5, [(name, True), (" · " + how, False)], size=6.5)
    E.spine(sh, connected=HOLE_TAPE, strip_widths=HOLE_TAPE)


def _tape_joints(sh):
    words = WORDS.fields("Tape joint fixtures")
    sh.text(LEFT, 30, words["title"], size=10, bold=True)
    sh.paragraph(LEFT, 32, RIGHT - LEFT, words["intro"], style(7, color=MUTED))
    sh.runs(LEFT, 44, [(words["zero"] + " ", True), ("_______ Ω", False), ("      " + words["built"] + " ", True),
                       ("______________", False)], size=7)
    ts.result_headers(sh, 44)

    x_a, x_b, x_bend = 102.0, 154.0, 126.0
    y = 51.0
    for jid, shape in TAPE_JOINTS:
        name, hint = ts.row(words[jid])
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
        ts.result_boxes(sh, (y + y_end) / 2)
        y = y_end + 11


def _part_joints(sh):
    words = WORDS.fields("Part joint fixtures")
    sh.text(LEFT, 140, words["title"], size=10, bold=True)
    sh.paragraph(LEFT, 142, RIGHT - LEFT, words["intro"], style(7, color=MUTED))
    sh.runs(LEFT, 154, [(words["alone"] + " ", True), ("_______ Ω", False), ("   " + words["alone_hint"], False)],
            size=7)

    col_w, top, gap0, gap1, bottom = 25.0, 172.0, 197.0, 207.0, 232.0
    mid = (gap0 + gap1) / 2
    rows = tuple(zip((words[k] for k in ("day0", "flexed", "day7", "flicker")), (239.0, 245.0, 251.0, 257.0)))
    for label, ry in rows:
        sh.text(LEFT, ry + 1.1, label, size=6.5, bold=True)
    for i, mid_id in enumerate(PART_JOINTS):
        name, how = ts.row(words[mid_id])
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
    sheet = WORDS.fields("Sheet 2")
    E.header(sh, PAGE_ID, sheet["title"], sheet["subtitle"], part="2/3")
    E.spine(sh)
    bullets, steps = ts.bullets, ts.steps

    story = ts.section(WORDS, "You need", bullets)
    story += ts.section(WORDS, "Before you start", steps)
    story += ts.section(WORDS, "1 · Tape joints", steps)
    story += ts.section(WORDS, "2 · Part joints", steps, notes=1)

    left_story, story = story, ts.section(WORDS, "3 · Binder contacts", steps)
    story += [Spacer(1, 2 * mm), _binder_table()]
    story += ts.section(WORDS, "4 · Switch contacts", ts.plain)
    story += ts.section(WORDS, "Pass or fail", bullets, notes=1)
    story += ts.section(WORDS, "Results for standard v0.2", _decision_table)

    left = (S.ZONE_BUILD[0], 27.0, 115.0, 282.0)
    right = (121.0, 27.0, S.ZONE_BUILD[2], 282.0)
    rest = sh.flow([left], left_story) + sh.flow([right], story)
    if rest:
        raise RuntimeError(f"T0 sheet 2 overflowed by {len(rest)} items")
    E.footer(sh, f"{PAGE_ID} {sheet['footer']}")


def _binder_table():
    head = style(6.5, leading=7.5, bold=True)
    short = WORDS.fields("Binder table columns")
    data = [[""] + [Paragraph(f"{h}<br/>{short[h]}", head) for h in HOLE_TAPE]]
    for row in WORDS.items("Binder table rows"):
        data.append([row, "", "", "", ""])
    return ts.table(data, [24, 14, 14, 14, 14], 7.5)


def _decision_table(questions):
    return [ts.decision_table(questions)]


def _switch_tests(sh):
    sheet, words = WORDS.fields("Sheet 3"), WORDS.fields("Switch fixtures")
    E.header(sh, PAGE_ID, sheet["title"], sheet["subtitle"], part="3/3")
    E.spine(sh)
    x0, _, x1, _ = S.ZONE_BUILD
    sh.text(x0, 31, words["title"], size=10, bold=True)
    sh.paragraph(x0, 33, 106, words["intro"], style(7, color=MUTED))
    _corner_switch_test(sh, words)
    for (tab_id, gap), x in zip(SWITCH_TABS, TAB_X):
        _tab_station(sh, x, TAB_UPPER, tab_id, words[tab_id], gap)

    rest = sh.flow([(x0, 104.0, x1, 146.0)], [_switch_table()])
    left_story = ts.section(WORDS, "How to test", ts.steps)
    story = ts.section(WORDS, "Switch pass or fail", ts.bullets, notes=2, heading=True)
    rest += sh.flow([(x0, 150.0, 115.0, 210.0)], left_story) + sh.flow([(121.0, 150.0, x1, 210.0)], story)
    if rest:
        raise RuntimeError(f"T0 sheet 3 overflowed by {len(rest)} items")
    sh.rect(x0, 214, x1, 281, stroke=GUIDE, width=0.25, radius=1.2)
    sh.text(x0 + 2, 218, WORDS.fields("Labels")["notes"], size=6.5, bold=True, color=MUTED)
    E.footer(sh, f"{PAGE_ID} {sheet['footer']}")


def _corner_switch_test(sh, words):
    """The standard corner switch, with its pair's lanes led out to two test points."""
    lane_a, lane_b = S.SWITCH_LANE_X
    top = S.SWITCH_LANE_TOP
    a = E.lane(sh, [(lane_a, top), (lane_a, 31), (146, 31)])
    b = E.lane(sh, [(lane_b, top), (lane_b, 40), (156, 40)])
    sh.allow(a, b, S.SWITCH_PAD_GAP)
    E.fold_switch(sh, stubs=False)
    for x, y, label in ((150.0, 31.0, "A"), (160.0, 40.0, "B")):
        E.test_point(sh, x, y)
        sh.text(x - 4.7, y + 1.1, label, size=6, color=MUTED, align="right")
    sh.text(156, 48.5, words["corner"], size=7, bold=True)
    sh.text(156, 52, words["corner_hint"], size=6.5, color=MUTED)


def _tab_station(sh, x, upper, tab_id, desc, gap):
    """A tab switch whose pair lanes overlap only under the landing, then lead apart to A and B."""
    pitch = S.TAPE_W + gap
    lower = upper + pitch
    a = E.lane(sh, [(x + 5, upper), (x - 20, upper)])
    b = E.lane(sh, [(x - 5, lower), (x + 20, lower)])
    sh.allow(a, b, gap)
    E.tab_switch(sh, x, upper, tab_id, pitch=pitch)
    E.test_point(sh, x - 17, upper)
    E.test_point(sh, x + 17, lower)
    sh.text(x - 17, upper - 4.7, "A", size=6, color=MUTED, align="center")
    sh.text(x + 17, lower + 6.7, "B", size=6, color=MUTED, align="center")
    sh.text(x, lower + 9.5, desc, size=6.5, color=MUTED, align="center")


def _switch_table():
    head = style(6.5, leading=7.5, bold=True)
    cols = WORDS.fields("Switch table columns")
    data = [[""] + [Paragraph(f"{name}<br/><font color='#666666'>{unit}</font>", head) for name, unit in cols.items()]]
    data += [[row] + [""] * len(cols) for row in WORDS.items("Switch table rows")]
    return ts.table(data, [27] + [23] * len(cols), 8)
