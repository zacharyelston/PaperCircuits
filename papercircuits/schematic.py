"""Circuit-diagram symbols for the schematic panel, IEC style, in page mm."""

from .draw import INK, MUTED, WHITE

W = 0.3


def wire(sh, pts):
    sh.polygon(pts, stroke=INK, width=W, closed=False)


def junction(sh, x, y):
    sh.circle(x, y, 1.1, stroke=None, fill=INK)


def terminal(sh, x, y, label, label_y, align="left"):
    """Open circle where a net meets the binder. Left-hand terminals label to the right
    of x - 1.5; right-hand ones (align="right") end their label at x + 1.5."""
    sh.circle(x, y, 1.6, stroke=INK, fill=WHITE, width=W)
    if align == "right":
        sh.text(x + 1.5, label_y, label, size=6.5, bold=True, align="right")
    else:
        sh.text(x - 1.5, label_y, label, size=6.5, bold=True)


def test_point(sh, x, y, label, side="right"):
    """Small open circle at the end of a stub, as drawn on the page."""
    sh.circle(x, y, 1.8, stroke=INK, fill=WHITE, width=W)
    if side == "right":
        sh.text(x + 1.8, y + 1, label, size=6, bold=True)
    else:
        sh.text(x - 1.8, y + 1, label, size=6, bold=True, align="right")


def resistor(sh, x, y0, y1, label, value):
    """Vertical resistor from y0 to y1; a 3 × 8 mm box."""
    cy = (y0 + y1) / 2
    sh.line(x, y0, x, cy - 4, width=W)
    sh.line(x, cy + 4, x, y1, width=W)
    sh.rect(x - 1.5, cy - 4, x + 1.5, cy + 4, stroke=INK, fill=WHITE, width=W)
    sh.text(x + 3, cy - 0.4, label, size=6.5, bold=True)
    sh.text(x + 3, cy + 2.8, value, size=6, color=MUTED)


def ldr(sh, x, y0, y1, label, value):
    """Vertical light-dependent resistor: a resistor with two arrows of light coming in
    from the left."""
    resistor(sh, x, y0, y1, label, value)
    cy = (y0 + y1) / 2
    for dy in (-2.4, 0.6):
        x1, y1a = x - 2.2, cy + dy
        sh.line(x1 - 2.0, y1a - 2.0, x1, y1a, width=0.25)
        sh.polygon([(x1, y1a), (x1 - 0.9, y1a - 0.2), (x1 - 0.2, y1a - 0.9)], stroke=None, fill=INK)


def led(sh, x, y0, y1, label, anode_top=True):
    """Vertical LED from y0 to y1. Current flows from anode to cathode, the way the triangle points."""
    cy = (y0 + y1) / 2
    h, half = 3.4, 2.4
    base, apex = (cy - h / 2, cy + h / 2) if anode_top else (cy + h / 2, cy - h / 2)
    top, bottom = min(base, apex), max(base, apex)
    sh.line(x, y0, x, top, width=W)
    sh.line(x, bottom, x, y1, width=W)
    sh.polygon([(x - half, base), (x + half, base), (x, apex)], stroke=INK, fill=WHITE, width=W)
    sh.line(x - half, apex, x + half, apex, width=W)
    for dy in (-1.4, 0.6):
        x0, y0a = x + 2.4, cy + dy
        x1, y1a = x0 + 2.0, y0a - 2.0
        sh.line(x0, y0a, x1, y1a, width=0.25)
        sh.polygon([(x1, y1a), (x1 - 0.9, y1a + 0.2), (x1 - 0.2, y1a + 0.9)], stroke=None, fill=INK)
    sh.text(x + 5.4, cy + 1, label, size=6.5, bold=True)


def switch(sh, x0, x1, y, label):
    """Open switch on a horizontal wire from x0 to x1."""
    a, b = x0 + (x1 - x0) * 0.25, x0 + (x1 - x0) * 0.75
    sh.line(x0, y, a, y, width=W)
    sh.line(b, y, x1, y, width=W)
    sh.line(a, y, b + 0.4, y - 2.6, width=W)
    sh.circle(a, y, 0.9, stroke=INK, fill=WHITE, width=0.25)
    sh.circle(b, y, 0.9, stroke=INK, fill=WHITE, width=0.25)
    sh.text((a + b) / 2, y - 3.8, label, size=6.5, bold=True, align="center")


def battery(sh, x, y0, y1, label, value, cells=3):
    """Vertical battery from y0 (+) to y1 (−): a long and a short plate per cell."""
    pitch, gap = 2.8, 1.4
    span = cells * pitch - gap
    first = (y0 + y1) / 2 - span / 2
    sh.line(x, y0, x, first, width=W)
    for i in range(cells):
        long_y = first + i * pitch
        sh.line(x - 3, long_y, x + 3, long_y, width=W)
        sh.line(x - 1.6, long_y + gap, x + 1.6, long_y + gap, width=0.7)
        if i < cells - 1:
            sh.line(x, long_y + gap, x, long_y + pitch, width=W)
    sh.line(x, first + span, x, y1, width=W)
    sh.text(x - 4.6, first + 0.8, "+", size=6.5, bold=True, align="center")
    cy = (y0 + y1) / 2
    sh.text(x + 4.5, cy - 0.4, label, size=6.5, bold=True)
    sh.text(x + 4.5, cy + 2.8, value, size=6, color=MUTED)


def fuse(sh, x0, x1, y, label, value):
    """Horizontal fuse from x0 to x1: a 9 × 3 mm box with the wire running through it."""
    cx = (x0 + x1) / 2
    sh.line(x0, y, cx - 4.5, y, width=W)
    sh.line(cx + 4.5, y, x1, y, width=W)
    sh.rect(cx - 4.5, y - 1.5, cx + 4.5, y + 1.5, stroke=INK, fill=WHITE, width=W)
    sh.line(cx - 4.5, y, cx + 4.5, y, width=0.25)
    sh.text(cx, y + 4.6, label, size=6.5, bold=True, align="center")
    sh.text(cx, y + 7.6, value, size=6, color=MUTED, align="center")


def rheostat(sh, x, y0, y1, wiper_y, wiper_x, label, value, open_end="top"):
    """Vertical resistor box from y0 to y1 with a wiper arrow coming in from the left at
    wiper_y. The `open_end` ("top" or "bottom") is left as a stub: only the wiper and the
    other end connect."""
    if open_end == "top":
        sh.line(x, y0 - 3, x, y0, width=W)
    else:
        sh.line(x, y1, x, y1 + 3, width=W)
    sh.rect(x - 1.5, y0, x + 1.5, y1, stroke=INK, fill=WHITE, width=W)
    sh.line(wiper_x, wiper_y, x - 3.2, wiper_y, width=W)
    sh.polygon([(x - 1.6, wiper_y), (x - 3.4, wiper_y - 0.9), (x - 3.4, wiper_y + 0.9)], stroke=None, fill=INK)
    cy = (y0 + y1) / 2
    sh.text(x + 3, cy - 0.4, label, size=6.5, bold=True)
    sh.text(x + 3, cy + 2.8, value, size=6, color=MUTED)


def diode(sh, x, y0, y1, label, cathode_bottom=True):
    """Vertical diode from y0 to y1: the triangle points the way current flows."""
    cy = (y0 + y1) / 2
    h, half = 3.4, 2.4
    base, apex = (cy - h / 2, cy + h / 2) if cathode_bottom else (cy + h / 2, cy - h / 2)
    top, bottom = min(base, apex), max(base, apex)
    sh.line(x, y0, x, top, width=W)
    sh.line(x, bottom, x, y1, width=W)
    sh.polygon([(x - half, base), (x + half, base), (x, apex)], stroke=INK, fill=WHITE, width=W)
    sh.line(x - half, apex, x + half, apex, width=W)
    sh.text(x + 3.4, cy + 1, label, size=6.5, bold=True)


def capacitor(sh, x, y0, y1, label, value, polarised=True):
    """Vertical capacitor from y0 to y1. Polarised, + at y0: a thin plate over a solid one.
    Otherwise two thin plates."""
    cy = (y0 + y1) / 2
    gap, half = 1.6, 3.0
    sh.line(x, y0, x, cy - gap / 2, width=W)
    if polarised:
        sh.line(x, cy + gap / 2 + 0.9, x, y1, width=W)
        sh.line(x - half, cy - gap / 2, x + half, cy - gap / 2, width=W)
        sh.rect(x - half, cy + gap / 2, x + half, cy + gap / 2 + 0.9, stroke=None, fill=INK)
        sh.text(x - 4.4, cy - 1.6, "+", size=6.5, bold=True, align="center")
    else:
        sh.line(x, cy + gap / 2, x, y1, width=W)
        for py in (cy - gap / 2, cy + gap / 2):
            sh.line(x - half, py, x + half, py, width=W)
    sh.text(x + 4.2, cy - 0.4, label, size=6.5, bold=True)
    sh.text(x + 4.2, cy + 2.8, value, size=6, color=MUTED)


def resistor_h(sh, x0, x1, y, label, value="", box_w=8.0):
    """Horizontal resistor from x0 to x1."""
    cx = (x0 + x1) / 2
    sh.line(x0, y, cx - box_w / 2, y, width=W)
    sh.line(cx + box_w / 2, y, x1, y, width=W)
    sh.rect(cx - box_w / 2, y - 1.5, cx + box_w / 2, y + 1.5, stroke=INK, fill=WHITE, width=W)
    sh.text(cx, y - 2.6, label, size=6.5, bold=True, align="center")
    if value:
        sh.text(cx, y + 4.6, value, size=6, color=MUTED, align="center")


def capacitor_h(sh, x0, x1, y, label, value="", plus=None):
    """Horizontal capacitor from x0 to x1, with no polarity. With `plus` ("left" or
    "right") it's polarised: a thin + plate and a solid − one."""
    cx = (x0 + x1) / 2
    sh.line(x0, y, cx - 0.8, y, width=W)
    sh.line(cx + 0.8, y, x1, y, width=W)
    if plus is None:
        for px in (cx - 0.8, cx + 0.8):
            sh.line(px, y - 2.6, px, y + 2.6, width=0.45)
    else:
        s = -1 if plus == "left" else 1
        sh.line(cx + s * 0.8, y - 2.6, cx + s * 0.8, y + 2.6, width=0.45)
        rx0, rx1 = sorted((cx - s * 0.8, cx - s * 1.7))
        sh.rect(rx0, y - 2.6, rx1, y + 2.6, stroke=None, fill=INK)
        sh.text(cx + s * 2.6, y - 1.2, "+", size=6.5, bold=True, align="center")
    sh.text(cx, y - 3.6, label, size=6.5, bold=True, align="center")
    if value:
        sh.text(cx, y + 5.6, value, size=6, color=MUTED, align="center")


def npn(sh, x, y, label, base="left"):
    """NPN transistor centred at (x, y), base facing `base`. Returns the base, collector
    and emitter terminal points; the collector leaves upward and the emitter downward."""
    s = 1 if base == "left" else -1
    sh.circle(x, y, 7.0, stroke=INK, fill=WHITE, width=W)
    bar = x - s * 1.2
    sh.line(bar, y - 2.2, bar, y + 2.2, width=0.55)
    b, c, e = (x - s * 4.5, y), (x + s * 1.6, y - 5.5), (x + s * 1.6, y + 5.5)
    sh.line(b[0], y, bar, y, width=W)
    sh.polygon([(bar, y - 1.0), (c[0], y - 2.6), c], stroke=INK, width=W, closed=False)
    sh.polygon([(bar, y + 1.0), (e[0], y + 2.6), e], stroke=INK, width=W, closed=False)
    tip = (bar + s * 2.6, y + 2.3)
    sh.polygon([tip, (tip[0] - s * 1.1, tip[1] - 0.15), (tip[0] - s * 0.5, tip[1] - 1.0)], stroke=None, fill=INK)
    if s == 1:
        sh.text(x + 4.2, y + 7.2, label, size=6.5, bold=True)
    else:
        sh.text(x - 4.2, y + 7.2, label, size=6.5, bold=True, align="right")
    return b, c, e
