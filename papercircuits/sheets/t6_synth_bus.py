"""T6: two-sided synth bus proof using the M3 controller and M6 filter.

Side A adapts M3's pencil ribbon: V+ feeds the ribbon through 13 kΩ and its wiper
drives BUS A. Side B adapts M6's pencil filter: BUS B is the audio input, the wiper
selects how much pencil resistance precedes the output, and 47 nF shunts high-frequency
content to GND. The two buses carry real control and audio signals; neither is a power
return and neither is duplicated across the opposite face.
"""

from reportlab.platypus import Paragraph

from .. import elements as E
from .. import schematic as sch
from .. import standard as S
from .. import testsheet as ts
from ..circuit import PENCIL, WIRE, C, Circuit, R
from ..draw import MUTED, Sheet, style
from ..placement import Placement
from ..words import Words

PAGE_ID = "T6"
WORDS = Words.beside(__file__)

SIDE_A = Circuit(
    R("R1", 13e3, "V+", "RIBBON"),
    PENCIL("Ribbon", track="RIBBON", wiper="BUS A", note="6B pencil"),
    controller=True,
    controller_outputs=("BUS A",),
)
SIDE_B = Circuit(
    PENCIL("Track", track="TRACK", wiper="BUS B", note="6B pencil"),
    WIRE("W1", "OUT", "TRACK"),
    C("C1", 47e-9, "OUT", "GND"),
)

AXIS_START = S.HOLE_X - S.TAPE_W / 2
V_PLUS_Y, BUS_A_Y, BUS_B_Y, GND_Y = 29.0, 133.0, 164.0, 274.0
SPINE_WRAP_X = 4.0
POWER_RAIL_END_X = 200.0

A_RIBBON = (54.0, 70.0, 178.0, 90.0)
A_WIPER = (106.0, 198.0, 122.0, 258.0)
A_WIPER_STRIP = 48.0

B_TRACK = (54.0, 190.0, 172.0, 210.0)
B_WIPER = (42.0, 78.0, 58.0, 126.0)
B_WIPER_STRIP = 32.0
B_OUT_X = 180.0


def build(path):
    sh = Sheet(path, WORDS.text("PDF title"))
    _side_a(sh)
    sh.next_page(mirrored=True)
    _side_b(sh)
    sh.next_page()
    _procedure(sh)
    sh.next_page()
    _results(sh)
    sh.save()


def _power_rails(lay, face):
    v_plus = lay.lane("V+", [(SPINE_WRAP_X, V_PLUS_Y), (POWER_RAIL_END_X, V_PLUS_Y)])
    gnd = lay.lane(
        "GND",
        [(SPINE_WRAP_X, GND_Y), (POWER_RAIL_END_X, GND_Y)],
        width=S.WIDE_TAPE_W,
    )
    E.wrap_arrow(lay.sh, SPINE_WRAP_X, V_PLUS_Y, "left")
    E.wrap_arrow(lay.sh, SPINE_WRAP_X, GND_Y, "left")
    E.test_point(lay.sh, 48, V_PLUS_Y, f"V+ {face}", side="below", size=6)
    E.test_point(lay.sh, 48, GND_Y, f"GND {face}", side="above", size=6)
    return v_plus, gnd


def _side_a(sh):
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, part="1/4", status=WORDS.text("Status"))
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    lay = Placement(sh, SIDE_A)
    _power_rails(lay, "A")
    lay.lane("BUS A", [(AXIS_START, BUS_A_Y), (200.0, BUS_A_Y)])
    lay.pencil("Ribbon", *A_RIBBON, last_number=120)
    sh.text(A_RIBBON[0], A_RIBBON[3] + 8, "low", size=6.5, bold=True, color=MUTED)
    sh.text(A_RIBBON[2], A_RIBBON[3] + 8, "high", size=6.5, bold=True, color=MUTED, align="right")
    _wiper_ghost(sh, 130.0, A_RIBBON[3], BUS_A_Y, A_WIPER_STRIP)
    lead = (A_RIBBON[1] - (V_PLUS_Y + S.TAPE_W / 2)) / 2
    lay.resistor("R1", 172.0, A_RIBBON[1] - lead, vertical=True, lead=lead, label="value")
    lay.loop("BUS A", 62.0, BUS_A_Y, side="above")
    lay.wiper("Ribbon", *A_WIPER, A_WIPER_STRIP, label="BUS A wiper")
    _side_a_schematic(sh, lay)
    words = WORDS.fields("Side A")
    sh.text(132, 190, words["title"], size=9, bold=True)
    sh.paragraph(132, 195, 65, words["body"], style(6.5, leading=8.2, color=MUTED))
    E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=170)
    lay.check(listed={"R1"})


def _side_b(sh):
    words = WORDS.fields("Side B")
    with sh.unmirrored():
        E.header(sh, PAGE_ID, words["page_title"], words["subtitle"], part="2/4")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    lay = Placement(sh, SIDE_B)
    _power_rails(lay, "B")
    lay.lane("BUS B", [(AXIS_START, BUS_B_Y), (200.0, BUS_B_Y)])
    lay.pencil("Track", *B_TRACK, last_number=110)
    sh.text(B_TRACK[0], B_TRACK[3] + 8, "soft", size=6.5, bold=True, color=MUTED)
    sh.text(B_TRACK[2], B_TRACK[3] + 8, "bright", size=6.5, bold=True, color=MUTED, align="right")
    _wiper_ghost(sh, 120.0, BUS_B_Y, B_TRACK[1], B_WIPER_STRIP)
    lay.lane("OUT", [(B_OUT_X, 200.0), (B_OUT_X, 250.0)])
    lay.wire("W1", (B_OUT_X, 200.0), (B_TRACK[2] - 5, 200.0))
    lay.ceramic_cap("C1", B_OUT_X, 259.0, vertical=True, lead=9.0, label="value")
    lay.loop("BUS B", 62.0, BUS_B_Y, side="above")
    lay.loop("OUT", B_OUT_X, 232.0, side="left")
    lay.wiper("Track", *B_WIPER, B_WIPER_STRIP, label="BUS B wiper")
    _side_b_schematic(sh, lay)
    sh.text(132, 78, words["title"], size=9, bold=True)
    sh.paragraph(132, 83, 65, words["body"], style(6.5, leading=8.2, color=MUTED))
    with sh.unmirrored():
        E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=170)
    lay.check(listed={"C1"})


def _wiper_ghost(sh, x, upper, lower, length):
    mid, half = (upper + lower) / 2, S.TAPE_W / 2
    sh.rect(x - half, mid - length / 2, x + half, mid + length / 2, stroke=MUTED, width=0.3, dash=(0.8, 0.8))
    sh.text(x + 4, mid, "wiper", size=6, color=MUTED)


def _side_a_schematic(sh, lay):
    sh.text(34, 184, "Controller schematic", size=8, bold=True)
    x, top, box = 76.0, 202.0, (224.0, 252.0)
    sch.terminal(sh, 42, top, "V+", label_y=top - 3.4)
    sch.wire(sh, [(42.8, top), (x, top)])
    r1 = lay.symbol("R1")
    sch.resistor(sh, x, top, box[0], r1.ref, r1.text)
    ribbon = lay.symbol("Ribbon")
    sch.rheostat(sh, x, *box, 238.0, 42.8, ribbon.ref, ribbon.text, open_end="bottom")
    sch.terminal(sh, 42, 238.0, "BUS A", label_y=243.0)


def _side_b_schematic(sh, lay):
    sh.text(72, 74, "Filter schematic", size=8, bold=True)
    x, term_x, box, node, gnd = 108.0, 76.0, (88.0, 116.0), 132.0, 148.0
    sch.terminal(sh, term_x, 102.0, "BUS B", label_y=98.5)
    track = lay.symbol("Track")
    sch.rheostat(sh, x, *box, 102.0, term_x + 0.8, track.ref, track.text)
    lay.symbol("W1")
    sch.wire(sh, [(x, box[1]), (x, node), (129.2, node)])
    sch.terminal(sh, 130.0, node, "OUT", label_y=node - 3.5, align="right")
    c1 = lay.symbol("C1")
    sch.capacitor(sh, x, node, gnd, c1.ref, c1.text, polarised=False)
    sch.wire(sh, [(76.8, gnd), (x, gnd)])
    sch.terminal(sh, 76.0, gnd, "GND", label_y=gnd + 5)


def _procedure(sh):
    words = WORDS.fields("Sheet 3")
    E.header(sh, PAGE_ID, words["title"], words["subtitle"], part="3/4")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    left = ts.section(WORDS, "You need", ts.bullets)
    for name in ("1 · Print and lay power", "2 · Build side A", "3 · Build side B"):
        left += ts.section(WORDS, name, ts.steps)
    right = []
    for name in ("4 · Patch the synth", "5 · Test the buses", "6 · Flex and inspect"):
        right += ts.section(WORDS, name, ts.steps)
    right += ts.section(WORDS, "Pass or fail", ts.bullets)
    _flow(sh, left, right, "sheet 3")
    E.footer(sh, f"{PAGE_ID} {words['footer']}")


def _results(sh):
    words = WORDS.fields("Results")
    E.header(sh, PAGE_ID, words["title"], words["subtitle"], part="4/4")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES, show_labels=False)
    h, note = ts.H, ts.NOTE
    continuity = [["", words["new"], words["cycles"]], ["V+ A-B", "", ""], ["GND A-B", "", ""]]
    signals = [["Test", "Before", "After"], ["BUS A pitch glide", "", ""], ["BUS B tone sweep", "", ""]]
    left = [Paragraph(words["continuity"], h), Paragraph(words["continuity_note"], note)]
    left += [ts.table(continuity, [30, 25, 25], 10)]
    left += [Paragraph(words["signals"], h), ts.table(signals, [38, 21, 21], 12)]
    right = ts.section(
        WORDS,
        "Bus decision",
        lambda rows: [ts.decision_table(rows, widths=(52, 28), row_height=11)],
    )
    right += ts.section(WORDS, "Notes", lambda rows: [ts.decision_table(rows, widths=(52, 28), row_height=17)])
    _flow(sh, left, right, "sheet 4")
    E.footer(sh, f"{PAGE_ID} {words['footer']}")


def _flow(sh, left, right, name):
    rest = sh.flow([(S.ZONE_BUILD[0], 27.0, 115.0, 282.0)], left) + sh.flow(
        [(121.0, 27.0, S.ZONE_BUILD[2], 282.0)], right
    )
    if rest:
        raise RuntimeError(f"T6 {name} overflowed by {len(rest)} items")
