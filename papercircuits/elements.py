"""Standard page elements: spine, header, footer, tape lanes, marks and part footprints."""

import math

from . import standard as S
from .circuit import COLOUR_CODE
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


def hole(
    sh,
    hole_id,
    connected=True,
    strip_width=S.TAPE_W,
    label_below=False,
    mechanical=False,
    show_label=True,
    holes=None,
):
    """Punch guide with eyelet flange ring and the hole's net name. A V2 page's holes are
    `mechanical`: they only bind the page, so the label says it has no net."""
    y, net = (holes or S.HOLES)[hole_id]
    x = S.HOLE_X
    sh.circle(x, y, S.EYELET_FLANGE_D, stroke=GUIDE, width=0.2, dash=(0.8, 0.8))
    sh.circle(x, y, S.HOLE_D, stroke=INK, fill=WHITE, width=0.3)
    arm = S.HOLE_D / 2 + 1.5
    sh.line(x - arm, y, x + arm, y, width=0.15, color=INK)
    sh.line(x, y - arm, x, y + arm, width=0.15, color=INK)
    if show_label:
        if mechanical:
            tag = f"{hole_id} · no net"
        else:
            tag = f"{hole_id} {net}" if connected else f"{hole_id} {net} · NC"
        label_y = y + strip_width / 2 + 3.8 if label_below else y - strip_width / 2 - 1.7
        sh.text(x + 6.5, label_y, tag, size=6, color=MUTED)


def spine(
    sh,
    connected=(),
    strip_widths=None,
    edge=False,
    labels_below=(),
    mechanical=False,
    show_labels=True,
    holes=None,
):
    """All holes in the selected pattern, optionally the spine edge. `connected` lists hole ids that carry a net strip;
    `labels_below` moves a hole's net name under its strip (H4 when Bus B climbs the gutter).
    `mechanical` labels every hole as having no net, for V2 pages, whose holes only bind.
    Dense procedure/results pages may set `show_labels=False` while keeping the punch guides."""
    if mechanical and connected:
        raise ValueError("a mechanical spine cannot connect binder holes to electrical nets")
    strip_widths = strip_widths or {}
    holes = holes or S.HOLES
    if edge:
        sh.line(S.SPINE_W, 26, S.SPINE_W, 280, width=0.15, color=GUIDE, dash=(0.4, 1.6))
    for hole_id in holes:
        hole(
            sh,
            hole_id,
            connected=hole_id in connected,
            strip_width=strip_widths.get(hole_id, S.TAPE_W),
            label_below=hole_id in labels_below,
            mechanical=mechanical,
            show_label=show_labels,
            holes=holes,
        )


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
    sh.text(
        x1, bar_y + 3.6, f"PaperCircuits page standard v{S.VERSION} · {page_id}", size=6, color=MUTED, align="right"
    )


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
    `stubs` draws short ones for pages that don't route those lanes. Returns the two
    points the flap pad presses on, one on each lane."""
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
    return [((x, cy), (x, cy)) for x in S.SWITCH_LANE_X]


def tab_switch(sh, x, upper_y, label, pitch=S.PAIR_PITCH):
    """Tab switch over a horizontal switch pair whose upper lane is centred on upper_y and
    whose lower lane is `pitch` below it. The flap is cut above the pair and hinges down
    onto it; its pad lands across both lanes as a vertical strip. Returns the two points
    the pad presses on, one on each lane."""
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
    return [((x, y), (x, y)) for y in (upper_y, upper_y + pitch)]


def pencil_track(sh, x0, y0, x1, y1, tick=10.0, last_number=None):
    """A band to shade with a soft pencil: solid outline, light hatching, and a tick every
    `tick` mm under it, numbered in mm from 0 at x0 up to `last_number`. tick=None
    leaves the ruler off."""
    step = 2.0
    c = x0 + y0 + step
    while c < x1 + y1:
        xa, xb = max(x0, c - y1), min(x1, c - y0)
        if xa < xb:
            sh.line(xa, c - xa, xb, c - xb, width=0.15, color=GUIDE)
        c += step
    sh.rect(x0, y0, x1, y1, stroke=INK, width=0.35)
    if tick is None:
        return
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


def registration_mark(sh, x, y, label, scale=False):
    """A crosshair for checking two-sided printing. On the back, scale=True adds 1 mm ticks
    along both arms, so a pin pushed through the front mark shows the offset in mm."""
    arm = 4.5 if scale else 3.0
    sh.circle(x, y, 4.0, stroke=INK, width=0.25)
    sh.line(x - arm, y, x + arm, y, width=0.15)
    sh.line(x, y - arm, x, y + arm, width=0.15)
    if scale:
        for i in (-4, -3, -2, -1, 1, 2, 3, 4):
            t = 1.1 if i % 2 == 0 else 0.6
            sh.line(x + i, y - t, x + i, y + t, width=0.12)
            sh.line(x - t, y + i, x + t, y + i, width=0.12)
    sh.text(x, y + 7.5, label, size=6, bold=True, align="center")


VIA_KINDS = ("slit", "wire", "eyelet", "mark")


def via(sh, x, y, kind):
    """Where a horizontal lane passes to the other side of the page. "slit": cut here and
    thread the tape through. "wire": push a bare wire through and solder both sides.
    "eyelet": set a small eyelet through both lanes. "mark": your own method."""
    if kind == "slit":
        sh.rect(x - 0.4, y - 3.5, x + 0.4, y + 3.5, stroke=None, fill=INK)
    elif kind == "wire":
        sh.circle(x, y, 4.0, stroke=INK, width=0.25, dash=(0.6, 0.6))
        sh.circle(x, y, 1.2, stroke=None, fill=INK)
    elif kind == "eyelet":
        sh.circle(x, y, 7.0, stroke=GUIDE, width=0.2, dash=(0.8, 0.8))
        sh.circle(x, y, 3.5, stroke=INK, fill=WHITE, width=0.3)
    else:
        sh.circle(x, y, 3.0, stroke=INK, width=0.3)


# Part footprints, actual size.


def resistor(sh, cx, cy, vertical=True, lead=11.0, label=None):
    """1/4 W resistor: 6.3 × 2.4 mm body, leads reaching `lead` mm from the centre.
    Returns its two leads as segments from tip to body, top or left one first."""
    bl, bw = 6.3, 2.4
    if vertical:
        sh.line(cx, cy - lead, cx, cy + lead, width=0.6, color=MUTED, cap=1)
        sh.rect(cx - bw / 2, cy - bl / 2, cx + bw / 2, cy + bl / 2, stroke=MUTED, fill=WHITE, width=0.3, radius=1)
        for d in (-1.6, -0.6, 0.4):
            sh.line(cx - bw / 2, cy + d, cx + bw / 2, cy + d, width=0.35, color=MUTED)
        if label:
            sh.text(cx + bw / 2 + 1, cy + 1, label, size=6, color=MUTED)
        return _leads(cx, cy, 0, 1, lead, bl / 2)
    sh.line(cx - lead, cy, cx + lead, cy, width=0.6, color=MUTED, cap=1)
    sh.rect(cx - bl / 2, cy - bw / 2, cx + bl / 2, cy + bw / 2, stroke=MUTED, fill=WHITE, width=0.3, radius=1)
    for d in (-1.6, -0.6, 0.4):
        sh.line(cx + d, cy - bw / 2, cx + d, cy + bw / 2, width=0.35, color=MUTED)
    if label:
        sh.text(cx, cy - S.TAPE_W / 2 - 1.1, label, size=6, color=MUTED, align="center")
    return _leads(cx, cy, 1, 0, lead, bl / 2)


def _leads(cx, cy, dx, dy, lead, body):
    """A two-lead part's leads along (dx, dy), each from its tip to the body's edge."""
    return [
        ((cx - dx * lead, cy - dy * lead), (cx - dx * body, cy - dy * body)),
        ((cx + dx * body, cy + dy * body), (cx + dx * lead, cy + dy * lead)),
    ]


def led(sh, cx, cy, anode="left", lead_anode=12.0, lead_cathode=9.0, label=None):
    """5 mm LED seen from above, legs splayed flat. The anode (long leg, +) points
    `anode`: left, right, up or down. Returns its leads by name, each from tip to body."""
    dx, dy = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}[anode]
    sh.line(
        cx + dx * lead_anode,
        cy + dy * lead_anode,
        cx - dx * lead_cathode,
        cy - dy * lead_cathode,
        width=0.5,
        color=MUTED,
        cap=1,
    )
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
    r = 5.8 / 2
    return {
        "anode": ((cx + dx * lead_anode, cy + dy * lead_anode), (cx + dx * r, cy + dy * r)),
        "cathode": ((cx - dx * r, cy - dy * r), (cx - dx * lead_cathode, cy - dy * lead_cathode)),
    }


def ptc(sh, cx, cy, lead=12.0, label=None):
    """Radial resettable fuse laid flat, legs splayed left and right."""
    bw, bh = 7.5, 6.0
    sh.line(cx - lead, cy, cx + lead, cy, width=0.5, color=MUTED, cap=1)
    sh.rect(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2, stroke=MUTED, fill=WHITE, width=0.3, radius=2)
    sh.text(cx, cy + 1, "PTC", size=6, color=MUTED, align="center")
    if label:
        sh.text(cx, cy - bh / 2 - 1.2, label, size=6, color=MUTED, align="center")
    return _leads(cx, cy, 1, 0, lead, bw / 2)


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
    """Insulated wire running left from x_from; its last `strip` mm, ending at x_to, is bare.
    Returns the bare end."""
    bare = x_to + strip
    sh.line(x_from, y, bare, y, width=1.4, color=MUTED, cap=1)
    sh.line(bare, y, x_to, y, width=0.5, color=INK, cap=1)
    return ((bare, y), (x_to, y))


def checkbox(sh, x, y, size=3.0):
    """A tick box sitting on the text baseline y."""
    sh.rect(x, y - size + 0.4, x + size, y + 0.4, stroke=INK, width=0.3)


def transistor(sh, cx, cy, legs, label=None):
    """TO-92 transistor lying flat face up, with its legs bent out to where they land.
    `legs` maps "E", "B" and "C" to (x, y). For a 2N3904 seen flat face up with the legs
    towards you, they come out E, B, C from left to right. Returns each leg by name, from
    where it leaves the body to its end."""
    for x, y in legs.values():
        sh.line(cx, cy, x, y, width=0.5, color=MUTED, cap=1)
    w, h = 5.0, 4.2
    sh.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, stroke=MUTED, fill=WHITE, width=0.3, radius=1.6)
    sh.line(cx - w / 2 + 0.7, cy - h / 2 + 1.0, cx + w / 2 - 0.7, cy - h / 2 + 1.0, width=0.25, color=MUTED)
    for name, (x, y) in legs.items():
        dx, dy = x - cx, y - cy
        n = math.hypot(dx, dy) or 1.0
        sh.text(x + dx / n * 2.8, y + dy / n * 2.8 + 1.1, name, size=6, bold=True, align="center")
    if label:
        sh.text(cx + w / 2 + 1.2, cy - h / 2 - 0.8, label, size=6, color=MUTED)
    out = {}
    for name, (x, y) in legs.items():
        n = math.hypot(x - cx, y - cy) or 1.0
        out[name] = ((cx + (x - cx) / n * 2.5, cy + (y - cy) / n * 2.5), (x, y))
    return out


def ceramic_cap(sh, cx, cy, vertical=False, lead=8.0, label=None):
    """Disc ceramic or film capacitor: no polarity, either way round. Returns its two
    leads, as resistor() does."""
    if vertical:
        sh.line(cx, cy - lead, cx, cy + lead, width=0.5, color=MUTED, cap=1)
    else:
        sh.line(cx - lead, cy, cx + lead, cy, width=0.5, color=MUTED, cap=1)
    sh.circle(cx, cy, 5.0, stroke=MUTED, fill=WHITE, width=0.3)
    if label:
        if vertical:
            sh.text(cx + 3.6, cy + 1, label, size=6, color=MUTED)
        else:
            sh.text(cx, cy - S.TAPE_W / 2 - 1.1, label, size=6, color=MUTED, align="center")
    return _leads(cx, cy, 0, 1, lead, 5.0) if vertical else _leads(cx, cy, 1, 0, lead, 5.0)


def radial_cap(sh, x_plus, x_minus, y, label=None, body=(5.0, 11.0)):
    """Small radial electrolytic capacitor, such as 10 µF 16 V (5 × 11 mm), lying on its
    side with its body pointing up the page. Both legs leave its bottom end; bend the +
    leg out to x_plus and the − leg to x_minus, along y. The − stripe runs down the
    body's side nearer the − leg. Returns the legs' ends by name: plus, minus."""
    bw, bl = body
    cx = (x_plus + x_minus) / 2
    s = 1 if x_minus > x_plus else -1
    by1 = y - 2.0
    by0 = by1 - bl
    for leg_x, end_x in ((cx - s, x_plus), (cx + s, x_minus)):
        sh.polygon([(leg_x, by1), (leg_x, y), (end_x, y)], stroke=MUTED, width=0.5, closed=False)
    sh.rect(cx - bw / 2, by0, cx + bw / 2, by1, stroke=MUTED, fill=WHITE, width=0.3, radius=1.2)
    sx0, sx1 = sorted((cx + s * (bw / 2 - 1.5), cx + s * (bw / 2 - 0.3)))
    sh.rect(sx0, by0 + 0.8, sx1, by1 - 0.4, stroke=None, fill=FAINT)
    for sign, mark in ((-s, "+"), (s, "−")):
        sh.text(cx + sign * (bw / 2 + 1.6), by1 - 0.6, mark, size=7, bold=True, align="center")
    if label:
        sh.text(cx, by0 - 1.4, label, size=6, color=MUTED, align="center")
    return {"plus": ((cx - s, y), (x_plus, y)), "minus": ((cx + s, y), (x_minus, y))}


def ldr(sh, cx, cy, lead=11.0, label=None):
    """Light-dependent resistor: a 5 mm disc lying face up, its two legs bent flat in
    opposite directions to reach `lead` mm above and below its centre. Either way round."""
    sh.line(cx, cy - lead, cx, cy + lead, width=0.6, color=MUTED, cap=1)
    r = 2.6
    sh.circle(cx, cy, r, stroke=MUTED, fill=WHITE, width=0.3)
    pts = []
    for i in range(7):
        y = cy - 1.5 + i * 0.5
        row = [(cx - 1.5, y), (cx + 1.5, y)]
        pts += row if i % 2 == 0 else row[::-1]
    sh.polygon(pts, stroke=MUTED, width=0.25, closed=False)
    if label:
        sh.text(cx + r + 1, cy + 1, label, size=6, color=MUTED)
    return _leads(cx, cy, 0, 1, lead, r / 2)


def patch_loop(sh, x, y, label, side="right"):
    """Where to solder a patch loop on a lane: an upright U of bare wire a clip can grip.
    Returns the segment between its two feet."""
    pts = [(x - 2.2 + 4.4 * i / 12, y - 2.8 * math.sin(math.pi * i / 12)) for i in range(13)]
    sh.polygon(pts, stroke=INK, width=0.5, closed=False)
    for fx in (x - 2.2, x + 2.2):
        sh.circle(fx, y, 1.0, stroke=None, fill=INK)
    if side == "right":
        sh.text(x + 4.2, y + 1.1, label, size=6.5, bold=True)
    elif side == "left":
        sh.text(x - 4.2, y + 1.1, label, size=6.5, bold=True, align="right")
    else:
        sh.text(x, y - 4.6, label, size=6.5, bold=True, align="center")
    return ((x - 2.2, y), (x + 2.2, y))


def diode(sh, cx, cy, lead=8.0, label=None, cathode="right"):
    """Small-signal diode (1N4148 size). The band marks the cathode, which points
    `cathode`: right, left, up or down. Returns its leads by name, as led() does."""
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
    dx, dy = {"right": (1, 0), "left": (-1, 0), "down": (0, 1), "up": (0, -1)}[cathode]
    return {
        "anode": ((cx - dx * lead, cy - dy * lead), (cx - dx * bl / 2, cy - dy * bl / 2)),
        "cathode": ((cx + dx * bl / 2, cy + dy * bl / 2), (cx + dx * lead, cy + dy * lead)),
    }


def electrolytic(sh, x, y_plus, y_minus, label=None):
    """Radial electrolytic capacitor lying on its side, actual size for 2200 µF 10 V
    (10 × 20 mm). Both legs leave the same end of the body, which lies to the left;
    bend the + leg up to y_plus and the − leg down to y_minus. The − stripe runs along
    the body's lower edge, on the − leg's side. Returns the legs' ends by name: plus, minus."""
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
    return {"plus": ((x, cy - pitch / 2), (x, y_plus)), "minus": ((x, cy + pitch / 2), (x, y_minus))}


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
