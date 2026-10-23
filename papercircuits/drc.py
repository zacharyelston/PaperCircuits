"""Design-rule check: copper lanes must stay NET_CLEARANCE apart.

Every lane on a page is its own node (standard §4: one strip per node), so two lanes
closer than the clearance are a fault: a likely short when built by hand. The only
exceptions are declared ones: a switch pair may sit SWITCH_PAD_GAP apart, and an
insulated crossing may touch.
"""

import math

from . import standard as S


def _point_seg(p, a, b):
    ax, ay = a
    dx, dy = b[0] - ax, b[1] - ay
    n = dx * dx + dy * dy
    t = 0.0 if n == 0 else max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / n))
    return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)


def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _segments_cross(a, b, c, d):
    d1, d2 = _cross(c, d, a), _cross(c, d, b)
    d3, d4 = _cross(a, b, c), _cross(a, b, d)
    return (d1 > 0) != (d2 > 0) and (d3 > 0) != (d4 > 0)


def _inside(p, poly):
    x, y = p
    hit = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            hit = not hit
    return hit


def distance(a, b):
    """Shortest distance between two simple polygons; 0 if they touch or overlap."""
    edges_a = list(zip(a, a[1:] + a[:1]))
    edges_b = list(zip(b, b[1:] + b[:1]))
    if _inside(a[0], b) or _inside(b[0], a):
        return 0.0
    best = math.inf
    for p, q in edges_a:
        for r, s in edges_b:
            if _segments_cross(p, q, r, s):
                return 0.0
            best = min(best, _point_seg(p, r, s), _point_seg(q, r, s), _point_seg(r, p, q), _point_seg(s, p, q))
    return best


def violations(lanes, allowed):
    """Lane pairs closer than allowed. `allowed` maps (i, j) with i < j to the smallest
    distance that pair may have; every other pair needs NET_CLEARANCE."""
    found = []
    for i in range(len(lanes)):
        for j in range(i + 1, len(lanes)):
            limit = allowed.get((i, j), S.NET_CLEARANCE)
            d = distance(lanes[i], lanes[j])
            if d < limit - 0.01:
                found.append((i, j, d, limit))
    return found
