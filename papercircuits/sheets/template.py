"""L00: the lesson-page template. Shows every zone, the backplane nets, the fold switch
and the drawing marks. Nothing on it is meant to be built.

Its words are in template.md."""

from .. import elements as E
from .. import standard as S
from ..draw import MUTED, Sheet
from ..words import Words

PAGE_ID = "L00"
WORDS = Words.beside(__file__)


def build(path):
    sh = Sheet(path, " ".join(WORDS.title.split()))
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle)
    labels = WORDS.fields("Labels")

    for hole_id in S.HOLES:
        E.net_strip(sh, hole_id, to_x=S.ZONE_BUILD[0] + 6)
    E.spine(sh, connected=S.HOLES, labels_below=("H4",), edge=True)
    sh.text(S.BUS_B_GUTTER_X - 3.5, 236, labels["gutter"], size=6, color=MUTED, align="right")

    x0, y0, x1, y1 = S.ZONE_BUILD
    sx0, _, _, sy1 = S.ZONE_SWITCH
    notch_x, notch_y = sx0 - 2, sy1 + 2
    sh.polygon([(x0, y0), (notch_x, y0), (notch_x, notch_y), (x1, notch_y), (x1, y1), (x0, y1)],
               stroke=MUTED, width=0.25, dash=(1.5, 1))
    sh.text(x1 - 1.5, y1 - 2, labels["build_zone"], size=6.5, bold=True, color=MUTED, align="right")

    E.fold_switch(sh)
    sh.text(183, 36.5, labels["switch"], size=6, color=MUTED, align="center")

    E.zone(sh, S.ZONE_SCHEMATIC, labels["schematic"], labels["schematic_note"])
    wx0, wy0, wx1, wy1 = S.ZONE_WORKBOOK
    third = (wy1 - wy0 - 4) / 3
    for i, (title, prompt) in enumerate(WORDS.fields("Workbook").items()):
        top = wy0 + i * (third + 2)
        E.workbook_box(sh, (wx0, top, wx1, top + third), title, prompt)

    _legend(sh, x0 + 12, 44)
    E.footer(sh, PAGE_ID)
    sh.save()


def _legend(sh, x, y):
    """The drawing marks, top to bottom in the order the words list them. The heading is
    the words' section name."""
    tx = x + 52
    heading = "Drawing marks"
    sh.text(x, y - 6, heading, size=8, bold=True)
    marks = iter(WORDS.fields(heading).items())

    def caption(row_y):
        title, detail = next(marks)
        sh.runs(tx, row_y + 1, [(title, True), ("  " + detail, False)], size=7)

    E.lane(sh, [(x, y), (x + 40, y)])
    caption(y)

    y += 14
    E.lane(sh, [(x, y), (x + 22, y), (x + 22, y + 10)])
    caption(y + 3)

    y += 22
    E.lane(sh, [(x, y), (x + 40, y)])
    E.joint(sh, x + 20, y)
    caption(y)

    y += 18
    under = E.lane(sh, [(x, y), (x + 40, y)])
    E.crossing(sh, x + 20, y)
    over = E.lane(sh, [(x + 20, y - 8), (x + 20, y + 8)])
    sh.allow(under, over, 0)
    caption(y)

    y += 20
    E.lane(sh, [(x, y), (x + 40, y)])
    E.test_point(sh, x + 20, y, "TP1", side="above")
    caption(y)

    y += 16
    E.lane(sh, [(x, y), (x + 15, y)])
    E.lane(sh, [(x + 25, y), (x + 40, y)])
    E.resistor(sh, x + 20, y, vertical=False, lead=10, label="R1")
    caption(y)

    y += 16
    E.lane(sh, [(x, y), (x + 13, y)])
    E.lane(sh, [(x + 27, y), (x + 40, y)])
    E.led(sh, x + 20, y, lead_anode=12, lead_cathode=10, label="LED1")
    caption(y)

    y += 16
    E.lane(sh, [(x, y), (x + 15, y)])
    E.lane(sh, [(x + 25, y), (x + 40, y)])
    E.diode(sh, x + 20, y, lead=9, label="D1")
    caption(y)
