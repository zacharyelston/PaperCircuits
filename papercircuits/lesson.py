"""Building blocks every lesson page shares: bullet and step lists, the You need and
Build it columns, the schematic panel and the three workbook boxes."""

from reportlab.platypus import Paragraph

from . import standard as S
from .draw import GUIDE, INK, MUTED, style
from .provisional import TAG_NOTE

HEADING = style(8.5, bold=True, spaceAfter=1.5)


def items(texts, numbered, size=7, leading=8.8, space_after=1.2):
    out = []
    for i, t in enumerate(texts, 1):
        p_style = style(size, leading=leading, leftIndent=8 if numbered else 7, bulletIndent=0,
                        bulletFontSize=size, spaceAfter=space_after)
        out.append(Paragraph(t, p_style, bulletText=f"{i}." if numbered else "•"))
    return out


def tag_note():
    return Paragraph(TAG_NOTE, style(6.5, leading=8.2, color=MUTED, spaceBefore=2))


def need_and_steps(sh, page_id, need, steps, need_rect, steps_rect):
    """The You need list and the numbered Build it steps, each poured into its own
    rect, with the tag note under the steps."""
    need_story = [Paragraph("You need", HEADING)] + items(need, numbered=False)
    steps_story = [Paragraph("Build it", HEADING)] + items(steps, numbered=True) + [tag_note()]
    rest = sh.flow([need_rect], need_story) + sh.flow([steps_rect], steps_story)
    if rest:
        raise RuntimeError(f"{page_id} instructions overflowed by {len(rest)} items")


def schematic_panel(sh):
    """Outline and title for the schematic zone."""
    x0, y0, x1, y1 = S.ZONE_SCHEMATIC
    sh.rect(x0, y0, x1, y1, stroke=INK, width=0.3, radius=1.2)
    sh.text(x0 + 2, y0 + 4, "Schematic", size=7, bold=True)


def schematic_note(sh, text):
    """One muted line along the bottom of the schematic panel."""
    x0, _, _, y1 = S.ZONE_SCHEMATIC
    sh.text(x0 + 2, y1 - 2.5, text, size=6, color=MUTED)


def workbook_boxes():
    """The Predict, Measure and Explain boxes' rects, top to bottom."""
    x0, y0, x1, y1 = S.ZONE_WORKBOOK
    h = (y1 - y0 - 4) / 3
    return [(x0, y0 + i * (h + 2), x1, y0 + i * (h + 2) + h) for i in range(3)]


def write_lines(sh, box, offsets):
    """Faint lines to write on, `offsets` mm below the box's top."""
    x0, y0, x1, _ = box
    for dy in offsets:
        sh.line(x0 + 2, y0 + dy, x1 - 2, y0 + dy, width=0.2, color=GUIDE)


def answer_table(sh, x, y, title, rows, cols, label_w=22.0, pitch=13.0, box_w=10.0, row_h=4.8, unit=None):
    """A small table to write in: a bold title and column heads on the first line, then
    one row label and a row of answer boxes per row. `unit` goes after every box."""
    sh.text(x, y, title, size=7, bold=True)
    col_x = x + label_w
    for j, col in enumerate(cols):
        sh.text(col_x + j * pitch + box_w / 2, y, col, size=6.5, bold=True, color=MUTED, align="center")
    for i, row in enumerate(rows):
        ry = y + row_h * (i + 1)
        sh.text(x, ry, row, size=7)
        for j in range(len(cols)):
            bx = col_x + j * pitch
            sh.rect(bx, ry - 3.3, bx + box_w, ry + 0.9, stroke=INK, width=0.25)
            if unit:
                sh.text(bx + box_w + 0.8, ry, unit, size=6, color=MUTED)
