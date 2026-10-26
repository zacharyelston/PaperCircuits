"""T4 book interconnects: the V2 bench tests for issue #39.

V2 binds two-layer pages in a ring binder whose holes carry nothing, so power and signals
cross from page to page through links at the spine. These coupons test how to build those
links, and the wraps that take copper from one side of a page to the other:

1. Edge wraps: 5 mm and 12 mm tape over the top, outer and bottom edges, side A to side B.
2. Links at the page edge and 10 mm inboard, which swing about 24 and 20 mm as a page
   turns, by solder bridge, stranded wire and ribbon.
3. The spine contract proposed in docs/v2/electrical-architecture.md: five pads on the
   ring axis, each passing to side B through a wire via, chained through the book.
4. Links on the ring axis, which twist rather than swing, by wire, ribbon, a stitched
   strain-relief patch and solder bridge.

Sheets 1 and 2 print on the two sides of one card, sheet 2 mirrored like T2's back. Three
cards make a three-page test book: side A takes each link from the page before, side B sends
it to the page after, and an open spread shows both. Sheet 3 is the procedure and sheet 4 the
results.

The words are in t4_book_interconnects.md.
"""

from reportlab.platypus import Paragraph

from .. import elements as E
from .. import standard as S
from .. import testsheet as ts
from ..draw import GUIDE, MUTED, Sheet, style
from ..words import Words

PAGE_ID = "T4"
WORDS = Words.beside(__file__)

# Where each link's lane starts: at the page edge, centred on the ring axis, or 10 mm inboard.
EDGE_START = 3.0
AXIS_START = S.HOLE_X - S.TAPE_W / 2
INBOARD_START = S.HOLE_X + 10 - S.TAPE_W / 2
LINKS = (
    ("E1", EDGE_START, 44.0),
    ("E2", EDGE_START, 56.0),
    ("E3", EDGE_START, 68.0),
    ("I1", INBOARD_START, 80.0),
    ("I2", INBOARD_START, 92.0),
    ("X1", AXIS_START, 204.0),
    ("X2", AXIS_START, 216.0),
    ("X3", AXIS_START, 228.0),
    ("X4", AXIS_START, 240.0),
    ("X5", AXIS_START, 252.0),
)
LANE_END_X, TP_X, LABEL_X = 50.0, 44.0, 56.0

# The proposed spine contract: five pads 8 mm apart on the ring axis between H2 and H3. The
# two GND pads are one strip, joined round the far side of the others.
CONTRACT = ("C1", "C2", "C3", "C4", "C5")
CONTRACT_RESULTS = ("gnd_pair", "bus_a", "power", "bus_b")
CONTRACT_Y0, CONTRACT_PITCH = 132.5, 8.0
CONTRACT_VIA_X = 30.0
GND_TIE_X = 60.0

# Edge wraps: code, tape width, the lane from the edge in to its test point, and the test point.
WRAPS = (
    ("W1", S.TAPE_W, [(186.0, 4.0), (186.0, 34.0)], (186.0, 30.0)),
    ("W2", S.WIDE_TAPE_W, [(199.0, 4.0), (199.0, 34.0)], (199.0, 30.0)),
    ("W3", S.TAPE_W, [(206.0, 120.0), (176.0, 120.0)], (180.0, 120.0)),
    ("W4", S.WIDE_TAPE_W, [(206.0, 140.0), (176.0, 140.0)], (180.0, 140.0)),
    ("W5", S.TAPE_W, [(6.0, 293.0), (6.0, 280.0)], (6.0, 284.0)),
    ("W6", S.WIDE_TAPE_W, [(20.0, 293.0), (20.0, 280.0)], (20.0, 284.0)),
)
LINK_COLUMNS = ("0", "10", "100", "500", "1,000")


def build(path):
    sh = Sheet(path, WORDS.text("PDF title"))
    _front(sh)
    sh.next_page(mirrored=True)
    _back(sh)
    sh.next_page()
    _procedure(sh)
    sh.next_page()
    _results(sh)
    sh.save()


def _contract_y(i):
    return CONTRACT_Y0 + CONTRACT_PITCH * i


def _coupons(sh):
    """The copper, vias and test points, which are the same on both sides: side B's lie
    behind side A's."""
    sh.line(S.HOLE_X, 4, S.HOLE_X, S.PAGE_H - 4, width=0.25, color=GUIDE, dash=(2, 1.5))
    for _, start, y in LINKS:
        E.lane(sh, [(start, y), (LANE_END_X, y)])
        E.test_point(sh, TP_X, y)
    E.lane(
        sh,
        [
            (AXIS_START, _contract_y(0)),
            (GND_TIE_X, _contract_y(0)),
            (GND_TIE_X, _contract_y(4)),
            (AXIS_START, _contract_y(4)),
        ],
    )
    for i in range(1, 4):
        E.lane(sh, [(AXIS_START, _contract_y(i)), (LANE_END_X, _contract_y(i))])
    for i in range(5):
        E.via(sh, CONTRACT_VIA_X, _contract_y(i), "wire")
        E.test_point(sh, TP_X, _contract_y(i))
    for _, width, pts, (tx, ty) in WRAPS:
        E.lane(sh, pts, width=width)
        E.test_point(sh, tx, ty)
    _wrap_codes(sh)


def _wrap_codes(sh):
    for code, _, _, (tx, ty) in WRAPS:
        if ty < 50:
            sh.text(tx, ty + 9, code, size=6.5, bold=True, align="center")
        elif tx > 100:
            sh.text(tx - 6, ty + 1.1, code, size=6.5, bold=True, align="right")
        else:
            sh.text(tx, ty - 6, code, size=6.5, bold=True, align="center")


def _front(sh):
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, part="1/4", status=WORDS.text("Status"))
    E.spine(sh, mechanical=True)
    _coupons(sh)
    sh.text(S.HOLE_X + 2, 101, WORDS.fields("Labels")["axis"], size=6, color=MUTED)

    links = WORDS.fields("Links")
    for title, y in ((links["edge_title"], 37), (links["axis_title"], 197)):
        sh.text(LABEL_X, y, title, size=10, bold=True)
    for code, _, y in LINKS:
        name, hint = ts.row(links[code])
        sh.text(LABEL_X, y - 0.4, f"{code}  {name}", size=7, bold=True)
        if hint:
            sh.text(LABEL_X, y + 3.2, hint, size=6.5, color=MUTED)

    contract = WORDS.fields("Contract")
    label_x = GND_TIE_X + S.TAPE_W / 2 + 4
    sh.text(label_x, 124, contract["title"], size=10, bold=True)
    sh.text(label_x, 128.3, contract["hint"], size=6.5, color=MUTED)
    for i, code in enumerate(CONTRACT):
        sh.text(label_x, _contract_y(i) + 1.1, f"{code}  {contract[code]}", size=7, bold=True)

    wraps = WORDS.fields("Wraps")
    sh.text(110, 48, wraps["title"], size=10, bold=True)
    sh.paragraph(110, 51, 60, wraps["body"], style(6.5, leading=8.2, color=MUTED))
    about = WORDS.items("About")
    sh.paragraph(116, 202, 78, "<br/><br/>".join(about), style(7, leading=8.8, color=MUTED))
    E.footer(sh, f"{PAGE_ID} {WORDS.fields('Sheet 1')['footer']}")


def _back(sh):
    sheet = WORDS.fields("Sheet 2")
    with sh.unmirrored():
        E.header(sh, PAGE_ID, sheet["title"], sheet["subtitle"], part="2/4")
    E.spine(sh, mechanical=True)
    _coupons(sh)
    for code, _, y in LINKS:
        sh.text(LABEL_X, y + 1.1, code, size=6.5, bold=True)
    for i, code in enumerate(CONTRACT):
        sh.text(GND_TIE_X + S.TAPE_W / 2 + 4, _contract_y(i) + 1.1, code, size=6.5, bold=True)


def _procedure(sh):
    sheet = WORDS.fields("Sheet 3")
    E.header(sh, PAGE_ID, sheet["title"], sheet["subtitle"], part="3/4")
    E.spine(sh, mechanical=True)
    left = ts.section(WORDS, "You need", ts.bullets)
    for name in ("1 · Wraps", "2 · Build the test book", "3 · Measuring a link"):
        left += ts.section(WORDS, name, ts.steps)
    right = []
    for name in ("4 · The spine contract chain", "5 · Flex cycles", "6 · Repair"):
        right += ts.section(WORDS, name, ts.steps)
    right += ts.section(WORDS, "Pass or fail", ts.bullets)
    _flow(sh, left, right, "sheet 3")
    E.footer(sh, f"{PAGE_ID} {sheet['footer']}")


def _results(sh):
    sheet = WORDS.fields("Sheet 4")
    E.header(sh, PAGE_ID, sheet["title"], sheet["subtitle"], part="4/4")
    E.spine(sh, mechanical=True, show_labels=False)
    words = WORDS.fields("Results")
    h, note = ts.H, ts.NOTE
    wraps = [["", words["new"], words["handled"], words["cracks"]]] + [[w[0], "", "", ""] for w in WRAPS]
    chain = [["", words["first"], words["second"]]] + [[words[key], "", ""] for key in CONTRACT_RESULTS]
    left = [Paragraph(words["wraps"], h), ts.table(wraps, [16, 20, 20, 24], 6.5)]
    left += [Paragraph(words["chain"], h), Paragraph(words["current"], note), ts.table(chain, [30, 25, 25], 6.5)]
    left += ts.section(
        WORDS,
        "Results for the standard",
        lambda questions: [ts.decision_table(questions, widths=(52, 28), row_height=8.0)],
    )
    right = []
    for title in (words["links_1"], words["links_2"]):
        table = [["", *LINK_COLUMNS, words["flicker"]]] + [[code, "", "", "", "", "", ""] for code, _, _ in LINKS]
        right += [Paragraph(title, h), ts.table(table, [11, 10, 10, 11, 11, 13, 14], 6.2)]
    _flow(sh, left, right, "sheet 4")
    E.footer(sh, f"{PAGE_ID} {sheet['footer']}")


def _flow(sh, left, right, name):
    rest = sh.flow([(S.ZONE_BUILD[0], 27.0, 115.0, 282.0)], left) + sh.flow(
        [(121.0, 27.0, S.ZONE_BUILD[2], 282.0)], right
    )
    if rest:
        raise RuntimeError(f"T4 {name} overflowed by {len(rest)} items")
