"""A4 canvas in the page standard's coordinates: mm, origin top-left, y down."""

import os

import reportlab
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph

from . import standard as S

INK = HexColor("#1f1f1f")
MUTED = HexColor("#666666")
GUIDE = HexColor("#a6a6a6")
COPPER = HexColor("#b87333")
COPPER_TINT = HexColor("#f6e6d8")
WHITE = HexColor("#ffffff")

# Vera ships with reportlab and has the Ω, ≥ and × glyphs the core PDF fonts lack.
FONT = "Vera"
FONT_BOLD = "Vera-Bold"


def _register_fonts():
    fonts = os.path.join(os.path.dirname(reportlab.__file__), "fonts")
    faces = {
        FONT: "Vera.ttf",
        FONT_BOLD: "VeraBd.ttf",
        "Vera-Italic": "VeraIt.ttf",
        "Vera-BoldItalic": "VeraBI.ttf",
    }
    for name, filename in faces.items():
        pdfmetrics.registerFont(TTFont(name, os.path.join(fonts, filename)))
    pdfmetrics.registerFontFamily(
        FONT, normal=FONT, bold=FONT_BOLD, italic="Vera-Italic", boldItalic="Vera-BoldItalic"
    )


_register_fonts()


def style(size=7.5, leading=None, bold=False, color=INK, **kw):
    return ParagraphStyle(
        name=f"s{size}{bold}",
        fontName=FONT_BOLD if bold else FONT,
        fontSize=size,
        leading=leading or size * 1.3,
        textColor=color,
        **kw,
    )


class Sheet:
    def __init__(self, path, title):
        self.c = canvas.Canvas(str(path), pagesize=(S.PAGE_W * mm, S.PAGE_H * mm))
        self.c.setTitle(title)
        self.c.setAuthor("PaperCircuits")

    def pt(self, x, y):
        return x * mm, (S.PAGE_H - y) * mm

    def _pen(self, stroke, fill, width, dash):
        c = self.c
        if stroke is not None:
            c.setStrokeColor(stroke)
            c.setLineWidth(width * mm)
            c.setDash([d * mm for d in dash] if dash else [])
        if fill is not None:
            c.setFillColor(fill)

    def line(self, x0, y0, x1, y1, width=0.25, color=INK, dash=None, cap=0):
        self._pen(color, None, width, dash)
        self.c.setLineCap(cap)
        self.c.line(*self.pt(x0, y0), *self.pt(x1, y1))
        self.c.setLineCap(0)

    def polygon(self, pts, stroke=INK, fill=None, width=0.25, dash=None, closed=True):
        self._pen(stroke, fill, width, dash)
        path = self.c.beginPath()
        path.moveTo(*self.pt(*pts[0]))
        for p in pts[1:]:
            path.lineTo(*self.pt(*p))
        if closed:
            path.close()
        self.c.drawPath(path, stroke=int(stroke is not None), fill=int(fill is not None))

    def rect(self, x0, y0, x1, y1, stroke=INK, fill=None, width=0.25, dash=None, radius=0):
        self._pen(stroke, fill, width, dash)
        x, y = self.pt(x0, y1)
        w, h = (x1 - x0) * mm, (y1 - y0) * mm
        stroke_on, fill_on = int(stroke is not None), int(fill is not None)
        if radius:
            self.c.roundRect(x, y, w, h, radius * mm, stroke=stroke_on, fill=fill_on)
        else:
            self.c.rect(x, y, w, h, stroke=stroke_on, fill=fill_on)

    def circle(self, cx, cy, d, stroke=INK, fill=None, width=0.25, dash=None):
        self._pen(stroke, fill, width, dash)
        self.c.circle(*self.pt(cx, cy), d / 2 * mm, stroke=int(stroke is not None), fill=int(fill is not None))

    def text(self, x, y, s, size=7, bold=False, color=INK, align="left"):
        """y is the baseline."""
        c = self.c
        c.setFont(FONT_BOLD if bold else FONT, size)
        c.setFillColor(color)
        draw = {"left": c.drawString, "center": c.drawCentredString, "right": c.drawRightString}[align]
        draw(*self.pt(x, y), s)

    def width(self, s, size=7, bold=False):
        return pdfmetrics.stringWidth(s, FONT_BOLD if bold else FONT, size) / mm

    def runs(self, x, y, parts, size=7, color=INK):
        """Draw (text, bold) runs one after another on a baseline; returns the end x."""
        for s, bold in parts:
            self.text(x, y, s, size=size, bold=bold, color=color)
            x += self.width(s, size, bold)
        return x

    def paragraph(self, x, y, width, markup, para_style):
        """Draw wrapped text with its top at y; returns its height in mm."""
        p = Paragraph(markup, para_style)
        _, h = p.wrapOn(self.c, width * mm, S.PAGE_H * mm)
        p.drawOn(self.c, x * mm, (S.PAGE_H - y) * mm - h)
        return h / mm

    def flow(self, columns, story):
        """Pour flowables into (x0, y0, x1, y1) columns in order; returns what didn't fit."""
        for x0, y0, x1, y1 in columns:
            frame = Frame(
                x0 * mm, (S.PAGE_H - y1) * mm, (x1 - x0) * mm, (y1 - y0) * mm,
                leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0,
            )
            frame.addFromList(story, self.c)
        return story

    def next_page(self):
        self.c.showPage()

    def save(self):
        self.c.save()
