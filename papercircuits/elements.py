"""Standard page elements: spine, header, footer, tape lanes, marks and part footprints."""

import math

from . import standard as S
from .draw import COPPER, COPPER_TINT, FAINT, GUIDE, INK, MUTED, WHITE


def _unit(ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    n = math.hypot(dx, dy)
    return dx / n, dy / n


def _offset_sides(pts, half):
    """Both edges of a band of half-width `half` along a polyline, with mitred corners."""
    normals = []
    for a, b in zip(pts, pts[1:]):
        ux, uy = _unit(*a, *b)
        normals.append((-uy, ux))
    sides = []
    for sign in (1, -1):
        h = half * sign
        side = [(pts[0][0] + h * normals[0][0], pts[0][1] + h * normals[0][1])]
        for i in range(1, len(pts) - 1):
            (n1x, n1y), (n2x, n2y) = normals[i - 1], normals[i]
            k = h / (1 + n1x * n2x + n1y * n2y)
            side.append((pts[i][0] + k * (n1x + n2x), pts[i][1] + k * (n1y + n2y)))
        side.append((pts[-1][0] + h * normals[-1][0], pts[-1][1] + h * normals[-1][1]))
        sides.append(side)
    return sides


def lane(sh, pts, width=S.TAPE_W, folds=True):
    """A tape lane along a polyline. Interior corners get a fold crease unless folds=False.
    Returns the lane's id for the clearance check (see Sheet.allow)."""
    left, right = _offset_sides(pts, width / 2)
    sh.polygon(left + right[::-1], stroke=COPPER, fill=COPPER_TINT, width=0.25, dash=(1.2, 0.8))
    if folds:
        for a, b in zip(left[1:-1], right[1:-1]):
            sh.line(*a, *b, width=0.35, color=COPPER)
    sh.lanes.append(left + right[::-1])
    return len(sh.lanes) - 1


def joint(sh, x, y, vertical=False, width=S.TAPE_W, label="J"):
    """Overlap joint centred on (x, y): ticks at each end of the overlap."""
    half, reach = S.JOINT_OVERLAP / 2, width / 2 + 1.2
    for d in (-half, half):
        if vertical:
            sh.line(x - reach, y + d, x + reach, y + d, width=0.35)
        else:
            sh.line(x + d, y - reach, x + d, y + reach, width=0.35)
    if label:
        if vertical:
            sh.text(x + reach + 1, y + 1, label, size=6.5, bold=True)
        else:
            sh.text(x, y - reach - 1, label, size=6.5, bold=True, align="center")


def corner_joint(sh, x, y, width=S.TAPE_W):
    """A cut-and-overlap corner: outline the square where the two pieces overlap."""
    h = width / 2
    sh.rect(x - h, y - h, x + h, y + h, width=0.35)


def crossing(sh, cx, cy, size=S.CROSSING_PATCH, label="X"):
    """Hatched insulating patch. Draw it after the lower lane and before the upper one."""
    x0, y0, s = cx - size / 2, cy - size / 2, size
    sh.rect(x0, y0, x0 + s, y0 + s, stroke=INK, fill=WHITE, width=0.3)
    step = 1.4
    c = step
    while c < 2 * s:
        if c <= s:
            sh.line(x0 + c, y0, x0, y0 + c, width=0.15, color=MUTED)
        else:
            sh.line(x0 + s, y0 + c - s, x0 + c - s, y0 + s, width=0.15, color=MUTED)
        c += step
    if label:
        sh.text(x0 + s + 1, y0 + 2.5, label, size=6.5, bold=True)


def test_point(sh, cx, cy, label=None, side="right", size=6.5):
    sh.circle(cx, cy, S.TEST_POINT_D, stroke=INK, width=0.35)
    sh.circle(cx, cy, 0.7, stroke=None, fill=INK)
    if label:
        r = S.TEST_POINT_D / 2
        if side == "right":
            sh.text(cx + r + 1.2, cy + 1.1, label, size=size, bold=True)
        elif side == "left":
            sh.text(cx - r - 1.2, cy + 1.1, label, size=size, bold=True, align="right")
        elif side == "above":
            sh.text(cx, cy - r - 1.2, label, size=size, bold=True, align="center")
        else:
            sh.text(cx, cy + r + 3.2, label, size=size, bold=True, align="center")


def hole(sh, hole_id, connected=True, strip_width=S.TAPE_W, label_below=False):
    """Punch guide with eyelet flange ring and the hole's net name."""
    y, net = S.HOLES[hole_id]
    x = S.HOLE_X
    sh.circle(x, y, S.EYELET_FLANGE_D, stroke=GUIDE, width=0.2, dash=(0.8, 0.8))
    sh.circle(x, y, S.HOLE_D, stroke=INK, fill=WHITE, width=0.3)
    arm = S.HOLE_D / 2 + 1.5
    sh.line(x - arm, y, x + arm, y, width=0.15, color=INK)
    sh.line(x, y - arm, x, y + arm, width=0.15, color=INK)
    tag = f"{hole_id} {net}" if connected else f"{hole_id} {net} · NC"
    label_y = y + strip_width / 2 + 3.8 if label_below else y - strip_width / 2 - 1.7
    sh.text(x + 6.5, label_y, tag, size=6, color=MUTED)


def spine(sh, connected=(), strip_widths=None, edge=False, labels_below=()):
    """All four holes, optionally the spine edge. `connected` lists hole ids that carry a net strip;
    `labels_below` moves a hole's net name under its strip (H4 when Bus B climbs the gutter)."""
    strip_widths = strip_widths or {}
    if edge:
        sh.line(S.SPINE_W, 26, S.SPINE_W, 280, width=0.15, color=GUIDE, dash=(0.4, 1.6))
    for hole_id in S.HOLES:
        hole(sh, hole_id, connected=hole_id in connected,
             strip_width=strip_widths.get(hole_id, S.TAPE_W), label_below=hole_id in labels_below)


def net_strip(sh, hole_id, to_x=S.ZONE_BUILD[0], width=S.TAPE_W):
    """Net strip from a hole to the build zone. Bus B climbs the gutter first (standard §2)."""
    y = S.hole_y(hole_id)
    start = (S.NET_STRIP_START_X, y)
    if hole_id == "H4":
        pts = [start, (S.BUS_B_GUTTER_X, y), (S.BUS_B_GUTTER_X, S.BUS_B_ENTRY_Y), (to_x, S.BUS_B_ENTRY_Y)]
    else:
        pts = [start, (to_x, y)]
    lane(sh, pts, width=width)


def header(sh, page_id, title, subtitle, part=None, status=None):
    x0, _, x1, _ = S.ZONE_HEADER
    sh.text(x0, 13, title, size=15, bold=True)
    sh.text(x0, 19.2, subtitle, size=7, color=MUTED)
    sh.text(x1, 13, page_id if part is None else f"{page_id} · {part}", size=10, bold=True, align="right")
    if status:
        if x0 + sh.width(subtitle, 7) > x1 - sh.width(status, 6) - 3:
            raise ValueError(f"{page_id}: subtitle runs into the header status; shorten it")
        sh.text(x1, 19.2, status, size=6, color=COPPER, align="right")
    sh.line(x0, 22, x1, 22, width=0.2, color=GUIDE)


def footer(sh, page_id):
    x0, y0, x1, _ = S.ZONE_FOOTER
    bar_y = y0 + 1.5
    sh.line(x0, bar_y, x0 + S.SCALE_BAR, bar_y, width=0.3)
    for i in range(11):
        tick = 1.4 if i in (0, 5, 10) else 0.8
        sh.line(x0 + i * 10, bar_y - tick, x0 + i * 10, bar_y, width=0.2)
    sh.text(x0, bar_y + 3.6, "Print at 100 %: this bar should measure 100 mm.", size=6, color=MUTED)
    sh.text(x1, bar_y + 3.6, f"PaperCircuits page standard v{S.VERSION} · {page_id}", size=6, color=MUTED, align="right")


def zone(sh, rect, name, note=None):
    x0, y0, x1, y1 = rect
    sh.rect(x0, y0, x1, y1, stroke=GUIDE, width=0.25, dash=(1.5, 1))
    sh.text(x0 + 1.5, y0 + 3.5, name, size=6.5, bold=True, color=MUTED)
    if note:
        sh.text(x0 + 1.5, y0 + 6.6, note, size=6, color=MUTED)


def workbook_box(sh, rect, title, prompt):
    x0, y0, x1, y1 = rect
    sh.rect(x0, y0, x1, y1, stroke=INK, width=0.3, radius=1.2)
    sh.runs(x0 + 2, y0 + 4, [(title, True), ("  " + prompt, False)], size=7)


def fold_switch(sh, stubs=True):
    """Fold line and flap pad. The page half-pads are the ends of the two switch lanes;
    `stubs` draws short ones for pages that don't route those lanes."""
    (fx0, fy0), (fx1, fy1) = S.SWITCH_FOLD
    sh.line(fx0, fy0, fx1, fy1, width=0.3, color=INK, dash=(2, 1.2))
    cx, cy = S.SWITCH_CENTER
    hl, hw = S.FLAP_PAD_LEN / 2, S.TAPE_W / 2
    landing = [(cx - hl, cy - hw), (cx + hl, cy - hw), (cx + hl, cy + hw), (cx - hl, cy + hw)]
    sh.polygon([S.reflect_across_fold(*p) for p in landing], stroke=COPPER, fill=COPPER_TINT, dash=(1.2, 0.8))
    sh.polygon(landing, stroke=INK, width=0.2, dash=(0.5, 0.7))
    if stubs:
        a, b = (lane(sh, [(x, S.SWITCH_LANE_TOP), (x, S.SWITCH_LANE_TOP + 10)]) for x in S.SWITCH_LANE_X)
        sh.allow(a, b, S.SWITCH_PAD_GAP)


def tab_switch(sh, x, upper_y, label, pitch=S.PAIR_PITCH):
    """Tab switch over a horizontal switch pair whose upper lane is centred on upper_y and
    whose lower lane is `pitch` below it. The flap is cut above the pair and hinges down
    onto it; its pad lands across both lanes as a vertical strip."""
    hinge = upper_y - S.TAPE_W / 2 - S.TAB_HINGE_CLEAR
    x0, x1, top = x - S.TAB_W / 2, x + S.TAB_W / 2, hinge - S.TAB_H
    sh.polygon([(x0, hinge), (x0, top), (x1, top), (x1, hinge)], stroke=INK, width=0.35, closed=False)
    sh.line(x0, hinge, x1, hinge, width=0.3, color=INK, dash=(0.4, 0.9))
    mid = upper_y + pitch / 2
    hl, hw = S.FLAP_PAD_LEN / 2, S.TAPE_W / 2
    pad_cy = 2 * hinge - mid
    sh.rect(x - hw, pad_cy - hl, x + hw, pad_cy + hl, stroke=COPPER, fill=COPPER_TINT, dash=(1.2, 0.8))
    sh.rect(x - hw, mid - hl, x + hw, mid + hl, stroke=INK, width=0.2, dash=(0.5, 0.7))
    sh.text(x, top - 1.5, label, size=7.5, bold=True, align="center")


def pencil_track(sh, x0, y0, x1, y1, tick=10.0, last_number=None):
    """A band to shade with a soft pencil: solid outline, light hatching, and a tick every
    `tick` mm under it, numbered in mm from 0 at x0 up to `last_number`."""
    step = 2.0
    c = x0 + y0 + step
    while c < x1 + y1:
        xa, xb = max(x0, c - y1), min(x1, c - y0)
        if xa < xb:
            sh.line(xa, c - xa, xb, c - xb, width=0.15, color=GUIDE)
        c += step
    sh.rect(x0, y0, x1, y1, stroke=INK, width=0.35)
    last = x1 - x0 if last_number is None else last_number
    i = 0.0
    while x0 + i <= x1 + 0.01:
        sh.line(x0 + i, y1, x0 + i, y1 + 1.6, width=0.25)
        if i <= last + 0.01:
            sh.text(x0 + i, y1 + 4.4, f"{i:g}", size=6, color=MUTED, align="center")
        i += tick


def wiper_card(sh, x0, y0, x1, y1, strip_len, label="Wiper"):
    """A card piece to cut out, with a strip of tape along its length. Turned copper side
    down, it joins a lane to a pencil track wherever it's pressed."""
    sh.rect(x0, y0, x1, y1, stroke=INK, width=0.35)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hw, hl = S.TAPE_W / 2, strip_len / 2
    sh.rect(cx - hw, cy - hl, cx + hw, cy + hl, stroke=COPPER, fill=COPPER_TINT, dash=(1.2, 0.8))
    sh.text(cx, y0 - 1.8, label, size=7.5, bold=True, align="center")
    sh.text(cx, y1 + 3.6, "cut out", size=6, color=MUTED, align="center")


# Part footprints, actual size.

def resistor(sh, cx, cy, vertical=True, lead=11.0, label=None):
    """1/4 W resistor: 6.3 × 2.4 mm body, leads reaching `lead` mm from the centre."""
    bl, bw = 6.3, 2.4
    if vertical:
        sh.line(cx, cy - lead, cx, cy + lead, width=0.6, color=MUTED, cap=1)
        sh.rect(cx - bw / 2, cy - bl / 2, cx + bw / 2, cy + bl / 2, stroke=MUTED, fill=WHITE, width=0.3, radius=1)
        for d in (-1.6, -0.6, 0.4):
            sh.line(cx - bw / 2, cy + d, cx + bw / 2, cy + d, width=0.35, color=MUTED)
        if label:
            sh.text(cx + bw / 2 + 1, cy + 1, label, size=6, color=MUTED)
    else:
        sh.line(cx - lead, cy, cx + lead, cy, width=0.6, color=MUTED, cap=1)
        sh.rect(cx - bl / 2, cy - bw / 2, cx + bl / 2, cy + bw / 2, stroke=MUTED, fill=WHITE, width=0.3, radius=1)
        for d in (-1.6, -0.6, 0.4):
            sh.line(cx + d, cy - bw / 2, cx + d, cy + bw / 2, width=0.35, color=MUTED)
        if label:
            sh.text(cx, cy - S.TAPE_W / 2 - 1.1, label, size=6, color=MUTED, align="center")


def led(sh, cx, cy, anode="left", lead_anode=12.0, lead_cathode=9.0, label=None):
    """5 mm LED seen from above, legs splayed flat. The anode (long leg, +) points
    `anode`: left, right, up or down."""
    dx, dy = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}[anode]
    sh.line(cx + dx * lead_anode, cy + dy * lead_anode, cx - dx * lead_cathode, cy - dy * lead_cathode,
            width=0.5, color=MUTED, cap=1)
    sh.circle(cx, cy, 5.8, stroke=MUTED, fill=WHITE, width=0.3)
    sh.circle(cx, cy, 5.0, stroke=MUTED, width=0.2)
    if dy:
        sh.text(cx - 4.5, cy + dy * 2.2 + 1.2, "+", size=7, bold=True, align="center")
        if label:
            sh.text(cx + 4.2, cy + 1, label, size=6, color=MUTED)
    else:
        sh.text(cx + dx * 4.6, cy - S.TAPE_W / 2 - 0.9, "+", size=7, bold=True, align="center")
        if label:
            sh.text(cx, cy - 4.2, label, size=6, color=MUTED, align="center")


def ptc(sh, cx, cy, lead=12.0, label=None):
    """Radial resettable fuse laid flat, legs splayed left and right."""
    bw, bh = 7.5, 6.0
    sh.line(cx - lead, cy, cx + lead, cy, width=0.5, color=MUTED, cap=1)
    sh.rect(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2, stroke=MUTED, fill=WHITE, width=0.3, radius=2)
    sh.text(cx, cy + 1, "PTC", size=6, color=MUTED, align="center")
    if label:
        sh.text(cx, cy - bh / 2 - 1.2, label, size=6, color=MUTED, align="center")


def battery_holder(sh, x0, y0, cells=3, label=None):
    """Side-by-side AA holder at actual size: 58 mm along the cells, 15.5 mm per cell.
    Returns its bottom edge."""
    length, pitch, cell_len, cell_d = 58.0, 15.5, 50.5, 14.0
    y1 = y0 + cells * pitch + 1.5
    sh.rect(x0, y0, x0 + length, y1, stroke=INK, width=0.35, radius=2)
    cx0 = x0 + (length - cell_len) / 2
    for i in range(cells):
        top = y0 + 1.5 + i * pitch
        sh.rect(cx0, top, cx0 + cell_len, top + cell_d, stroke=GUIDE, width=0.25, radius=3)
        sh.text(cx0 + cell_len / 2, top + cell_d / 2 + 1, "AA", size=6, color=MUTED, align="center")
        plus_x = cx0 + cell_len - 3 if i % 2 == 0 else cx0 + 3
        sh.text(plus_x, top + cell_d / 2 + 1.2, "+", size=7, bold=True, color=MUTED, align="center")
    if label:
        sh.text(x0 + length / 2, y1 + 4, label, size=6.5, color=MUTED, align="center")
    return y1


def wire_lead(sh, x_from, x_to, y, strip=8.0):
    """Insulated wire running left from x_from; its last `strip` mm, ending at x_to, is bare."""
    bare = x_to + strip
    sh.line(x_from, y, bare, y, width=1.4, color=MUTED, cap=1)
    sh.line(bare, y, x_to, y, width=0.5, color=INK, cap=1)


def checkbox(sh, x, y, size=3.0):
    """A tick box sitting on the text baseline y."""
    sh.rect(x, y - size + 0.4, x + size, y + 0.4, stroke=INK, width=0.3)


def diode(sh, cx, cy, lead=8.0, label=None, cathode="right"):
    """Small-signal diode (1N4148 size). The band marks the cathode, which points
    `cathode`: right, left, up or down."""
    bl, bw = 4.0, 1.9
    if cathode in ("right", "left"):
        sh.line(cx - lead, cy, cx + lead, cy, width=0.5, color=MUTED, cap=1)
        sh.rect(cx - bl / 2, cy - bw / 2, cx + bl / 2, cy + bw / 2, stroke=MUTED, fill=WHITE, width=0.3, radius=0.6)
        if cathode == "right":
            sh.rect(cx + bl / 2 - 1.0, cy - bw / 2, cx + bl / 2 - 0.4, cy + bw / 2, stroke=None, fill=MUTED)
        else:
            sh.rect(cx - bl / 2 + 0.4, cy - bw / 2, cx - bl / 2 + 1.0, cy + bw / 2, stroke=None, fill=MUTED)
        if label:
            sh.text(cx, cy - S.TAPE_W / 2 - 1.1, label, size=6, color=MUTED, align="center")
    else:
        sh.line(cx, cy - lead, cx, cy + lead, width=0.5, color=MUTED, cap=1)
        sh.rect(cx - bw / 2, cy - bl / 2, cx + bw / 2, cy + bl / 2, stroke=MUTED, fill=WHITE, width=0.3, radius=0.6)
        if cathode == "down":
            sh.rect(cx - bw / 2, cy + bl / 2 - 1.0, cx + bw / 2, cy + bl / 2 - 0.4, stroke=None, fill=MUTED)
        else:
            sh.rect(cx - bw / 2, cy - bl / 2 + 0.4, cx + bw / 2, cy - bl / 2 + 1.0, stroke=None, fill=MUTED)
        if label:
            sh.text(cx + bw / 2 + 1, cy + 1, label, size=6, color=MUTED)


def electrolytic(sh, x, y_plus, y_minus, label=None):
    """Radial electrolytic capacitor lying on its side, actual size for 2200 µF 10 V
    (10 × 20 mm). Both legs leave the same end of the body, which lies to the left;
    bend the + leg up to y_plus and the − leg down to y_minus. The − stripe runs along
    the body's lower edge, on the − leg's side."""
    cy = (y_plus + y_minus) / 2
    bw, bl, pitch = 10.0, 20.0, 5.0
    bx1 = x - 2
    bx0 = bx1 - bl
    for leg_y, end_y in ((cy - pitch / 2, y_plus), (cy + pitch / 2, y_minus)):
        sh.polygon([(bx1, leg_y), (x, leg_y), (x, end_y)], stroke=MUTED, width=0.5, closed=False)
    sh.rect(bx0, cy - bw / 2, bx1, cy + bw / 2, stroke=MUTED, fill=WHITE, width=0.3, radius=2)
    sh.rect(bx0 + 1, cy + bw / 2 - 2.8, bx1, cy + bw / 2 - 0.4, stroke=None, fill=FAINT)
    for i in range(4):
        sh.text(bx0 + 4 + i * 4.5, cy + bw / 2 - 0.9, "−", size=6.5, bold=True, color=INK, align="center")
    sh.text(x + 1.8, y_plus + S.TAPE_W / 2 + 3.2, "+", size=7, bold=True)
    if label:
        sh.text((bx0 + bx1) / 2, cy - 1.2, label, size=6, color=MUTED, align="center")


COLOUR_CODE = ("black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "grey", "white")


def colour_code_key(sh, x, y, width=46.0):
    """The resistor colour code in words, so it reads on a black-and-white print."""
    sh.text(x, y, "Colour code", size=7.5, bold=True)
    sh.text(x, y + 3.6, "Band 1, band 2, then that many zeros.", size=6.5, color=MUTED)
    for digit, name in enumerate(COLOUR_CODE):
        cx = x + (digit // 5) * width / 2
        ry = y + 8 + (digit % 5) * 3.3
        sh.runs(cx, ry, [(f"{digit}  ", True), (name, False)], size=6.5)
    sh.text(x, y + 8 + 5 * 3.3 + 0.8, "e.g. yellow-violet-red = 4, 7 + 00 = 4.7 kΩ", size=6.5, color=MUTED)


def spiral(sh, cx, cy, r=1.7, turns=2.5, color=MUTED):
    pts = []
    steps = int(turns * 24)
    for i in range(steps + 1):
        t = i / steps
        a = t * turns * 2 * math.pi
        pts.append((cx + r * t * math.cos(a), cy + r * t * math.sin(a)))
    sh.polygon(pts, stroke=color, width=0.35, closed=False)
