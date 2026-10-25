"""T3 copper oxide wafer.

An exploration, not a standard decision: can a class grow its own diodes, and learn how
chips are made while it does? One square of copper foil is oxidised on a hot plate (the
wafer). Its dies are tested in place (wafer sort), cut apart with scissors (dicing), tested
again (final test) and sorted into bins. The best can be packaged on copper-tape leads.
The physics, sources and hazards are in docs/explorations/paper-semiconductors.md.

Sheet 1 is the wafer frame, the packages and the bin trays: print on card.
Sheets 2 and 3 are the results and the procedure: print on plain paper.
"""

from reportlab.platypus import Paragraph

from .. import elements as E
from .. import standard as S
from .. import testsheet as ts
from ..draw import FAINT, FONT_BOLD, GUIDE, INK, MUTED, Sheet, style
from ..provisional import HEADER_STATUS, T1, T3

PAGE_ID = "T3"
LEFT, RIGHT = S.ZONE_BUILD[0], S.ZONE_BUILD[2]

# Recipe and bin limits the first wafer will settle [T3].
FOIL = "0.1–0.2 mm"   # thick enough to survive oxidising, thin enough for scissors
PLATE_W = 1000        # the coil must glow red; a 700 W plate may not get hot enough
HEAT_MIN = 30         # minutes at full heat once the coil glows
COOL_MIN = 20         # minutes cooling on the switched-off plate
SHORT_V = 0.05        # V: both readings under this is a short
FAIR, WEAK = 3, 1.5   # Rev ÷ Fwd at least this for bins 2 and 3
# Fwd puts the red probe on T: Grondahl's easy direction ran from the top contact into the
# copper. Nobody has checked it with pencil graphite instead of his lead.
BINS = [
    ("1", "Good", "Rev OL, Fwd reads"),
    ("2", "Fair", f"Rev ≥ {FAIR:g} × Fwd"),
    ("3", "Weak", f"Rev {WEAK:g}–{FAIR:g} × Fwd"),
    ("R", "Resistor", f"Rev < {WEAK:g} × Fwd"),
    ("S", "Short", f"both < {SHORT_V:g} V"),
    ("O", "Open", "both OL"),
]

# The wafer: a 90 mm square cut into a 6 × 6 grid of 15 mm dies. Its corners are clipped
# along the corner cells' diagonals, so 32 whole dies remain: 16 in the centre, 16 round the edge.
WAFER_X, WAFER_Y = 44.0, 47.0
DIE = 15.0
GRID = 6
WAFER = DIE * GRID
CLIPPED = {(0, 0), (0, GRID - 1), (GRID - 1, 0), (GRID - 1, GRID - 1)}
DIES = [(r, c) for r in range(GRID) for c in range(GRID) if (r, c) not in CLIPPED]
TICK = 3.0

# Inside a die, in mm from its top-left corner: the pencil dot T and the scraped corner S.
T_DOT, T_DOT_D = (5.5, 9.5), 5.0
S_OPEN = (11.0, 0.0, 15.0, 4.0)

# Packages: a die face up in a landing, with a copper-tape lead from each test point onto it.
PACKAGES = ("D1", "D2", "D3", "D4")
PACKAGE_X = (47.0, 89.0, 131.0, 173.0)  # landings' left edges
PACKAGE_Y = 190.0                        # landings' top edge
LEAD = 24.0                              # how far each lead runs off the die

TRAYS = [
    ("Bin 1", "good"),
    ("Bin 2", "fair"),
    ("Bin 3", "weak"),
    ("Reject", "R, S and O"),
]


def build(path):
    sh = Sheet(path, "T3 copper oxide wafer")
    _fixtures(sh)
    sh.next_page()
    _results(sh)
    sh.next_page()
    _procedure(sh)
    sh.save()


def _is_centre(r, c):
    return 0 < r < GRID - 1 and 0 < c < GRID - 1


def _hatch(sh, x0, y0, x1, y1, step=0.8):
    """A lightly hatched box: scrape here."""
    c = x0 + y0 + step
    while c < x1 + y1:
        xa, xb = max(x0, c - y1), min(x1, c - y0)
        if xa < xb:
            sh.line(xa, c - xa, xb, c - xb, width=0.12, color=GUIDE)
        c += step
    sh.rect(x0, y0, x1, y1, stroke=MUTED, width=0.25)


def _die_marks(sh, x, y, scale=1.0, dot_stroke=MUTED):
    """The scraped corner S and the pencil dot T of a die whose top-left corner is (x, y)."""
    sx0, sy0, sx1, sy1 = S_OPEN
    _hatch(sh, x + sx0 * scale, y + sy0 * scale, x + sx1 * scale, y + sy1 * scale, step=0.8 * scale)
    sh.circle(x + T_DOT[0] * scale, y + T_DOT[1] * scale, T_DOT_D * scale, stroke=dot_stroke, width=0.3,
              dash=(0.8, 0.6))


def _clipped_outline(x0, y0, size, cut):
    x1, y1 = x0 + size, y0 + size
    return [(x0 + cut, y0), (x1 - cut, y0), (x1, y0 + cut), (x1, y1 - cut),
            (x1 - cut, y1), (x0 + cut, y1), (x0, y1 - cut), (x0, y0 + cut)]


# Sheet 1: the frame, packages and trays

def _fixtures(sh):
    E.header(sh, PAGE_ID, "T3  Copper oxide wafer",
             "Grow diodes on one sheet of copper, cut them apart and test every one. Print on card.",
             part="1/3")
    E.spine(sh)
    _wafer(sh)
    _die_key(sh)
    _packages(sh)
    _trays(sh)
    E.footer(sh, f"{PAGE_ID} sheet 1 of 3")


def _wafer(sh):
    sh.text(LEFT, 30, "1  Wafer", size=10, bold=True)
    sh.paragraph(LEFT, 32, 168,
                 "After oxidising, lay the wafer on the frame. Rule the streets from tick to tick in fine "
                 "permanent marker and number the dies. After dicing, put each die back on its number.",
                 style(7, color=MUTED))
    x0, y0 = WAFER_X, WAFER_Y
    x1, y1 = x0 + WAFER, y0 + WAFER
    for k in range(1, GRID):
        d = k * DIE
        sh.line(x0 + d, y0, x0 + d, y1, width=0.25, color=GUIDE, dash=(1.5, 1))
        sh.line(x0, y0 + d, x1, y0 + d, width=0.25, color=GUIDE, dash=(1.5, 1))
        for a, b, c, e in ((x0 + d, y0 - TICK, x0 + d, y0 - 0.8), (x0 + d, y1 + 0.8, x0 + d, y1 + TICK),
                           (x0 - TICK, y0 + d, x0 - 0.8, y0 + d), (x1 + 0.8, y0 + d, x1 + TICK, y0 + d)):
            sh.line(a, b, c, e, width=0.35)
    sh.polygon(_clipped_outline(x0, y0, WAFER, DIE), stroke=INK, width=0.4)
    for n, (r, c) in enumerate(DIES, 1):
        dx, dy = x0 + c * DIE, y0 + r * DIE
        _die_marks(sh, dx, dy)
        sh.text(dx + 1.2, dy + 3.4, str(n), size=6, bold=True, color=MUTED)
    for r, c in CLIPPED:
        cx, cy = x0 + (c + 0.5) * DIE, y0 + (r + 0.5) * DIE
        cx += 3 if c == 0 else -3
        cy += 4 if r == 0 else -2
        sh.text(cx, cy, "name" if (r, c) == (0, 0) else "scrap", size=6, color=MUTED, align="center")
    sh.text(x0 + WAFER / 2, y1 + 7.5, f"{WAFER:g} mm square, {DIE:g} mm dies, corners clipped",
            size=6, color=MUTED, align="center")


def _die_key(sh):
    x, y, k = 150.0, 55.0, 2.0
    sh.text(142, 50, "One die, 2× size", size=7, bold=True)
    sh.rect(x, y, x + DIE * k, y + DIE * k, stroke=GUIDE, width=0.3, dash=(1.5, 1))
    _die_marks(sh, x, y, scale=k, dot_stroke=INK)
    sh.text(x + 2.4, y + 7.2, "17", size=7, bold=True, color=MUTED)
    sh.text(x + T_DOT[0] * k, y + T_DOT[1] * k + 1.3, "T", size=8, bold=True, align="center")
    sh.text(x + (S_OPEN[0] + S_OPEN[2]) * k / 2, y + (S_OPEN[1] + S_OPEN[3]) * k / 2 + 1.3, "S",
            size=8, bold=True, align="center")
    sh.paragraph(142, 90, 60,
                 "<b>T</b>  top contact: a 5 mm dot of 6B pencil, pressed hard.<br/>"
                 "<b>S</b>  scrape this corner back to bare copper.<br/>"
                 "<b>17</b>  the die's number, in fine marker.<br/>"
                 "<b>Dashed lines</b> are streets: cut along them.<br/>"
                 "The clipped corners aren't dies. Write your wafer's name in the top-left one.",
                 style(6.5, leading=8.4, color=INK))


def _packages(sh):
    sh.text(LEFT, 151, "2  Packages", size=10, bold=True)
    sh.paragraph(LEFT, 153, 168,
                 "Put your best dies in packages. Stick a die face up in a landing, then lay each lead from its "
                 "test point onto the die so its tip covers S or the dot. Sheet 3, step 6, says how.",
                 style(7, color=MUTED))
    for name, px in zip(PACKAGES, PACKAGE_X):
        py = PACKAGE_Y
        sx, tx = px + (S_OPEN[0] + S_OPEN[2]) / 2, px + T_DOT[0]
        E.lane(sh, [(sx, py - LEAD), (sx, py + S_OPEN[3])])
        E.lane(sh, [(tx, py + T_DOT[1] - T_DOT_D / 2), (tx, py + DIE + LEAD)])
        sh.rect(px, py, px + DIE, py + DIE, stroke=INK, width=0.2, dash=(0.5, 0.7))
        _die_marks(sh, px, py, dot_stroke=INK)
        E.test_point(sh, sx, py - LEAD + 4.5, "S", side="left")
        E.test_point(sh, tx, py + DIE + LEAD - 4.5, "T", side="left")
        sh.text(px - 2.5, py + 9, name, size=8, bold=True, align="right")


def _trays(sh):
    sh.text(LEFT, 238, "3  Bin trays", size=10, bold=True)
    x0, gap = LEFT + 3, 4.0  # x0 keeps the first tray clear of H4's label
    w = (RIGHT - x0 - gap * (len(TRAYS) - 1)) / len(TRAYS)
    top, bottom = 241.0, 281.0
    for i, (name, hint) in enumerate(TRAYS):
        x = x0 + i * (w + gap)
        sh.rect(x, top, x + w, bottom, stroke=INK, width=0.35, radius=1.2)
        sh.runs(x + 2, top + 4.2, [(name, True), (f"  {hint}", False)], size=7)
        for j in range(4):
            dx = x + (w - 2 * DIE - 2) / 2 + (j % 2) * (DIE + 2)
            dy = top + 6.5 + (j // 2) * (DIE + 1.5)
            sh.rect(dx, dy, dx + DIE, dy + DIE, stroke=FAINT, width=0.3)


# Sheet 2: the wafer map and results

def _results(sh):
    E.header(sh, PAGE_ID, "T3  Wafer map and results",
             "Readings on the diode range, in volts. OL means over range.", part="2/3",
             status=HEADER_STATUS)
    E.spine(sh)
    sh.runs(LEFT, 30, [("Wafer ", True), ("________", False), ("    Meter ", True), ("________________", False),
                       ("    Open circuit ", True), ("______ V", False), ("    Test current ", True),
                       ("______ mA", False)], size=7)
    sh.runs(LEFT, 36, [("Plate ", True), ("______ W", False), ("    Heat ", True), ("______ min", False),
                       ("    Cool ", True), ("______ min", False), ("    Foil ", True), ("______ mm", False),
                       ("    Date ", True), ("__________", False)], size=7)
    # Tables first: they draw with whatever dash the canvas was last given.
    side = [Paragraph(f"Bins {T3}", ts.H), _bin_table(), Paragraph("Yield", ts.H), _yield_table()]
    rest = sh.flow([(116.0, 42.0, RIGHT, 142.0)], side)
    half = len(DIES) // 2
    rest += sh.flow([(LEFT, 151.0, LEFT + 79, 262.0)], [_die_table(range(1, half + 1))])
    rest += sh.flow([(RIGHT - 79, 151.0, RIGHT, 262.0)], [_die_table(range(half + 1, len(DIES) + 1))])
    if rest:
        raise RuntimeError(f"T3 sheet 2 overflowed by {len(rest)} items")
    _wafer_map(sh)
    _title_with_hint(sh, 147.5, "Every die",
                     f"<b>Fwd:</b> red on T, black on S {T3}. <b>Rev:</b> red on S, black on T.")
    sh.paragraph(LEFT, 267, 168,
                 "If a die reads lower with red on S, it conducts the other way: bin it on the larger reading "
                 "÷ the smaller, and circle its number.",
                 ts.NOTE)
    E.footer(sh, f"{PAGE_ID} sheet 2 of 3")


def _title_with_hint(sh, y, title, hint):
    """A small heading on baseline y, with a muted hint running on after it."""
    sh.text(LEFT, y, title, size=9, bold=True)
    sh.paragraph(LEFT + sh.width(title, 9, bold=True) + 3, y - 2.6, 140, hint, style(7, color=MUTED))


def _wafer_map(sh):
    x0, y0, cell = 36.0, 47.0, 12.0
    _title_with_hint(sh, 43.5, "Wafer map", "write each die's bin: sort / final")
    size = cell * GRID
    for k in range(1, GRID):
        sh.line(x0 + k * cell, y0, x0 + k * cell, y0 + size, width=0.25, color=GUIDE)
        sh.line(x0, y0 + k * cell, x0 + size, y0 + k * cell, width=0.25, color=GUIDE)
    sh.polygon(_clipped_outline(x0, y0, size, cell), stroke=INK, width=0.4)
    sh.rect(x0 + cell, y0 + cell, x0 + size - cell, y0 + size - cell, stroke=INK, width=0.5, dash=(2, 1))
    for n, (r, c) in enumerate(DIES, 1):
        sh.text(x0 + c * cell + 1, y0 + r * cell + 3.2, str(n), size=6, color=MUTED)
    sh.text(x0 + size / 2, y0 + size + 4.5, "dashed: the centre 16", size=6, color=MUTED, align="center")


def _bin_table():
    data = [["Bin", "Rule", "Sort", "Final"]]
    data += [[f"{code}  {name}", rule, "", ""] for code, name, rule in BINS]
    data += [["Pass", "bins 1, 2 and 3", "", ""]]
    t = ts.table(data, [21, 33, 16, 16], 5.6)
    t.setStyle([("FONT", (0, 0), (-1, 0), FONT_BOLD, 7)])
    return t


def _yield_table():
    data = [["Stage", "In", "Pass", "Yield"],
            ["Wafer sort", str(len(DIES)), "", ""],
            ["Final test", "", "", ""],
            ["Packages", "", "", ""],
            ["Overall", str(len(DIES)), "", ""],
            ["Centre 16, sort", str(sum(_is_centre(*d) for d in DIES)), "", ""],
            ["Edge 16, sort", str(sum(not _is_centre(*d) for d in DIES)), "", ""]]
    t = ts.table(data, [34, 17, 17, 18], 5.6)
    t.setStyle([("FONT", (0, 0), (-1, 0), FONT_BOLD, 7)])
    return t


def _die_table(numbers):
    data = [["", "Wafer sort", "", "", "Final test", "", ""],
            ["Die", "Fwd", "Rev", "Bin", "Fwd", "Rev", "Bin"]]
    data += [[str(n), "", "", "", "", "", ""] for n in numbers]
    t = ts.table(data, [9, 13, 13, 9, 13, 13, 9], 6.0)
    t.setStyle([
        ("SPAN", (1, 0), (3, 0)),
        ("SPAN", (4, 0), (6, 0)),
        ("FONT", (0, 0), (-1, 1), FONT_BOLD, 7),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LINEAFTER", (3, 0), (3, -1), 1.0, INK),
    ])
    return t


# Sheet 3: the procedure

def _procedure(sh):
    E.header(sh, PAGE_ID, "T3  Running the wafer test",
             "Print on plain paper. An adult runs every hot-plate step.", part="3/3", status=HEADER_STATUS)
    E.spine(sh)
    h = ts.H
    left = [Paragraph("Why it works", h),
            Paragraph("Copper(I) oxide is a semiconductor. Where it meets the copper underneath, there's a "
                      "barrier that lets current through far more easily one way than the other: a diode. "
                      "The pencil dot only has to reach the oxide. How well each die works depends on how its "
                      "oxide grew, so dies from one wafer differ, just as real chips do.",
                      style(7.5, leading=9.6))]
    left += [Paragraph("You need", h)] + ts.bullets([
        f"A 90 mm square of bare, uncoated copper foil, {FOIL} thick {T3}, and a spare scrap",
        f"A single-coil electric hot plate, {PLATE_W} W or more {T3}, on a heatproof board",
        "Tongs, and safety glasses for everyone near the plate",
        "Washing-up liquid, a kitchen scouring pad and kitchen roll",
        "Old scissors, a ruler, a fine permanent marker, a craft knife or fine sandpaper, and a 6B pencil",
        "A multimeter with a diode range, and a 1N4148 diode (L06's D1) to check it",
    ])
    left += [Paragraph("Safety", h)] + ts.bullets([
        "<b>An adult runs the hot plate</b> and moves the copper with tongs. Keep everyone else an arm's "
        "length away, and open a window or run an extractor.",
        "<b>Heat only clean, bare copper.</b> Never copper tape, coated foil, brass, zinc or galvanised metal: "
        "glue and coatings smoke, and zinc fumes make people ill.",
        "<b>Goggles on while it cools:</b> black flakes jump off. Hot copper looks like cold copper.",
        "<b>No acids, lye or lead.</b> Wipe flakes up with damp kitchen roll, and wash hands afterwards.",
        "Cut foil is sharp. Craft knives are for adults.",
    ])
    left += [Paragraph("1 · Prepare the wafer", h)] + ts.steps([
        "Cut the square. Clip each corner off along a diagonal from 15 mm along one edge to 15 mm along the other.",
        "Scrub both sides with washing-up liquid and the scouring pad until bright. Rinse, dry, and hold it "
        "by its edges from now on.",
    ])
    left += [Paragraph(f"2 · Oxidise {T3}", h)] + ts.steps([
        "<b>Adult:</b> lay the wafer flat in the middle of the cold plate and turn it to full.",
        f"It turns orange, purple and red, then black. Keep it at full heat for {HEAT_MIN} min after the "
        "coil starts to glow.",
        f"Switch off and leave it on the plate for {COOL_MIN} min. The black layer flakes off as it shrinks. "
        "Moving it too soon keeps the black on.",
        "Rinse it under the tap, rubbing gently with fingertips only, and pat it dry. The red-orange layer "
        "left is copper(I) oxide. Don't bend it.",
    ])

    right = [Paragraph("3 · Mark the dies", h)] + ts.steps([
        "Lay the wafer on sheet 1's frame. Rule the streets from tick to tick in fine marker. Never use "
        "pencil: graphite would join the dies.",
        "Write the wafer's name in its top-left corner, and each die's number in its own top-left corner.",
        "<b>S:</b> scrape each die's top-right corner back to shiny copper, about 4 mm square.",
        "<b>T:</b> draw a 5 mm dot of 6B where sheet 1 shows it, pressing hard. Keep it clear of S and the streets.",
    ])
    right += [Paragraph("4 · Wafer sort", h)] + ts.steps([
        "Check the meter on the 1N4148: about 0.6 V one way, OL the other.",
        f"On the diode range, measure every die. <b>Fwd:</b> red on T, black on S {T3}. "
        "<b>Rev:</b> red on S, black on T. Keep the light and the probe pressure the same throughout.",
        "Bin each die by the table on sheet 2, and write its bin on the wafer map.",
    ])
    right += [Paragraph("5 · Dice and final test", h)] + ts.steps([
        "Cut along the streets with old scissors, rows first. Put each die back on its number on sheet 1.",
        "Test every die again, re-bin it, and move it to its bin tray.",
        "Count the bins and fill in the yields. A stage's <b>In</b> is the number that passed the stage before it.",
    ])
    right += [Paragraph("6 · Package, if you like", h)] + ts.steps([
        "Stick a Bin 1 die face up in a D landing with glue stick.",
        f"Lay each lead from its test point onto the die, its tip over S or the dot. Rub 6B into the "
        f"tip's glue first, or solder the S lead. {T1}",
        "Measure Fwd and Rev between the T and S test points.",
    ])
    right += [Paragraph("Pass or fail", h)] + ts.bullets([
        "A die passes in bins 1, 2 or 3. Bin 1 is the goal: it blocks the meter completely in reverse.",
        "No die rectifies? Check the meter on the 1N4148 again, then try a sharpened 6B pencil point pressed "
        "on a die in place of its dot.",
        "Compare the centre 16 with the edge 16. A difference means the plate heats unevenly.",
    ])
    right += [Paragraph("Results", h),
              ts.decision_table(["Did any die rectify?", "Fwd is red on T?", "Sort yield, final yield",
                                 "Centre or edge better?", "Bin limits to keep"], widths=(38, 43), row_height=7)]
    right += [Paragraph(f"{T3} marks recipe numbers and bin limits that the first wafer will settle. "
                        f"{T1} waits on the pencil tests. Background, sources and hazards: "
                        "docs/explorations/paper-semiconductors.md.", ts.NOTE)]
    rest = sh.flow([(LEFT, 27.0, 115.0, 282.0)], left) + sh.flow([(121.0, 27.0, RIGHT, 282.0)], right)
    if rest:
        raise RuntimeError(f"T3 sheet 3 overflowed by {len(rest)} items")
    E.footer(sh, f"{PAGE_ID} sheet 3 of 3")
