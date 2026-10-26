"""M3: Pencil ribbon, a slide controller for the M1 oscillator.

A wide 6B pencil ribbon is a resistor you play. R1 joins the V+ rail to the ribbon's right
end. The PITCH lane runs alongside, and a cut-out wiper with copper underneath joins the
two wherever it's pressed. Sliding the wiper left puts more pencil between V+ and PITCH,
so M1's note glides down, with no steps between notes.

R1 sets the top note, the same high C as M2's keyboard, and keeps M1 from ever seeing less
than 13 kΩ, which M5's gate relies on. A heavy ribbon adds a few tens of kΩ end to end, so
it reaches down more than an octave. Pencil varies, so finding the notes with a tuner and
marking them is part of the page.

Only V+ is used here. GND just passes through the ring to the next page.

The page is built in three layers: CIRCUIT says what it is, the functions below say where
things go, and m3_pencil_ribbon.md holds the words.
"""

from .. import elements as E
from .. import lesson, module
from .. import schematic as sch
from .. import standard as S
from ..circuit import PENCIL, Circuit, R
from ..draw import GUIDE, MUTED, Sheet
from ..placement import Placement
from ..provisional import HEADER_STATUS, TAG_NOTE_WITH_T1
from ..words import Words

PAGE_ID = "M3"

CIRCUIT = Circuit(
    # R1's bottom lead lies on the ribbon's right end. That join waits on the T1 pencil
    # tests (K4 is this join, as on L03).
    R("R1", 13e3, "V+", "RIBBON"),
    PENCIL("Ribbon", track="RIBBON", wiper="PITCH", note="6B pencil"),
)
WORDS = Words.beside(__file__, CIRCUIT)

RIBBON = (54.0, 66.0, 178.0, 86.0)  # 124 × 20 mm
PITCH_Y = S.RING_TOP + S.TAPE_W / 2 + 10
PITCH_X = (58.0, 166.0)
R1_X = 172.0
FRETS = (54.0, 100.0, 178.0, 108.0)
WIPER = (102.0, 120.0, 118.0, 162.0)
WIPER_GHOST_X = 130.0  # where the outline shows the wiper in use
WIPER_STRIP = 34.0


def build(path):
    sh = Sheet(path, " ".join(WORDS.title.split()))
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, status=HEADER_STATUS)
    E.spine(sh)
    lay = Placement(sh, CIRCUIT)
    lay.ring()
    _ribbon(lay)
    _parts(lay)
    need = WORDS.items("You need", loops=len(lay.loops))
    module.need(sh, PAGE_ID, need[:3], need[3:])
    module.caption(sh, WORDS.text("Caption"))
    _schematic(sh, lay)
    module.steps(
        sh,
        PAGE_ID,
        WORDS.items("Build it", wiper_strip=f"{WIPER_STRIP:g}"),
        WORDS.items("Play it"),
        note=TAG_NOTE_WITH_T1,
    )
    E.footer(sh, PAGE_ID)
    lay.check(listed=WORDS.refs("You need"))
    sh.save()


def _ribbon(lay):
    sh, labels = lay.sh, WORDS.fields("Labels")
    lay.pencil("Ribbon", *RIBBON, last_number=120)
    x0, y0, x1, y1 = FRETS
    sh.rect(x0, y0, x1, y1, stroke=GUIDE, width=0.3, radius=1)
    sh.text(x0 + 2, y1 + 4, labels["frets"], size=6.5, color=MUTED)
    sh.text(RIBBON[0], RIBBON[3] + 9, labels["low"], size=6.5, bold=True, color=MUTED)
    sh.text(RIBBON[2], RIBBON[3] + 9, labels["high"], size=6.5, bold=True, color=MUTED, align="right")
    # The wiper in use: its copper strip lies across the PITCH lane and the ribbon.
    gx, half, mid = WIPER_GHOST_X, S.TAPE_W / 2, (PITCH_Y + RIBBON[3]) / 2
    sh.rect(
        gx - half, mid - WIPER_STRIP / 2, gx + half, mid + WIPER_STRIP / 2, stroke=MUTED, width=0.3, dash=(0.8, 0.8)
    )
    sh.text(gx, RIBBON[3] + 9, labels["wiper_strip"], size=6, color=MUTED, align="center")
    lay.lane("PITCH", [(PITCH_X[0], PITCH_Y), (PITCH_X[1], PITCH_Y)])


def _parts(lay):
    r_cy = (S.RING_TOP + S.TAPE_W / 2 + RIBBON[1]) / 2 + 1
    lay.resistor("R1", R1_X, r_cy, vertical=True, lead=12)
    lay.loop("PITCH", PITCH_X[0] + 6, PITCH_Y, side="above")
    lay.wiper("Ribbon", *WIPER, WIPER_STRIP)


def _schematic(sh, lay):
    lesson.schematic_panel(sh)
    labels = WORDS.fields("Labels")
    x, top = 72.0, 214.0
    sch.terminal(sh, 44, top, "V+", label_y=top - 3.4)
    sch.wire(sh, [(44.8, top), (x, top), (x, top + 0.01)])
    r1 = lay.symbol("R1")
    sch.resistor(sh, x, top, 234, r1.ref, r1.text)
    box, wiper_y, term_x = (238.0, 264.0), 252.0, 50.0
    sch.wire(sh, [(x, 234), (x, box[0])])
    ribbon = lay.symbol("Ribbon")
    sch.rheostat(sh, x, *box, wiper_y, term_x + 0.8, ribbon.ref, ribbon.text, open_end="bottom")
    sch.terminal(sh, term_x, wiper_y, "", 0)
    sh.text(term_x - 1.5, wiper_y + 5.4, labels["pitch"], size=6.5, bold=True)
    sh.text(term_x + 8, wiper_y - 2, labels["wiper"], size=6, color=MUTED)
    lesson.schematic_note(sh, WORDS.text("Schematic note"))
