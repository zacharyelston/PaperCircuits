"""Numbers from docs/page-standard.md. Keep the two in step.

Units are mm. The origin is the top-left corner of the front face, x right, y down.
"""

VERSION = "0.1"

PAGE_W, PAGE_H = 210.0, 297.0
PRINT_SAFE = (5.0, 5.0, 205.0, 292.0)

# Spine: four holes, ISO 838 two-hole on the inner pair, 80 mm pitch.
HOLE_X = 12.0
HOLE_D = 6.0
EYELET_FLANGE_D = 10.0
HOLE_KEEP_OUT = 8.0
HOLES = {
    "H1": (28.5, "BUS A"),
    "H2": (108.5, "V+"),
    "H3": (188.5, "GND"),
    "H4": (268.5, "BUS B"),
}
NET_STRIP_START_X = 6.0  # strip starts left of the hole so the flange clamps it all round
SPINE_W = 30.0
BUS_B_GUTTER_X = 24.5
BUS_B_ENTRY_Y = 197.0  # 3.5 mm clear of the GND strip

# Copper tape
TAPE_W = 5.0
WIDE_TAPE_W = 12.0
NET_CLEARANCE = 3.0
JOINT_OVERLAP = 10.0
CROSSING_PATCH = 10.0
PART_GAP = 10.0
TEST_POINT_D = 7.0

# Zones as (x0, y0, x1, y1)
ZONE_HEADER = (30.0, 6.0, 170.0, 22.0)
ZONE_SWITCH = (172.0, 0.0, 210.0, 38.0)
ZONE_BUILD = (34.0, 26.0, 202.0, 200.0)
ZONE_SCHEMATIC = (34.0, 203.0, 98.0, 282.0)
ZONE_WORKBOOK = (102.0, 203.0, 202.0, 282.0)
ZONE_FOOTER = (30.0, 284.0, 202.0, 291.0)

# Switches (standard §6). Every flap pad is a 10 mm piece of 5 mm tape laid across a
# switch pair: two lanes of different nets running 2 mm apart, 7 mm centre to centre.
FLAP_PAD_LEN = 10.0
SWITCH_PAD_GAP = 2.0
PAIR_PITCH = TAPE_W + SWITCH_PAD_GAP

# Corner switch: folding the corner forward reflects the flap across this line.
SWITCH_FOLD = ((172.0, 0.0), (210.0, 38.0))
SWITCH_FLAP_PAD = (196.0, 12.0)

# Tab switch: a flap cut on three sides, hinged 2 mm above the pair it folds onto.
TAB_W, TAB_H = 14.0, 16.0
TAB_HINGE_CLEAR = 2.0

SCALE_BAR = 100.0

# Table-top module pages (standard §10): power enters and leaves at the side edges and runs
# round the build zone as a ring; signals go by clip lead between patch loops.
EDGE_V_Y, EDGE_GND_Y = 135.0, 145.0
EDGE_LEFT_X, EDGE_RIGHT_X = 6.0, 204.0
RING_TOP, RING_BOTTOM = 46.0, 176.0
RING_LEFT = (40.0, 45.0)  # x where V+ climbs and GND drops on the left
RING_RIGHT = (194.0, 189.0)  # x where they come back on the right
PATCH_LOOP = 15.0

# Normative values repeated in docs/page-standard.md. The documentation checker reads
# the compact table there and fails when code and the standard disagree.
DOCUMENTED_VALUES = {
    "VERSION": VERSION,
    "PAGE_W": PAGE_W,
    "PAGE_H": PAGE_H,
    "HOLE_X": HOLE_X,
    "HOLE_D": HOLE_D,
    "HOLE_KEEP_OUT": HOLE_KEEP_OUT,
    "SPINE_W": SPINE_W,
    "TAPE_W": TAPE_W,
    "WIDE_TAPE_W": WIDE_TAPE_W,
    "NET_CLEARANCE": NET_CLEARANCE,
    "JOINT_OVERLAP": JOINT_OVERLAP,
    "PART_GAP": PART_GAP,
    "TEST_POINT_D": TEST_POINT_D,
    "FLAP_PAD_LEN": FLAP_PAD_LEN,
    "SWITCH_PAD_GAP": SWITCH_PAD_GAP,
    "SCALE_BAR": SCALE_BAR,
    "EDGE_V_Y": EDGE_V_Y,
    "EDGE_GND_Y": EDGE_GND_Y,
    "PATCH_LOOP": PATCH_LOOP,
}


def hole_y(hole):
    return HOLES[hole][0]


def reflect_across_fold(x, y):
    (x0, y0), (x1, y1) = SWITCH_FOLD
    dx, dy = x1 - x0, y1 - y0
    t = ((x - x0) * dx + (y - y0) * dy) / (dx * dx + dy * dy)
    fx, fy = x0 + t * dx, y0 + t * dy
    return 2 * fx - x, 2 * fy - y


# Under the corner flap the switch pair is the ends of two vertical lanes, V+ in and
# V+ out; the flap pad lands across them as a horizontal strip.
SWITCH_CENTER = tuple(round(v, 3) for v in reflect_across_fold(*SWITCH_FLAP_PAD))
SWITCH_LANE_X = (SWITCH_CENTER[0] - PAIR_PITCH / 2, SWITCH_CENTER[0] + PAIR_PITCH / 2)
SWITCH_LANE_TOP = SWITCH_CENTER[1] - TAPE_W / 2
