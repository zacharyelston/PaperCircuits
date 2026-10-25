"""M4: Light pitch, a hands-free controller for the M1 oscillator.

LDR1 is a light-dependent resistor: a few kΩ in bright light, up to a megohm in the dark.
R2 runs from the V+ rail to the upper lane, and LDR1 and R1 sit side by side between that
lane and PITCH. A hand over LDR1 shades it, its resistance climbs, and M1's note falls,
like a theremin you play with shadows.

R1 (68 kΩ) in parallel caps the total, so the darkest shadow still plays a low note
instead of fading out. R2 (10 kΩ) sets the top note and keeps M1 from ever seeing less
than about 10 kΩ, which M5's gate relies on. On paper: about 540 Hz under a lamp, 390 Hz
in room light, and 160 Hz in shadow.

Only V+ is used here. GND just passes through the ring to the next page.
"""

from .. import elements as E
from .. import lesson
from .. import module
from .. import schematic as sch
from .. import standard as S
from ..draw import GUIDE, INK, MUTED, Sheet
from ..provisional import HEADER_STATUS, T0

PAGE_ID = "M4"

# Waiting on the T0 contact tests.
LEAD_STEP = f"Solder every lead to its lane, or hold it flat with a small patch of copper tape. {T0}"
LOOP_STEP = f"Solder a patch loop upright on the PITCH loop mark. {T0}"

R_CAP, R_TOP = "68 kΩ", "10 kΩ"
LDR = "5 mm LDR, such as a GL5528"

LANE_TOP = S.RING_TOP + S.TAPE_W / 2 + 10
R2_X, LDR_X, R1_X = 88.0, 110.0, 134.0
N_Y, P_Y = 84.0, 120.0
P_END = 160.0
LDR_Y = (N_Y + P_Y) / 2
TUBE = (122.0, 136.0, 182.0, 158.0)  # rolls into a tube about 7 mm across
TUBE_FLAP = 6.0


def build(path):
    sh = Sheet(path, "M4 Light pitch")
    E.header(sh, PAGE_ID, "M4  Light pitch",
             "Wave a hand over a light sensor, and the note follows.", status=HEADER_STATUS)
    E.spine(sh)
    module.power_ring(sh)
    _lanes(sh)
    _parts(sh)
    _tube(sh)
    module.need(sh, PAGE_ID, [
        f"LDR1: {LDR}",
        f"R1 {R_CAP} · R2 {R_TOP}",
        "Bare wire for 1 patch loop",
    ], [
        "A clip lead to M1's PITCH",
        "A desk lamp, for the widest range",
        "Copper tape, solder, 2-core cable",
    ])
    module.caption(sh, "Patch PITCH to M1's PITCH. Shade LDR1 for a lower note. Only V+ is used; GND passes through.")
    _schematic(sh)
    module.steps(sh, PAGE_ID, [
        "Lay the power ring and the two lanes inside it, one piece of tape each.",
        "Bend LDR1's legs flat in opposite directions, so its face looks up, and place it across the two "
        "lanes. Either way round.",
        "Place R1 beside it, and R2 from the top rail to the upper lane. Either way round.",
        LEAD_STEP,
        LOOP_STEP,
        "Join the edge connectors to the pages either side with 2-core cable, or with red and black clip leads.",
    ], [
        "Patch PITCH to M1's PITCH. Hold a hand over LDR1 and lower it: the darker, the lower the note.",
        "Cut out the light tube, roll it round a pencil, glue the flap and slip it over LDR1. Now point it "
        "at a lamp to play.",
        "Take R1 out, and a full shadow fades the note to silence.",
    ])
    E.footer(sh, PAGE_ID)
    sh.save()


def _lanes(sh):
    E.lane(sh, [(R2_X, LANE_TOP), (R2_X, N_Y), (R1_X + 6, N_Y)])
    E.lane(sh, [(LDR_X - 6, P_Y), (P_END, P_Y)])


def _parts(sh):
    r_cy = (S.RING_TOP + S.TAPE_W / 2 + LANE_TOP) / 2
    E.resistor(sh, R2_X, r_cy, vertical=True, lead=12, label="R2")
    reach = (P_Y - N_Y) / 2 + 1
    ripples = (7.0, 11.0)
    for r in ripples:
        sh.circle(LDR_X, LDR_Y, r, stroke=GUIDE, width=0.3)
    E.ldr(sh, LDR_X, LDR_Y, lead=reach)
    sh.text(LDR_X - ripples[-1] - 1.5, LDR_Y + 1, "LDR1", size=6, color=MUTED, align="right")
    E.resistor(sh, R1_X, LDR_Y, vertical=True, lead=reach, label="R1")
    sh.text(LDR_X, P_Y + 11, "Hold your hand over LDR1", size=6.5, color=MUTED, align="center")
    E.patch_loop(sh, P_END - 6, P_Y, "PITCH", side="above")


def _tube(sh):
    """A strip to cut out and roll into a tube, so LDR1 only sees light from one way."""
    x0, y0, x1, y1 = TUBE
    sh.rect(x0, y0, x1, y1, stroke=INK, width=0.35)
    sh.line(x1 - TUBE_FLAP, y0, x1 - TUBE_FLAP, y1, width=0.25, color=MUTED, dash=(1, 0.8))
    sh.text(x1 - TUBE_FLAP / 2, (y0 + y1) / 2 + 1, "glue", size=6, color=MUTED, align="center")
    sh.text((x0 + x1 - TUBE_FLAP) / 2, (y0 + y1) / 2 + 1, "Light tube", size=7.5, bold=True, align="center")
    sh.text(x0, y1 + 3.6, "cut out, roll up and slip over LDR1", size=6, color=MUTED)


def _schematic(sh):
    lesson.schematic_panel(sh)
    mid, a, b = 70.0, 60.0, 80.0
    top, split, join, end = 214.0, 236.0, 260.0, 270.0
    sch.terminal(sh, 44, top, "V+", label_y=top - 3.4)
    sch.wire(sh, [(44.8, top), (mid, top), (mid, top + 0.01)])
    sch.resistor(sh, mid, top, split - 4, "R2", R_TOP)
    sch.wire(sh, [(mid, split - 4), (mid, split)])
    sch.junction(sh, mid, split)
    sch.wire(sh, [(a, split), (b, split)])
    sch.ldr(sh, a, split, join, "LDR1", "light")
    sch.resistor(sh, b, split, join, "R1", R_CAP)
    sch.wire(sh, [(a, join), (b, join)])
    sch.junction(sh, mid, join)
    sch.wire(sh, [(mid, join), (mid, end - 1.6)])
    sch.terminal(sh, mid, end, "", 0)
    sh.text(mid + 3, end + 1.2, "PITCH", size=6.5, bold=True)
    lesson.schematic_note(sh, "Less light, more resistance: a lower note on M1.")
