"""Building blocks the T-series test sheets share: result columns, step and bullet lists,
and the tables for recording results."""

from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Table, TableStyle

from .draw import FONT, FONT_BOLD, GUIDE, INK, MUTED, style

RESULT_X = (167.0, 181.0, 195.0)

H = style(9, bold=True, spaceBefore=5, spaceAfter=2)
NOTE = style(7, leading=9.2, color=MUTED, spaceBefore=2)


def row(text):
    """A test row's words, "name · hint", as (name, hint). The hint may be left out."""
    name, _, hint = text.partition(" · ")
    return name, hint


def plain(texts):
    return [Paragraph(t, style(7.5, leading=9.6)) for t in texts]


def section(words, name, kind, notes=0, heading=False, **values):
    """A procedure heading, then `words`' section `name`: its items as `kind` (bullets,
    steps or plain), and its last `notes` paragraphs as notes. The heading is the
    section's name, or, with heading=True, its first paragraph, for a heading that can't
    be a section name because it repeats or carries a tag."""
    items = words.items(name, **values)
    if heading:
        name, *items = items
    body, after = items[: len(items) - notes], items[len(items) - notes :]
    return [Paragraph(name, H)] + kind(body) + [Paragraph(t, NOTE) for t in after]


def bullets(items):
    return [
        Paragraph(
            t,
            style(7.5, leading=9.6, leftIndent=7, bulletIndent=0.5, bulletFontSize=7.5, spaceAfter=1.2),
            bulletText="•",
        )
        for t in items
    ]


def steps(items):
    return [
        Paragraph(
            t,
            style(
                7.5,
                leading=9.6,
                leftIndent=9,
                bulletIndent=0,
                bulletFontName=FONT_BOLD,
                bulletFontSize=7.5,
                spaceAfter=1.5,
            ),
            bulletText=f"{i}.",
        )
        for i, t in enumerate(items, 1)
    ]


def result_headers(sh, y, names=("Day 0", "Flexed", "Day 7")):
    for x, name in zip(RESULT_X, names):
        sh.text(x, y, name, size=6.5, bold=True, align="center")


def result_boxes(sh, y):
    for x in RESULT_X:
        sh.rect(x - 6, y - 3, x + 6, y + 3, stroke=INK, width=0.25)


def table(data, col_widths, row_height):
    t = Table(data, colWidths=[w * mm for w in col_widths], rowHeights=row_height * mm, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, -1), FONT, 7),
                ("FONT", (0, 0), (0, -1), FONT_BOLD, 7),
                ("TEXTCOLOR", (0, 0), (-1, -1), INK),
                ("GRID", (0, 0), (-1, -1), 0.6, GUIDE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def decision_table(rows, widths=(33, 47), row_height=8.5):
    """Questions on the left, a blank cell for the answer on the right."""
    return table([[r, ""] for r in rows], list(widths), row_height)
