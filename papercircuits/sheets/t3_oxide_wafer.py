"""T3 copper oxide wafer.

An exploration, not a standard decision: can a class grow its own diodes, and learn how
chips are made while it does? One square of copper foil is oxidised on a hot plate (the
wafer). Its dies are tested in place (wafer sort), cut apart with scissors (dicing), tested
again (final test) and sorted into bins. The best can be packaged on copper-tape leads.
The physics, sources and hazards are in docs/explorations/paper-semiconductors.md.

Sheet 1 is the wafer frame, the packages and the bin trays: print on card.
Sheets 2 and 3 are the results and the procedure: print on plain paper.

The words are in t3_oxide_wafer.md. A section that prints its own heading is named after
it; a row's words are "name · hint", keyed by its code. The recipe numbers and bin limits
below are filled into the words, and so is the T3 tag: the words layer's own tags don't
include it yet.
"""

from reportlab.platypus import Paragraph

from .. import elements as E
from .. import standard as S
from .. import testsheet as ts
from ..draw import FAINT, FONT_BOLD, GUIDE, INK, MUTED, Sheet, style
from ..provisional import HEADER_STATUS, T3
from ..words import Words

PAGE_ID = "T3"
WORDS = Words.beside(__file__)
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
BINS = ("1", "2", "3", "R", "S", "O")

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

# What the words fill in, besides the words layer's own tags.
VALUES = {
    "T3": T3,
    "foil": FOIL, "plate_w": PLATE_W, "heat_min": HEAT_MIN, "cool_min": COOL_MIN,
    "fair": f"{FAIR:g}", "weak": f"{WEAK:g}", "short_v": f"{SHORT_V:g}",
    "wafer": f"{WAFER:g}", "die": f"{DIE:g}",
}


def _items(name):
    return WORDS.items(name, **VALUES)


def _fields(name):
    return WORDS.fields(name, **VALUES)


def _row(text):
    """A row's words, "name · hint", as (name, hint)."""
    name, _, hint = text.partition(" · ")
    return name, hint


def _plain(texts):
    return [Paragraph(t, style(7.5, leading=9.6)) for t in texts]


def _section(name, kind, notes=0, heading=None):
    """A procedure heading, then the words' section `name`: its items as `kind`, and its
    last `notes` paragraphs as notes. The heading is the section's name, or, where that
    can't be (it carries a tag), the section's first paragraph: pass heading=True."""
    items = _items(name)
    if heading:
        name, *items = items
    body, after = items[:len(items) - notes], items[len(items) - notes:]
    return [Paragraph(name, ts.H)] + kind(body) + [Paragraph(t, ts.NOTE) for t in after]


def build(path):
    sh = Sheet(path, WORDS.text("PDF title"))
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
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, part="1/3")
    E.spine(sh)
    _wafer(sh)
    _die_key(sh)
    _packages(sh)
    _trays(sh)
    E.footer(sh, f"{PAGE_ID} {_fields('Sheet 1')['footer']}")


def _wafer(sh):
    words = _fields("Fixtures")
    sh.text(LEFT, 30, words["wafer"], size=10, bold=True)
    sh.paragraph(LEFT, 32, 168, words["wafer_intro"], style(7, color=MUTED))
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
        sh.text(cx, cy, words["name"] if (r, c) == (0, 0) else words["scrap"], size=6, color=MUTED, align="center")
    sh.text(x0 + WAFER / 2, y1 + 7.5, words["wafer_size"], size=6, color=MUTED, align="center")


def _die_key(sh):
    x, y, k = 150.0, 55.0, 2.0
    title, *key = _items("Die key")
    sh.text(142, 50, title, size=7, bold=True)
    sh.rect(x, y, x + DIE * k, y + DIE * k, stroke=GUIDE, width=0.3, dash=(1.5, 1))
    _die_marks(sh, x, y, scale=k, dot_stroke=INK)
    sh.text(x + 2.4, y + 7.2, "17", size=7, bold=True, color=MUTED)
    sh.text(x + T_DOT[0] * k, y + T_DOT[1] * k + 1.3, "T", size=8, bold=True, align="center")
    sh.text(x + (S_OPEN[0] + S_OPEN[2]) * k / 2, y + (S_OPEN[1] + S_OPEN[3]) * k / 2 + 1.3, "S",
            size=8, bold=True, align="center")
    sh.paragraph(142, 90, 60, "<br/>".join(key), style(6.5, leading=8.4, color=INK))


def _packages(sh):
    words = _fields("Fixtures")
    sh.text(LEFT, 151, words["packages"], size=10, bold=True)
    sh.paragraph(LEFT, 153, 168, words["packages_intro"], style(7, color=MUTED))
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
    sh.text(LEFT, 238, _fields("Fixtures")["trays"], size=10, bold=True)
    trays = _fields("Bin trays")
    x0, gap = LEFT + 3, 4.0  # x0 keeps the first tray clear of H4's label
    w = (RIGHT - x0 - gap * (len(trays) - 1)) / len(trays)
    top, bottom = 241.0, 281.0
    for i, (name, hint) in enumerate(trays.items()):
        x = x0 + i * (w + gap)
        sh.rect(x, top, x + w, bottom, stroke=INK, width=0.35, radius=1.2)
        sh.runs(x + 2, top + 4.2, [(name, True), (f"  {hint}", False)], size=7)
        for j in range(4):
            dx = x + (w - 2 * DIE - 2) / 2 + (j % 2) * (DIE + 2)
            dy = top + 6.5 + (j // 2) * (DIE + 1.5)
            sh.rect(dx, dy, dx + DIE, dy + DIE, stroke=FAINT, width=0.3)


# Sheet 2: the wafer map and results

def _results(sh):
    sheet = _fields("Sheet 2")
    E.header(sh, PAGE_ID, sheet["title"], sheet["subtitle"], part="2/3", status=HEADER_STATUS)
    E.spine(sh)
    sh.runs(LEFT, 30, _record("Wafer record", ("________", "________________", "______ V", "______ mA")), size=7)
    sh.runs(LEFT, 36, _record("Recipe record", ("______ W", "______ min", "______ min", "______ mm", "__________")),
            size=7)
    # Tables first: they draw with whatever dash the canvas was last given.
    side = [Paragraph(sheet["bins"], ts.H), _bin_table(), Paragraph(sheet["yield"], ts.H), _yield_table()]
    rest = sh.flow([(116.0, 42.0, RIGHT, 142.0)], side)
    half = len(DIES) // 2
    rest += sh.flow([(LEFT, 151.0, LEFT + 79, 262.0)], [_die_table(range(1, half + 1))])
    rest += sh.flow([(RIGHT - 79, 151.0, RIGHT, 262.0)], [_die_table(range(half + 1, len(DIES) + 1))])
    if rest:
        raise RuntimeError(f"T3 sheet 2 overflowed by {len(rest)} items")
    _wafer_map(sh, sheet)
    _title_with_hint(sh, 147.5, sheet["every_die"], sheet["every_die_hint"])
    sh.paragraph(LEFT, 267, 168, sheet["reversed"], ts.NOTE)
    E.footer(sh, f"{PAGE_ID} {sheet['footer']}")


def _record(name, blanks):
    """A line of labels to fill in, each in bold with its blank after it."""
    runs = []
    for i, (label, blank) in enumerate(zip(_items(name), blanks)):
        runs += [(("    " if i else "") + label + " ", True), (blank, False)]
    return runs


def _title_with_hint(sh, y, title, hint):
    """A small heading on baseline y, with a muted hint running on after it."""
    sh.text(LEFT, y, title, size=9, bold=True)
    sh.paragraph(LEFT + sh.width(title, 9, bold=True) + 3, y - 2.6, 140, hint, style(7, color=MUTED))


def _wafer_map(sh, sheet):
    x0, y0, cell = 36.0, 47.0, 12.0
    _title_with_hint(sh, 43.5, sheet["map"], sheet["map_hint"])
    size = cell * GRID
    for k in range(1, GRID):
        sh.line(x0 + k * cell, y0, x0 + k * cell, y0 + size, width=0.25, color=GUIDE)
        sh.line(x0, y0 + k * cell, x0 + size, y0 + k * cell, width=0.25, color=GUIDE)
    sh.polygon(_clipped_outline(x0, y0, size, cell), stroke=INK, width=0.4)
    sh.rect(x0 + cell, y0 + cell, x0 + size - cell, y0 + size - cell, stroke=INK, width=0.5, dash=(2, 1))
    for n, (r, c) in enumerate(DIES, 1):
        sh.text(x0 + c * cell + 1, y0 + r * cell + 3.2, str(n), size=6, color=MUTED)
    sh.text(x0 + size / 2, y0 + size + 4.5, sheet["centre"], size=6, color=MUTED, align="center")


def _bin_table():
    words = _fields("Bin table")
    data = [_items("Bin table columns")]
    data += [[f"{code}  {name}", rule, "", ""] for code, (name, rule) in ((c, _row(words[c])) for c in BINS)]
    data += [[*_row(words["pass"]), "", ""]]
    t = ts.table(data, [21, 33, 16, 16], 5.6)
    t.setStyle([("FONT", (0, 0), (-1, 0), FONT_BOLD, 7)])
    return t


def _yield_table():
    counts = {"sort": str(len(DIES)), "overall": str(len(DIES)),
              "centre": str(sum(_is_centre(*d) for d in DIES)), "edge": str(sum(not _is_centre(*d) for d in DIES))}
    data = [_items("Yield table columns")]
    data += [[stage, counts.get(key, ""), "", ""] for key, stage in _fields("Yield table").items()]
    t = ts.table(data, [34, 17, 17, 18], 5.6)
    t.setStyle([("FONT", (0, 0), (-1, 0), FONT_BOLD, 7)])
    return t


def _die_table(numbers):
    stages = _fields("Die table")
    die, *readings = _items("Die table columns")
    data = [["", stages["sort"], "", "", stages["final"], "", ""], [die, *readings, *readings]]
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
    sheet = _fields("Sheet 3")
    E.header(sh, PAGE_ID, sheet["title"], sheet["subtitle"], part="3/3", status=HEADER_STATUS)
    E.spine(sh)
    left = _section("Why it works", _plain)
    left += _section("You need", ts.bullets)
    left += _section("Safety", ts.bullets)
    left += _section("1 · Prepare the wafer", ts.steps)
    left += _section("2 · Oxidise", ts.steps, heading=True)

    right = _section("3 · Mark the dies", ts.steps)
    right += _section("4 · Wafer sort", ts.steps)
    right += _section("5 · Dice and final test", ts.steps)
    right += _section("6 · Package, if you like", ts.steps)
    right += _section("Pass or fail", ts.bullets)
    right += _section("Results", lambda questions: [ts.decision_table(questions, widths=(38, 43), row_height=7)],
                      notes=1)
    rest = sh.flow([(LEFT, 27.0, 115.0, 282.0)], left) + sh.flow([(121.0, 27.0, RIGHT, 282.0)], right)
    if rest:
        raise RuntimeError(f"T3 sheet 3 overflowed by {len(rest)} items")
    E.footer(sh, f"{PAGE_ID} {sheet['footer']}")
