"""T5: validate the proposed V2 dual-sided page format.

The power rails have fixed vertical homes and wrap between faces: V+ below the header
and a wide GND rail at the bottom. One resistor-and-LED load on each face validates the
two power wraps without pretending that a signal bus is a power return.
"""

from reportlab.platypus import Paragraph

from .. import elements as E
from .. import standard as S
from .. import testsheet as ts
from ..draw import MUTED, Sheet, style
from ..words import Words

PAGE_ID = "T5"
WORDS = Words.beside(__file__)

AXIS_START = S.HOLE_X - S.TAPE_W / 2
V_PLUS_Y = 29.0
GND_Y = 274.0
TOP_BOTTOM_WRAP_X = 184.0


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


def _rails(sh, face):
    rails = {
        "V+": E.lane(
            sh,
            [(AXIS_START, V_PLUS_Y), (TOP_BOTTOM_WRAP_X, V_PLUS_Y), (TOP_BOTTOM_WRAP_X, 4.0)],
        ),
        "GND": E.lane(
            sh,
            [(AXIS_START, GND_Y), (TOP_BOTTOM_WRAP_X, GND_Y), (TOP_BOTTOM_WRAP_X, 293.0)],
            width=S.WIDE_TAPE_W,
        ),
    }
    E.wrap_arrow(sh, TOP_BOTTOM_WRAP_X, 4.0, "up")
    E.wrap_arrow(sh, TOP_BOTTOM_WRAP_X, 293.0, "down")
    labels = WORDS.fields("Rail labels")
    for net, y in (("V+", V_PLUS_Y), ("GND", GND_Y)):
        sh.text(56, y - (4.0 if net != "GND" else 7.5), labels[net], size=7, bold=True)
    E.test_point(sh, 48, V_PLUS_Y, f"V+ {face}", side="below", size=6)
    E.test_point(sh, 48, GND_Y, f"GND {face}", side="above", size=6)
    return rails


def _load(sh, rails, *, x, top_net, bottom_net, resistor_y, led_y, ref):
    """A resistor and LED between two of the fixed rails."""
    rail_y = {"V+": V_PLUS_Y, "GND": GND_Y}
    top_y, bottom_y = rail_y[top_net], rail_y[bottom_net]
    first = E.lane(sh, [(x, top_y), (x, resistor_y - 12)])
    E.lane(sh, [(x, resistor_y + 12), (x, led_y - 12)])
    last = E.lane(sh, [(x, led_y + 9), (x, bottom_y)])
    sh.allow(rails[top_net], first, 0)
    sh.allow(rails[bottom_net], last, 0)
    E.resistor(sh, x, resistor_y, vertical=True, lead=12, label=f"{ref} · 1 kΩ")
    E.led(sh, x, led_y, anode="up", lead_anode=12, lead_cathode=9, label=f"LED{ref[-1]}")


def _front(sh):
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, part="1/4", status=WORDS.text("Status"))
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    rails = _rails(sh, "A")
    _load(sh, rails, x=120, top_net="V+", bottom_net="GND", resistor_y=90, led_y=190, ref="R1")
    words = WORDS.fields("Side A")
    sh.text(138, 84, words["load_title"], size=9, bold=True)
    sh.paragraph(138, 88, 58, words["load_body"], style(6.5, leading=8.2, color=MUTED))
    sh.text(138, 224, words["rule_title"], size=9, bold=True)
    sh.paragraph(138, 228, 58, words["rule_body"], style(6.5, leading=8.2, color=MUTED))
    E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=170)


def _back(sh):
    words = WORDS.fields("Side B")
    with sh.unmirrored():
        E.header(sh, PAGE_ID, words["title"], words["subtitle"], part="2/4")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    rails = _rails(sh, "B")
    _load(sh, rails, x=120, top_net="V+", bottom_net="GND", resistor_y=90, led_y=190, ref="R2")
    sh.text(138, 84, words["load_title"], size=9, bold=True)
    sh.paragraph(138, 88, 58, words["load_body"], style(6.5, leading=8.2, color=MUTED))
    sh.text(138, 58, words["wrap_title"], size=9, bold=True)
    sh.paragraph(138, 62, 58, words["wrap_body"], style(6.5, leading=8.2, color=MUTED))
    with sh.unmirrored():
        E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=170)


def _procedure(sh):
    words = WORDS.fields("Sheet 3")
    E.header(sh, PAGE_ID, words["title"], words["subtitle"], part="3/4")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    left = ts.section(WORDS, "You need", ts.bullets)
    for name in ("1 · Print and inspect", "2 · Lay the power rails", "3 · Add the loads"):
        left += ts.section(WORDS, name, ts.steps)
    right = []
    for name in ("4 · Continuity before power", "5 · Powered proof", "6 · Flex and inspect"):
        right += ts.section(WORDS, name, ts.steps)
    right += ts.section(WORDS, "Pass or fail", ts.bullets)
    _flow(sh, left, right, "sheet 3")
    E.footer(sh, f"{PAGE_ID} {words['footer']}")


def _results(sh):
    words = WORDS.fields("Results")
    E.header(sh, PAGE_ID, words["title"], words["subtitle"], part="4/4")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES, show_labels=False)
    h, note = ts.H, ts.NOTE
    rail_rows = [["", words["new"], words["cycles_100"], words["cycles_1000"]]]
    rail_rows += [[net, "", "", ""] for net in ("V+ A-B", "GND A-B")]
    power_rows = [["", words["before"], words["after"]], ["LED1 / side A", "", ""], ["LED2 / side B", "", ""]]
    left = [Paragraph(words["continuity"], h), Paragraph(words["continuity_note"], note)]
    left += [ts.table(rail_rows, [20, 20, 20, 20], 8)]
    left += [Paragraph(words["powered"], h), ts.table(power_rows, [36, 22, 22], 9)]
    right = ts.section(
        WORDS,
        "Format decision",
        lambda questions: [ts.decision_table(questions, widths=(52, 28), row_height=10)],
    )
    right += ts.section(
        WORDS,
        "Notes",
        lambda prompts: [ts.decision_table(prompts, widths=(52, 28), row_height=16)],
    )
    _flow(sh, left, right, "sheet 4")
    E.footer(sh, f"{PAGE_ID} {words['footer']}")


def _flow(sh, left, right, name):
    rest = sh.flow([(S.ZONE_BUILD[0], 27.0, 115.0, 282.0)], left) + sh.flow(
        [(121.0, 27.0, S.ZONE_BUILD[2], 282.0)], right
    )
    if rest:
        raise RuntimeError(f"T5 {name} overflowed by {len(rest)} items")
