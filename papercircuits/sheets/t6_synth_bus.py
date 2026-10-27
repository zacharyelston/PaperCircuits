"""T6: a four-card, self-contained V2 synth book.

Power enters card 1. Card 2 drives BUS A, card 3 reads BUS A and drives BUS B through a
1 kΩ protection resistor, and card 4 filters BUS B and makes a line-level output. Each
bus occupies only its named face; all four nets use explicit, testable spine links.
"""

from reportlab.platypus import Paragraph

from .. import elements as E
from .. import schematic as sch
from .. import standard as S
from .. import testsheet as ts
from ..circuit import LED, PENCIL, WIRE, C, Circuit, Q, R
from ..draw import COPPER, COPPER_TINT, MUTED, Sheet, style
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
    WIRE("W1", "FILTER", "TRACK"),
    C("C1", 47e-9, "FILTER", "GND"),
    R("R1", 22e3, "FILTER", "MIX"),
    C("C2", 1e-6, "MIX", "LINE"),
    R("R2", 4.7e3, "LINE", "GND"),
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
    R("R5", 1e3, "OUT", "BUS B"),
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
    _power_a(sh)
    sh.next_page(mirrored=True)
    _power_b(sh)
    sh.next_page()
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
    direction = "TO PREVIOUS CARD" if face == "A" else "TO NEXT CARD"
    sh.text(30, 112, f"SPINE LINKS · {direction}", size=6.2, bold=True, color=MUTED)
    for net, y in (("V+", V_PLUS_Y), ("BUS A", BUS_A_Y), ("BUS B", BUS_B_Y), ("GND", GND_Y)):
        E.test_point(sh, 18, y, net, side="right", size=5.5)
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


def _power_a(sh):
    words = WORDS.fields("Power A")
    E.header(sh, PAGE_ID, words["title"], words["subtitle"], part="1/10", status=WORDS.text("Status"))
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    # The switched holder feeds BAT+; F1 is the only path from BAT+ into the book's V+.
    E.lane(sh, [(SPINE_WRAP_X, V_PLUS_Y), (104.0, V_PLUS_Y)])
    E.lane(sh, [(136.0, V_PLUS_Y), (POWER_RAIL_END_X, V_PLUS_Y)])
    gnd = E.lane(sh, [(SPINE_WRAP_X, GND_Y), (POWER_RAIL_END_X, GND_Y)], width=S.WIDE_TAPE_W)
    bus_a = E.lane(sh, [(SPINE_WRAP_X, BUS_A_Y), (POWER_RAIL_END_X, BUS_A_Y)])
    E.lane(sh, [(SPINE_WRAP_X, BUS_B_Y), (26.0, BUS_B_Y)])
    for y in (V_PLUS_Y, BUS_A_Y, BUS_B_Y, GND_Y):
        E.wrap_arrow(sh, SPINE_WRAP_X, y, "left")
    for net, y in (("V+", V_PLUS_Y), ("BUS A", BUS_A_Y), ("BUS B", BUS_B_Y), ("GND", GND_Y)):
        E.test_point(sh, 18, y, net, side="right", size=5.5)
    sh.text(30, 112, "SPINE LINKS · TO NEXT CARD", size=6.2, bold=True, color=MUTED)
    E.ptc(sh, 120.0, V_PLUS_Y, lead=16.0, label="F1 · 0.1 A resettable fuse")
    sh.text(172, 35, "BAT+ from switched 3×AA holder", size=6.2, bold=True, align="center")
    E.test_point(sh, 184.0, V_PLUS_Y, "RED", side="above", size=5.5)
    E.test_point(sh, 170.0, GND_Y, "BLACK", side="above", size=5.5)
    E.battery_holder(sh, 132.0, 62.0, cells=3, label="BT1 · switched 3×AA holder")
    sh.line(132, 72, 150, 72, width=0.5, color=MUTED)
    sh.text(151, 73, "red → BAT+", size=6.2, color=MUTED)
    sh.line(132, 96, 150, 96, width=0.5, color=MUTED)
    sh.text(151, 97, "black → GND", size=6.2, color=MUTED)
    indicator_return = E.lane(sh, [(72.0, 81.0), (72.0, GND_Y)])
    sh.allow(indicator_return, bus_a, 0)
    sh.allow(indicator_return, gnd, 0)
    E.crossing(sh, 72.0, BUS_A_Y, label=None)
    sh.rect(
        72.0 - S.TAPE_W / 2,
        BUS_A_Y - 4.2,
        72.0 + S.TAPE_W / 2,
        BUS_A_Y + 4.2,
        stroke=COPPER,
        fill=COPPER_TINT,
        width=0.25,
        dash=(1.2, 0.8),
    )
    E.resistor(sh, 72.0, 44.0, vertical=True, lead=13.0, label="R1 · 1 kΩ")
    E.led(sh, 72.0, 69.0, anode="up", lead_anode=12.0, lead_cathode=12.0, label="LED1 · POWER")
    sh.paragraph(44, 101, 94, words["body"], style(6.5, leading=8, color=MUTED))
    E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=168)


def _power_b(sh):
    words = WORDS.fields("Power B")
    with sh.unmirrored():
        E.header(sh, PAGE_ID, words["title"], words["subtitle"], part="2/10")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    _rails(sh, "B", full_b=True)
    with sh.unmirrored():
        _book_map(sh)
        sh.paragraph(48, 218, 126, words["body"], style(7, leading=9, color=MUTED))
        E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=168)


def _book_map(sh):
    sh.text(107, 62, "T6 BOOK CONNECTION MAP", size=9, bold=True, align="center")
    labels = (("1", "POWER"), ("2", "BUS A\nCONTROL"), ("3", "OSCILLATOR\nA→B"), ("4", "FILTER +\nLINE OUT"))
    for i, (number, label) in enumerate(labels):
        x0 = 42 + i * 35
        sh.rect(x0, 78, x0 + 27, 105, stroke=COPPER, fill=COPPER_TINT, width=0.4, radius=1.5)
        sh.text(x0 + 13.5, 85, number, size=9, bold=True, align="center")
        for j, line in enumerate(label.split("\n")):
            sh.text(x0 + 13.5, 94 + j * 6, line, size=5.8, bold=True, align="center")
        if i < len(labels) - 1:
            sh.line(x0 + 27, 91.5, x0 + 35, 91.5, width=0.7, color=COPPER)
            sh.text(x0 + 31, 88, "4 links", size=5, color=MUTED, align="center")
    sh.text(107, 116, "V+ · BUS A · BUS B · GND at every card boundary", size=6.4, bold=True, align="center")


def _controller_a(sh):
    words = WORDS.fields("Controller A")
    E.header(sh, PAGE_ID, words["title"], words["subtitle"], part="3/10", status=WORDS.text("Status"))
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
        E.header(sh, PAGE_ID, words["page_title"], words["subtitle"], part="4/10")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    _rails(sh, "B", full_b=True)
    sh.text(58, 78, words["title"], size=11, bold=True)
    sh.paragraph(58, 84, 118, words["body"], style(7.2, leading=9.2, color=MUTED))
    with sh.unmirrored():
        E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=168)


def _oscillator_a(sh):
    words = WORDS.fields("Oscillator A")
    E.header(sh, PAGE_ID, words["page_title"], words["subtitle"], part="5/10")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    lay = Placement(sh, OSCILLATOR)
    rails = _rails(lay, "A", bus_a="PITCH", bus_b="BUS B", full_a=True, label_b=False)
    _oscillator_copper(lay, rails)
    sh.text(88, 62, words["title"], size=9, bold=True)
    sh.paragraph(88, 67, 45, words["body"], style(6.2, leading=7.8, color=MUTED))
    E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=168)
    # The legible schematic is printed on the paired reverse face; bind its symbols to
    # this physical placement so connectivity and component coverage remain checked.
    for ref in OSCILLATOR.parts:
        lay.symbol(ref)
    lay.check(listed=set(OSCILLATOR.parts))


def _oscillator_copper(lay, rails):
    sh = lay.sh
    lay.lane("N1", [(64.0, 55.0), (64.0, 60.0)])
    q1c = lay.lane("Q1C", [(64.0, 80.0), (64.0, 202.0)])
    q1b = lay.lane("Q1B", [(140.0, 55.0), (140.0, 205.0), (72.0, 205.0)])
    q2b = lay.lane("Q2B", [(80.0, 157.0), (80.0, 215.0), (143.0, 215.0)])
    out = lay.lane("OUT", [(155.0, 55.0), (155.0, 202.0), (170.0, 202.0), (170.0, BUS_B_Y), (48.0, BUS_B_Y)])
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
    # Redraw the insulated conductor on top of each hatched crossing so the intended
    # over/under path is unambiguous when following tape through the crowded oscillator.
    for x, y in (
        (64.0, BUS_A_Y),
        (140.0, BUS_A_Y),
        (155.0, BUS_A_Y),
        (64.0, BUS_B_Y),
        (80.0, BUS_B_Y),
        (140.0, BUS_B_Y),
    ):
        sh.rect(
            x - 4.2,
            y - S.TAPE_W / 2,
            x + 4.2,
            y + S.TAPE_W / 2,
            stroke=COPPER,
            fill=COPPER_TINT,
            width=0.25,
            dash=(1.2, 0.8),
        )
    sh.rect(
        80.0 - S.TAPE_W / 2,
        200.8,
        80.0 + S.TAPE_W / 2,
        209.2,
        stroke=COPPER,
        fill=COPPER_TINT,
        width=0.25,
        dash=(1.2, 0.8),
    )
    sh.text(110, 190, "hatched bridge = insulated crossing", size=6, color=MUTED)
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
    lay.resistor("R5", 37.0, BUS_B_Y, vertical=False, lead=11.0, label="value")
    lay.ceramic_cap("C1", 72.0, 180.0, lead=8.0, label="value")
    lay.ceramic_cap("C2", 147.5, 110.0, lead=7.5, label="value")
    lay.transistor("Q1", 70.0, 210.0, {"E": (70.0, 268.0), "B": (72.0, 205.0), "C": (64.0, 202.0)}, label="ref")
    lay.transistor("Q2", 150.0, 220.0, {"E": (150.0, 268.0), "B": (143.0, 215.0), "C": (155.0, 202.0)}, label="ref")
    lay.loop("PITCH", 100.0, BUS_A_Y, side="above")
    lay.loop("BUS B", 18.0, BUS_B_Y, side="above")
    lay.loop("OUT", 54.0, BUS_B_Y, side="above")
    sh.text(30, BUS_B_Y + 7, "R5 protects BUS B; the spine wrap continues on side B", size=6.5, bold=True)


def _oscillator_b(sh):
    words = WORDS.fields("Oscillator B")
    with sh.unmirrored():
        E.header(sh, PAGE_ID, words["page_title"], words["subtitle"], part="6/10")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    _rails(sh, "B", full_b=True)
    sh.text(58, 70, words["title"], size=11, bold=True)
    sh.paragraph(58, 76, 118, words["body"], style(7.0, leading=8.8, color=MUTED))
    _oscillator_schematic(sh)
    with sh.unmirrored():
        E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=168)


def _oscillator_schematic(sh):
    """Compact functional schematic; the protected BUS B boundary is the key addition."""
    sh.text(108, 196, "Protected oscillator output", size=8, bold=True, align="center")
    sch.terminal(sh, 48, 220, "BUS A / PITCH", label_y=216.5)
    sh.rect(69, 207, 126, 240, stroke=MUTED, width=0.35, radius=1.5)
    sh.text(97.5, 220, "M1 ASTABLE", size=8, bold=True, align="center")
    sh.text(97.5, 230, "Q1 · Q2 · C1 · C2", size=6.2, color=MUTED, align="center")
    sch.wire(sh, [(48.8, 220), (69, 220), (126, 220)])
    sch.resistor_h(sh, 126, 158, 220, "R5", "1 kΩ", box_w=8)
    sch.wire(sh, [(158, 220), (176.2, 220)])
    sch.terminal(sh, 177, 220, "BUS B", label_y=216.5, align="right")
    sh.text(108, 248, "R5 limits a BUS B fault to less than 4.5 mA at 4.5 V.", size=6.2, color=MUTED, align="center")


def _filter_a(sh):
    words = WORDS.fields("Filter A")
    E.header(sh, PAGE_ID, words["page_title"], words["subtitle"], part="7/10")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    _rails(sh, "A", full_a=True)
    sh.text(58, 78, words["title"], size=11, bold=True)
    sh.paragraph(58, 84, 118, words["body"], style(7.2, leading=9.2, color=MUTED))
    E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=168)


def _filter_b(sh):
    words = WORDS.fields("Filter B")
    with sh.unmirrored():
        E.header(sh, PAGE_ID, words["page_title"], words["subtitle"], part="8/10")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    lay = Placement(sh, SIDE_B)
    _rails(lay, "B", bus_b="BUS B", full_b=True)
    lay.pencil("Track", *B_TRACK, last_number=110)
    sh.text(B_TRACK[0], B_TRACK[3] + 8, "soft", size=6.5, bold=True, color=MUTED)
    sh.text(B_TRACK[2], B_TRACK[3] + 8, "bright", size=6.5, bold=True, color=MUTED, align="right")
    _wiper_ghost(sh, 120.0, BUS_B_Y, B_TRACK[1], B_WIPER_STRIP)
    lay.lane("FILTER", [(B_OUT_X, 200.0), (B_OUT_X, 250.0)])
    lay.wire("W1", (B_OUT_X, 200.0), (B_TRACK[2] - 5, 200.0))
    lay.ceramic_cap("C1", B_OUT_X, 259.0, vertical=True, lead=9.0, label="value")
    lay.lane("MIX", [(150.0, 230.0), (150.0, 245.0)])
    lay.resistor("R1", 165.0, 230.0, vertical=False, lead=15.0, label="value")
    lay.lane("LINE", [(125.0, 245.0), (125.0, 251.0)])
    lay.ceramic_cap("C2", 137.5, 245.0, lead=12.5, label="value")
    lay.resistor("R2", 125.0, 259.5, vertical=True, lead=8.5, label="value")
    lay.loop("BUS B", 62.0, BUS_B_Y, side="above")
    lay.loop("LINE", 125.0, 248.0, side="left")
    lay.wiper("Track", *B_WIPER, B_WIPER_STRIP, label="BUS B wiper")
    _side_b_schematic(sh, lay)
    sh.text(132, 78, words["title"], size=9, bold=True)
    sh.paragraph(132, 83, 65, words["body"], style(6.5, leading=8.2, color=MUTED))
    with sh.unmirrored():
        E.footer(sh, f"{PAGE_ID} {words['footer']}", label_x=168)
    lay.check(listed=set(SIDE_B.parts))


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
    sh.text(72, 62, "Filter + line output schematic", size=8, bold=True)
    x, term_x, box, node, gnd = 108.0, 76.0, (76.0, 98.0), 110.0, 154.0
    sch.terminal(sh, term_x, 102.0, "BUS B", label_y=98.5)
    track = lay.symbol("Track")
    sch.rheostat(sh, x, *box, 102.0, term_x + 0.8, track.ref, track.text)
    lay.symbol("W1")
    sch.wire(sh, [(x, box[1]), (x, node)])
    r1 = lay.symbol("R1")
    sch.resistor_h(sh, x, 136.0, node, r1.ref, r1.text, box_w=7)
    c2 = lay.symbol("C2")
    sch.capacitor_h(sh, 136.0, 158.0, node, c2.ref, c2.text)
    sch.wire(sh, [(158.0, node), (172.2, node)])
    sch.terminal(sh, 173.0, node, "LINE", label_y=node - 3.5, align="right")
    c1 = lay.symbol("C1")
    sch.capacitor(sh, x, node, gnd, c1.ref, c1.text, polarised=False)
    r2 = lay.symbol("R2")
    sch.resistor(sh, 158.0, node, gnd, r2.ref, r2.text)
    sch.wire(sh, [(76.8, gnd), (158.0, gnd)])
    sch.terminal(sh, 76.0, gnd, "GND", label_y=gnd + 5)


def _procedure(sh):
    words = WORDS.fields("Sheet 7")
    E.header(sh, PAGE_ID, words["title"], words["subtitle"], part="9/10")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES)
    left = ts.section(WORDS, "You need", ts.bullets)
    for name in ("1 · Print the four cards", "2 · Build power and controller", "3 · Build oscillator"):
        left += ts.section(WORDS, name, ts.steps)
    right = []
    for name in ("4 · Build filter and output", "5 · Link and test the book", "6 · Flex and inspect"):
        right += ts.section(WORDS, name, ts.steps)
    right += ts.section(WORDS, "Pass or fail", ts.bullets)
    _flow(sh, left, right, "sheet 7")
    E.footer(sh, f"{PAGE_ID} {words['footer']}")


def _results(sh):
    words = WORDS.fields("Results")
    E.header(sh, PAGE_ID, words["title"], words["subtitle"], part="10/10")
    E.spine(sh, mechanical=True, holes=S.V2_HOLES, show_labels=False)
    h, note = ts.H, ts.NOTE
    continuity = [["Boundary / net", words["new"], words["cycles"]]]
    continuity += [
        [f"{boundary} · {net}", "", ""] for boundary in ("1–2", "2–3", "3–4") for net in ("V+", "BUS A", "BUS B", "GND")
    ]
    signals = [
        ["Bench measurement", "Idle", "Active"],
        ["BUS A voltage", "", ""],
        ["BUS B voltage", "", ""],
        ["Total current", "", ""],
        ["LINE output amplitude", "", ""],
    ]
    left = [Paragraph(words["continuity"], h), Paragraph(words["continuity_note"], note)]
    left += [ts.table(continuity, [36, 22, 22], 5.8)]
    left += [Paragraph(words["signals"], h), ts.table(signals, [40, 20, 20], 9)]
    right = ts.section(
        WORDS,
        "Bus decision",
        lambda rows: [_wrapped_decision(rows, row_height=11)],
    )
    right += ts.section(WORDS, "Notes", lambda rows: [_wrapped_decision(rows, row_height=17)])
    _flow(sh, left, right, "sheet 8")
    E.footer(sh, f"{PAGE_ID} {words['footer']}")


def _flow(sh, left, right, name):
    rest = sh.flow([(S.ZONE_BUILD[0], 27.0, 115.0, 282.0)], left) + sh.flow(
        [(121.0, 27.0, S.ZONE_BUILD[2], 282.0)], right
    )
    if rest:
        raise RuntimeError(f"T6 {name} overflowed by {len(rest)} items")


def _wrapped_decision(rows, row_height):
    cells = [[Paragraph(row, style(6.2, leading=7.2, bold=True)), ""] for row in rows]
    return ts.table(cells, [66, 14], row_height)
