"""M4: Light pitch, a hands-free controller for the M1 oscillator.

LDR1 is a light-dependent resistor: a few kΩ in bright light, up to a megohm in the dark.
R2 runs from the V+ rail to the upper lane, and LDR1 and R1 sit side by side between that
lane and PITCH. A hand over LDR1 shades it, its resistance climbs, and M1's note falls,
like a theremin you play with shadows.

R1 in parallel caps the total, so the darkest shadow still plays a low note instead of
fading out. R2 sets the top note and keeps M1 from ever seeing less than about 10 kΩ,
which M5's gate relies on. On paper: about 540 Hz under a lamp, 390 Hz in room light,
and 160 Hz in shadow.

Only V+ is used here. GND just passes through the ring to the next page.

The page is built in three layers: CIRCUIT says what it is, the functions below say where
things go, and m4_light_pitch.md holds the words.
"""

from .. import elements as E
from .. import lesson, module
from .. import schematic as sch
from .. import standard as S
from ..circuit import LDR, Circuit, R
from ..draw import GUIDE, INK, MUTED, Sheet
from ..placement import Placement
from ..provisional import HEADER_STATUS
from ..words import Words, number

PAGE_ID = "M4"

# N1 is the upper lane, where R2 meets LDR1 and R1.
CIRCUIT = Circuit(
    LDR("LDR1", "N1", "PITCH", note="5 mm LDR, such as a GL5528"),
    R("R1", 68e3, "N1", "PITCH"),
    R("R2", 10e3, "V+", "N1"),
)
WORDS = Words.beside(__file__, CIRCUIT)

LANE_TOP = S.RING_TOP + S.TAPE_W / 2 + 10
R2_X, LDR_X, R1_X = 88.0, 110.0, 134.0
N_Y, P_Y = 84.0, 120.0
P_END = 160.0
LDR_Y = (N_Y + P_Y) / 2
TUBE = (122.0, 136.0, 182.0, 158.0)  # rolls into a tube about 7 mm across
TUBE_FLAP = 6.0


def build(path):
    sh = Sheet(path, " ".join(WORDS.title.split()))
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, status=HEADER_STATUS)
    E.spine(sh)
    lay = Placement(sh, CIRCUIT)
    lay.ring()
    _lanes(lay)
    _parts(lay)
    _tube(sh)
    need = WORDS.items("You need", loops=len(lay.loops))
    module.need(sh, PAGE_ID, need[:3], need[3:])
    module.caption(sh, WORDS.text("Caption"))
    _schematic(sh, lay)
    module.steps(sh, PAGE_ID, WORDS.items("Build it", lanes=number(lay.laid)), WORDS.items("Play it"))
    E.footer(sh, PAGE_ID)
    lay.check(listed=WORDS.refs("You need"))
    sh.save()


def _lanes(lay):
    lay.lane("N1", [(R2_X, LANE_TOP), (R2_X, N_Y), (R1_X + 6, N_Y)])
    lay.lane("PITCH", [(LDR_X - 6, P_Y), (P_END, P_Y)])


def _parts(lay):
    sh, labels = lay.sh, WORDS.fields("Labels")
    r_cy = (S.RING_TOP + S.TAPE_W / 2 + LANE_TOP) / 2
    lay.resistor("R2", R2_X, r_cy, vertical=True, lead=12)
    reach = (P_Y - N_Y) / 2 + 1
    ripples = (7.0, 11.0)
    for r in ripples:
        sh.circle(LDR_X, LDR_Y, r, stroke=GUIDE, width=0.3)
    lay.ldr("LDR1", LDR_X, LDR_Y, lead=reach, label=None)
    sh.text(LDR_X - ripples[-1] - 1.5, LDR_Y + 1, CIRCUIT["LDR1"].ref, size=6, color=MUTED, align="right")
    lay.resistor("R1", R1_X, LDR_Y, vertical=True, lead=reach)
    sh.text(LDR_X, P_Y + 11, labels["hand"], size=6.5, color=MUTED, align="center")
    lay.loop("PITCH", P_END - 6, P_Y, side="above")


def _tube(sh):
    """A strip to cut out and roll into a tube, so LDR1 only sees light from one way."""
    labels = WORDS.fields("Labels")
    x0, y0, x1, y1 = TUBE
    sh.rect(x0, y0, x1, y1, stroke=INK, width=0.35)
    sh.line(x1 - TUBE_FLAP, y0, x1 - TUBE_FLAP, y1, width=0.25, color=MUTED, dash=(1, 0.8))
    sh.text(x1 - TUBE_FLAP / 2, (y0 + y1) / 2 + 1, labels["glue"], size=6, color=MUTED, align="center")
    sh.text((x0 + x1 - TUBE_FLAP) / 2, (y0 + y1) / 2 + 1, labels["tube"], size=7.5, bold=True, align="center")
    sh.text(x0, y1 + 3.6, labels["tube_steps"], size=6, color=MUTED)


def _schematic(sh, lay):
    lesson.schematic_panel(sh)
    mid, a, b = 70.0, 60.0, 80.0
    top, split, join, end = 214.0, 236.0, 260.0, 270.0
    sch.terminal(sh, 44, top, "V+", label_y=top - 3.4)
    sch.wire(sh, [(44.8, top), (mid, top), (mid, top + 0.01)])
    r2 = lay.symbol("R2")
    sch.resistor(sh, mid, top, split - 4, r2.ref, r2.text)
    sch.wire(sh, [(mid, split - 4), (mid, split)])
    sch.junction(sh, mid, split)
    sch.wire(sh, [(a, split), (b, split)])
    sch.ldr(sh, a, split, join, lay.symbol("LDR1").ref, WORDS.fields("Labels")["ldr"])
    r1 = lay.symbol("R1")
    sch.resistor(sh, b, split, join, r1.ref, r1.text)
    sch.wire(sh, [(a, join), (b, join)])
    sch.junction(sh, mid, join)
    sch.wire(sh, [(mid, join), (mid, end - 1.6)])
    sch.terminal(sh, mid, end, "", 0)
    sh.text(mid + 3, end + 1.2, "PITCH", size=6.5, bold=True)
    lesson.schematic_note(sh, WORDS.text("Schematic note"))
