"""What every table-top module page (M series, standard §10) shares: the power ring with
its two edge connectors, and the page layout around it."""

from reportlab.platypus import Paragraph

from . import elements as E
from . import lesson
from . import standard as S
from .draw import COPPER, MUTED, style

RING_INSIDE = (S.RING_LEFT[1] + S.TAPE_W / 2 + S.NET_CLEARANCE, S.RING_TOP + S.TAPE_W / 2 + S.NET_CLEARANCE,
               S.RING_RIGHT[1] - S.TAPE_W / 2 - S.NET_CLEARANCE, S.RING_BOTTOM - S.TAPE_W / 2 - S.NET_CLEARANCE)


def power_ring(sh):
    """Both edge connectors and the ring between them. V+ climbs from the left V+ pad, runs
    along the top and comes down to the right V+ pad; GND does the same round the bottom.
    Returns the two lanes' ids."""
    lv, lg = S.RING_LEFT
    rv, rg = S.RING_RIGHT
    v = E.lane(sh, [(S.EDGE_LEFT_X, S.EDGE_V_Y), (lv, S.EDGE_V_Y), (lv, S.RING_TOP), (rv, S.RING_TOP),
                    (rv, S.EDGE_V_Y), (S.EDGE_RIGHT_X, S.EDGE_V_Y)])
    g = E.lane(sh, [(S.EDGE_LEFT_X, S.EDGE_GND_Y), (lg, S.EDGE_GND_Y), (lg, S.RING_BOTTOM), (rg, S.RING_BOTTOM),
                    (rg, S.EDGE_GND_Y), (S.EDGE_RIGHT_X, S.EDGE_GND_Y)])
    for x, align in ((S.EDGE_LEFT_X + 1, "left"), (S.EDGE_RIGHT_X - 1, "right")):
        sh.text(x, S.EDGE_V_Y - S.TAPE_W / 2 - 1.2, "V+", size=6, bold=True, color=COPPER, align=align)
        sh.text(x, S.EDGE_GND_Y + S.TAPE_W / 2 + 3.4, "GND", size=6, bold=True, color=COPPER, align=align)
    return v, g


def need(sh, page_id, first, second):
    """The You need list in the band above the ring, in two columns of up to three items."""
    h = style(8.5, bold=True, spaceAfter=1.2)
    heading_h = (h.leading + h.spaceAfter) / 72 * 25.4
    left = [Paragraph("You need", h)] + lesson.items(first, numbered=False, space_after=0.4)
    right = lesson.items(second, numbered=False, space_after=0.4)
    rest = sh.flow([(46.0, 25.0, 108.0, 42.5)], left) + sh.flow([(112.0, 25.0 + heading_h, 170.0, 42.5)], right)
    if rest:
        raise RuntimeError(f"{page_id} parts list overflowed by {len(rest)} items")


def steps(sh, page_id, build, play, note=None):
    """Build it and Play it in the steps zone, under the ring, with the tag note."""
    x0, y0, x1, y1 = S.ZONE_WORKBOOK
    story = [Paragraph("Build it", lesson.HEADING)] + lesson.items(build, numbered=True)
    story += [Paragraph("Play it", style(8.5, bold=True, spaceBefore=3, spaceAfter=1.5))]
    story += lesson.items(play, numbered=False)
    story.append(lesson.tag_note(note) if note else lesson.tag_note())
    rest = sh.flow([(x0, y0, x1, y1)], story)
    if rest:
        raise RuntimeError(f"{page_id} steps overflowed by {len(rest)} items")


def caption(sh, text):
    """One muted line just under the ring, saying what the page does on the table."""
    sh.text(S.ZONE_BUILD[0], S.RING_BOTTOM + S.TAPE_W / 2 + 8, text, size=6.5, color=MUTED)

