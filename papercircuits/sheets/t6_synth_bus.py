"""T6: a three-card V2 synth that proves signals cross real page boundaries.

Card 1 adapts M3 and drives BUS A. Card 2 adapts M1: its side-A oscillator reads BUS A,
then its OUT trace wraps at the spine and becomes BUS B on side B. Card 3 adapts M6 and
reads BUS B. The opposite face of each card has only a short spine stub for the other
bus, so BUS A never crosses a side-B work area and BUS B never crosses a side-A work area.
"""

from reportlab.platypus import Paragraph

from .. import elements as E
from .. import schematic as sch
from .. import standard as S
from .. import testsheet as ts
from ..circuit import LED, PENCIL, WIRE, C, Circuit, Q, R
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
OSCILLATOR = Circuit(
    R("R1", 1e3, "V+", "N1"),
    LED("LED1", anode="N1", cathode="Q1C", note="red, 5 mm"),
    R("R2", 1e3, "V+", "OUT"),
    R("R3", 10e3, "V+", "Q1B"),
    R("R4", 4.7e3, "PITCH", "Q2B"),
    C("C1", 100e-9, "Q1C", "Q2B"),
    C("C2", 100e-9, "Q1B", "OUT"),
    Q("Q1", "2N3904", e="GND", b="Q1B", c="Q1C"),
    Q("Q2", "2N3904", e="GND", b="Q2B", c="OUT"),
)

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
    _controller_a(sh)
    sh.next_page(mirrored=True)
    _controller_b(sh)
    sh.next_page()
    _oscillator_a(sh)
    sh.next_page(mirrored=True)
    _oscillator_b(sh)
    sh.next_page()
    _filter_a(sh)
    sh.next_page(mirrored=True)
    _filter_b(sh)
    sh.next_page()
    _procedure(sh)
    sh.next_page()
    _results(sh)
    sh.save()


def _rails(target, face, *, bus_a=None, bus_b=None, full_a=False, full_b=False, label_b=True):
    """Draw one face of the four-rail contract.

    A bus occupies the work area only on its named face. On the opposite face it stops
    at x=26 mm, leaving just enough copper for the spine wrap and inter-page link.
    """
    sh = target.sh if isinstance(target, Placement) else target

    def lane(net, pts, **kw):
        return target.lane(net, pts, **kw) if isinstance(target, Placement) and net else E.lane(sh, pts, **kw)

    lanes = {
        "v_plus": lane("V+", [(SPINE_WRAP_X, V_PLUS_Y), (POWER_RAIL_END_X, V_PLUS_Y)]),
        "gnd": lane("GND", [(SPINE_WRAP_X, GND_Y), (POWER_RAIL_END_X, GND_Y)], width=S.WIDE_TAPE_W),
        "bus_a": lane(bus_a, [(SPINE_WRAP_X, BUS_A_Y), (POWER_RAIL_END_X if full_a else 26.0, BUS_A_Y)]),
        "bus_b": lane(bus_b, [(SPINE_WRAP_X, BUS_B_Y), (POWER_RAIL_END_X if full_b else 26.0, BUS_B_Y)]),
    }
    for y in (V_PLUS_Y, BUS_A_Y, BUS_B_Y, GND_Y):
        E.wrap_arrow(sh, SPINE_WRAP_X, y, "left")
    for net, y, side in (("V+", V_PLUS_Y, "below"), ("GND", GND_Y, "above")):
        E.test_point(sh, 48, y, f"{net} {face}", side=side, size=6)
    labels = (("BUS A", BUS_A_Y, full_a), ("BUS B", BUS_B_Y, full_b))
    for net, y, full in labels:
        if net == "BUS B" and not label_b:
            continue
        if full:
            sh.text(185, y - 4, f"{net} · work rail", size=6.5, bold=True, align="right")
        else:
            sh.text(18, y - 4, f"{net} · spine stub", size=6.5, bold=True)
    return lanes


def _controller_a(sh):
    words = WORDS.fields("Controller A")
    E.header(sh, PAGE_ID, words["title"], words["subtitle"], part="1/8", status=WORDS.text("Status"))
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    lay = Placement(sh, SIDE_A)
    _rails(lay, "A", bus_a="BUS A", full_a=True)
    lay.pencil("Ribbon", *A_RIBBON, last_number=120)
    sh.text(A_RIBBON[0], A_RIBBON[3] + 8, "low", size=6.5, bold=True, color=MUTED)
    sh.text(A_RIBBON[2], A_RIBBON[3] + 8, "high", size=6.5, bold=True, color=MUTED, align="right")
    _wiper_ghost(sh, 130.0, A_RIBBON[3], BUS_A_Y, A_WIPER_STRIP)
    lead = (A_RIBBON[1] - (V_PLUS_Y + S.TAPE_W / 2)) / 2
    lay.resistor("R1", 172.0, A_RIBBON[1] - lead, vertical=True, lead=lead, label="value")
    lay.loop("BUS A", 62.0, BUS_A_Y, side="above")
    lay.wiper("Ribbon", *A_WIPER, A_WIPER_STRIP, label="BUS A wiper")
    _side_a_schematic(sh, lay)
    sh.text(132, 190, words["title"], size=9, bold=True)
    sh.paragraph(132, 195, 65, words["body"], style(6.5, leading=8.2, color=MUTED))
    E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=168)
    lay.check(listed={"R1"})


def _controller_b(sh):
    words = WORDS.fields("Controller B")
    with sh.unmirrored():
        E.header(sh, PAGE_ID, words["page_title"], words["subtitle"], part="2/8")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    _rails(sh, "B", full_b=True)
    sh.text(58, 78, words["title"], size=11, bold=True)
    sh.paragraph(58, 84, 118, words["body"], style(7.2, leading=9.2, color=MUTED))
    with sh.unmirrored():
        E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=168)


def _oscillator_a(sh):
    words = WORDS.fields("Oscillator A")
    E.header(sh, PAGE_ID, words["page_title"], words["subtitle"], part="3/8")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    lay = Placement(sh, OSCILLATOR)
    rails = _rails(lay, "A", bus_a="PITCH", bus_b="OUT", full_a=True, label_b=False)
    _oscillator_copper(lay, rails)
    sh.text(88, 62, words["title"], size=9, bold=True)
    sh.paragraph(88, 67, 45, words["body"], style(6.2, leading=7.8, color=MUTED))
    E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=168)


def _oscillator_copper(lay, rails):
    sh = lay.sh
    lay.lane("N1", [(64.0, 55.0), (64.0, 60.0)])
    q1c = lay.lane("Q1C", [(64.0, 80.0), (64.0, 202.0)])
    q1b = lay.lane("Q1B", [(140.0, 55.0), (140.0, 205.0), (72.0, 205.0)])
    q2b = lay.lane("Q2B", [(80.0, 157.0), (80.0, 215.0), (143.0, 215.0)])
    out = lay.lane("OUT", [(155.0, 55.0), (155.0, 202.0), (170.0, 202.0), (170.0, BUS_B_Y), (26.0, BUS_B_Y)])
    for x, y in (
        (64.0, BUS_A_Y),
        (140.0, BUS_A_Y),
        (155.0, BUS_A_Y),
        (64.0, BUS_B_Y),
        (80.0, BUS_B_Y),
        (140.0, BUS_B_Y),
        (80.0, 205.0),
    ):
        E.crossing(sh, x, y, label=None)
    for lane_id in (q1c, q1b, out):
        sh.allow(rails["bus_a"], lane_id, 0)
    sh.allow(rails["bus_b"], out, 0)
    sh.allow(q1b, q2b, 0)
    for lane_id in (q1c, q1b):
        sh.allow(lane_id, out, 0)
    sh.allow(q2b, out, 0)
    r_top = 42.0
    lay.resistor("R1", 64.0, r_top, vertical=True, lead=13.0, label="value")
    lay.led("LED1", 64.0, 70.0, anode="up", lead_anode=10.0, lead_cathode=10.0, label="ref")
    lay.resistor("R2", 155.0, r_top, vertical=True, lead=13.0, label="value")
    lay.resistor("R3", 140.0, r_top, vertical=True, lead=13.0, label="value")
    lay.resistor("R4", 80.0, 145.0, vertical=True, lead=12.0, label="value")
    lay.ceramic_cap("C1", 72.0, 180.0, lead=8.0, label="value")
    lay.ceramic_cap("C2", 147.5, 110.0, lead=7.5, label="value")
    lay.transistor("Q1", 70.0, 210.0, {"E": (70.0, 268.0), "B": (72.0, 205.0), "C": (64.0, 202.0)}, label="ref")
    lay.transistor("Q2", 150.0, 220.0, {"E": (150.0, 268.0), "B": (143.0, 215.0), "C": (155.0, 202.0)}, label="ref")
    lay.loop("PITCH", 100.0, BUS_A_Y, side="above")
    lay.loop("OUT", 34.0, BUS_B_Y, side="above")
    sh.text(30, BUS_B_Y + 7, "OUT wraps to BUS B on side B", size=6.5, bold=True)


def _oscillator_b(sh):
    words = WORDS.fields("Oscillator B")
    with sh.unmirrored():
        E.header(sh, PAGE_ID, words["page_title"], words["subtitle"], part="4/8")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    _rails(sh, "B", full_b=True)
    sh.text(58, 78, words["title"], size=11, bold=True)
    sh.paragraph(58, 84, 118, words["body"], style(7.2, leading=9.2, color=MUTED))
    with sh.unmirrored():
        E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=168)


def _filter_a(sh):
    words = WORDS.fields("Filter A")
    E.header(sh, PAGE_ID, words["page_title"], words["subtitle"], part="5/8")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    _rails(sh, "A", full_a=True)
    sh.text(58, 78, words["title"], size=11, bold=True)
    sh.paragraph(58, 84, 118, words["body"], style(7.2, leading=9.2, color=MUTED))
    E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=168)


def _filter_b(sh):
    words = WORDS.fields("Filter B")
    with sh.unmirrored():
        E.header(sh, PAGE_ID, words["page_title"], words["subtitle"], part="6/8")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    lay = Placement(sh, SIDE_B)
    _rails(lay, "B", bus_b="BUS B", full_b=True)
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
        E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=168)
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
    words = WORDS.fields("Sheet 7")
    E.header(sh, PAGE_ID, words["title"], words["subtitle"], part="7/8")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    left = ts.section(WORDS, "You need", ts.bullets)
    for name in ("1 · Print the three cards", "2 · Build card 1", "3 · Build card 2"):
        left += ts.section(WORDS, name, ts.steps)
    right = []
    for name in ("4 · Build card 3", "5 · Link and test the book", "6 · Flex and inspect"):
        right += ts.section(WORDS, name, ts.steps)
    right += ts.section(WORDS, "Pass or fail", ts.bullets)
    _flow(sh, left, right, "sheet 7")
    E.footer(sh, f"{PAGE_ID} {words['footer']}")


def _results(sh):
    words = WORDS.fields("Results")
    E.header(sh, PAGE_ID, words["title"], words["subtitle"], part="8/8")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES, show_labels=False)
    h, note = ts.H, ts.NOTE
    continuity = [["", words["new"], words["cycles"]]]
    continuity += [[name, "", ""] for name in ("V+ links", "GND links", "BUS A links", "BUS B links")]
    signals = [["Test", "Before", "After"], ["BUS A pitch glide", "", ""], ["BUS B tone sweep", "", ""]]
    left = [Paragraph(words["continuity"], h), Paragraph(words["continuity_note"], note)]
    left += [ts.table(continuity, [30, 25, 25], 8)]
    left += [Paragraph(words["signals"], h), ts.table(signals, [38, 21, 21], 12)]
    right = ts.section(
        WORDS,
        "Bus decision",
        lambda rows: [ts.decision_table(rows, widths=(52, 28), row_height=11)],
    )
    right += ts.section(WORDS, "Notes", lambda rows: [ts.decision_table(rows, widths=(52, 28), row_height=17)])
    _flow(sh, left, right, "sheet 8")
    E.footer(sh, f"{PAGE_ID} {words['footer']}")


def _flow(sh, left, right, name):
    rest = sh.flow([(S.ZONE_BUILD[0], 27.0, 115.0, 282.0)], left) + sh.flow(
        [(121.0, 27.0, S.ZONE_BUILD[2], 282.0)], right
    )
    if rest:
        raise RuntimeError(f"T6 {name} overflowed by {len(rest)} items")
