"""M6: Tone, a filter that softens the paper synth's sound.

M1's square wave has sharp edges, and sharp edges are what make it buzz. Here the signal
comes in on the IN lane, through a pencil track, and out to OUT, where C1 leads to GND.
A cut-out wiper joins IN to the track wherever it's pressed, so it sets how much pencil
the signal passes through. Little pencil, and C1 barely notices; more pencil, and C1 has
time to smooth each edge, so the high buzz fades and the tone goes soft and round.

That's a low-pass filter: it passes low notes and cuts high ones. With M7's input as the
load, the corner moves from a few kHz with the wiper near OUT to below 200 Hz at the far
end of a heavy track. A softer sound is quieter too, so turn the amp up a little.

Only GND is used here, for C1. V+ just passes through the ring to the next page.

The page is built in three layers: CIRCUIT says what it is, the functions below say where
things go, and m6_tone.md holds the words.
"""

from .. import elements as E
from .. import lesson
from .. import module
from .. import schematic as sch
from .. import standard as S
from ..circuit import PENCIL, WIRE, C, Circuit
from ..draw import MUTED, Sheet
from ..placement import Placement
from ..provisional import HEADER_STATUS, TAG_NOTE_WITH_T1
from ..words import Words

PAGE_ID = "M6"

CIRCUIT = Circuit(
    PENCIL("Track", track="TRACK", wiper="IN", note="6B pencil"),
    # The bare-wire join from the OUT lane onto the track's right end. It waits on the T1
    # pencil tests (K4 is this join).
    WIRE("W1", "OUT", "TRACK"),
    C("C1", 47e-9, "OUT", "GND"),
)
WORDS = Words.beside(__file__, CIRCUIT)

TRACK = (54.0, 66.0, 172.0, 86.0)  # 118 × 20 mm
IN_Y = S.RING_TOP + S.TAPE_W / 2 + 10
IN_X = (58.0, 160.0)
OUT_X, OUT_TURN_Y, OUT_END_X = 180.0, 146.0, 148.0
BRIDGE_Y = (TRACK[1] + TRACK[3]) / 2
C1_X = 154.0
WIPER = (60.0, 112.0, 76.0, 154.0)
WIPER_STRIP = 34.0
WIPER_GHOST_X = 120.0


def build(path):
    sh = Sheet(path, " ".join(WORDS.title.split()))
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, status=HEADER_STATUS)
    E.spine(sh)
    lay = Placement(sh, CIRCUIT)
    lay.ring()
    _track(lay)
    _parts(lay)
    need = WORDS.items("You need", loops=len(lay.loops))
    module.need(sh, PAGE_ID, need[:3], need[3:])
    module.caption(sh, WORDS.text("Caption"))
    _schematic(sh, lay)
    module.steps(sh, PAGE_ID, WORDS.items("Build it", wiper_strip=f"{WIPER_STRIP:g}"), WORDS.items("Play it"),
                 note=TAG_NOTE_WITH_T1)
    E.footer(sh, PAGE_ID)
    lay.check(listed=WORDS.refs("You need"))
    sh.save()


def _track(lay):
    sh, labels = lay.sh, WORDS.fields("Labels")
    lay.pencil("Track", *TRACK, last_number=110)
    sh.text(TRACK[0], TRACK[3] + 9, labels["soft"], size=6.5, bold=True, color=MUTED)
    sh.text(TRACK[2], TRACK[3] + 9, labels["bright"], size=6.5, bold=True, color=MUTED, align="right")
    gx, half, mid = WIPER_GHOST_X, S.TAPE_W / 2, (IN_Y + TRACK[3]) / 2
    sh.rect(gx - half, mid - WIPER_STRIP / 2, gx + half, mid + WIPER_STRIP / 2, stroke=MUTED, width=0.3,
            dash=(0.8, 0.8))
    sh.text(gx, TRACK[3] + 9, labels["wiper_strip"], size=6, color=MUTED, align="center")
    lay.lane("IN", [(IN_X[0], IN_Y), (IN_X[1], IN_Y)])
    lay.lane("OUT", [(OUT_X, IN_Y), (OUT_X, OUT_TURN_Y), (OUT_END_X, OUT_TURN_Y)])


def _parts(lay):
    sh, labels = lay.sh, WORDS.fields("Labels")
    lay.loop("IN", IN_X[0] + 6, IN_Y, side="above")
    lay.loop("OUT", OUT_X, 112, side="left")
    lay.wire("W1", (OUT_X, BRIDGE_Y), (TRACK[2] - 5, BRIDGE_Y))
    sh.text(OUT_X - 2, BRIDGE_Y - 2.4, labels["wire"], size=6, color=MUTED, align="right")
    gnd_edge = S.RING_BOTTOM - S.TAPE_W / 2
    top = OUT_TURN_Y + S.TAPE_W / 2 - 1
    lay.ceramic_cap("C1", C1_X, (top + gnd_edge + 1) / 2, vertical=True, lead=(gnd_edge + 1 - top) / 2 + 1)
    lay.wiper("Track", *WIPER, WIPER_STRIP)


def _schematic(sh, lay):
    lesson.schematic_panel(sh)
    labels = WORDS.fields("Labels")
    x, box, wiper_y = 66.0, (222.0, 246.0), 234.0
    node, bottom, term_x = 254.0, 272.0, 46.0
    sch.terminal(sh, term_x, wiper_y, "", 0)
    sh.text(term_x - 1.5, wiper_y - 3.4, "IN", size=6.5, bold=True)
    track = lay.symbol("Track")
    sch.rheostat(sh, x, *box, wiper_y, term_x + 0.8, track.ref, track.text)
    sh.text(term_x + 8, wiper_y - 2, labels["wiper"], size=6, color=MUTED)
    lay.symbol("W1")  # the join from the track's end to OUT is this wire
    sch.wire(sh, [(x, box[1]), (x, node), (93.2, node)])
    sch.junction(sh, x, node)
    sch.terminal(sh, 94, node, "OUT", label_y=node - 3.6, align="right")
    c1 = lay.symbol("C1")
    sch.capacitor(sh, x, node, bottom, c1.ref, c1.text, polarised=False)
    sch.wire(sh, [(40.8, bottom), (x, bottom), (x, bottom - 0.01)])
    sch.terminal(sh, 40, bottom, "GND", label_y=bottom + 5)
    lesson.schematic_note(sh, WORDS.text("Schematic note"))
