"""M6: Tone, a filter that softens the paper synth's sound.

M1's square wave has sharp edges, and sharp edges are what make it buzz. Here the signal
comes in on the IN lane, through a pencil track, and out to OUT, where C1 (47 nF) leads
to GND. A cut-out wiper joins IN to the track wherever it's pressed, so it sets how much
pencil the signal passes through. Little pencil, and C1 barely notices; more pencil, and
C1 has time to smooth each edge, so the high buzz fades and the tone goes soft and round.

That's a low-pass filter: it passes low notes and cuts high ones. With M7's input as the
load, the corner moves from a few kHz with the wiper near OUT to below 200 Hz at the far
end of a heavy track. A softer sound is quieter too, so turn the amp up a little.

Only GND is used here, for C1. V+ just passes through the ring to the next page.
"""

from .. import elements as E
from .. import lesson
from .. import module
from .. import schematic as sch
from .. import standard as S
from ..draw import MUTED, Sheet
from ..provisional import HEADER_STATUS, T0, T1, TAG_NOTE_WITH_T1

PAGE_ID = "M6"

# Waiting on the T0 contact tests.
LEAD_STEP = f"Solder C1's leads to their lanes, or hold them flat with a small patch of copper tape. {T0}"
LOOP_STEP = f"Solder a patch loop upright on the IN and OUT loop marks. {T0}"
# Waiting on the T1 pencil tests (K4 is this join).
PENCIL_STEP = (f"Lay a short bare wire from the OUT lane onto the track's right end, and hold it down "
               f"with clear tape. {T1}")

CAP = "47 nF"

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
    sh = Sheet(path, "M6 Tone")
    E.header(sh, PAGE_ID, "M6  Tone",
             "A pencil line and a capacitor soften the sound.", status=HEADER_STATUS)
    E.spine(sh)
    module.power_ring(sh)
    _track(sh)
    _parts(sh)
    module.need(sh, PAGE_ID, [
        f"C1: {CAP}, no polarity (ceramic or film)",
        "A soft 6B pencil and an eraser",
        "Card for the wiper, and clear tape",
    ], [
        "Bare wire for 2 patch loops and a join",
        "Copper tape and solder",
        "2-core cable to join the pages",
    ])
    module.caption(sh, "Patch M1's OUT to IN, and OUT to an IN on M7. Slide the wiper left for a softer sound.")
    _schematic(sh)
    module.steps(sh, PAGE_ID, [
        "Shade the track hard with the 6B pencil, at least 10 times, until it shines. Rub out any smudge "
        "between it and the IN lane.",
        "Lay the power ring, the IN lane and the OUT lane, one piece of tape each. Fold at the crease.",
        PENCIL_STEP,
        "Place C1 from the OUT lane to the GND rail, either way round.",
        LEAD_STEP,
        LOOP_STEP,
        f"Cut out the wiper. Stick {WIPER_STRIP:g} mm of tape on it where marked, then turn it copper side down.",
        "Join the edge connectors to the pages either side with 2-core cable, or with red and black clip leads.",
    ], [
        "Patch M1's OUT to IN, and OUT to M7's IN1. Press the wiper across the IN lane and the track.",
        "Near OUT the note buzzes. Slide left and it goes soft and round, and a little quieter.",
    ], note=TAG_NOTE_WITH_T1)
    E.footer(sh, PAGE_ID)
    sh.save()


def _track(sh):
    E.pencil_track(sh, *TRACK, last_number=110)
    sh.text(TRACK[0], TRACK[3] + 9, "soft", size=6.5, bold=True, color=MUTED)
    sh.text(TRACK[2], TRACK[3] + 9, "bright", size=6.5, bold=True, color=MUTED, align="right")
    gx, half, mid = WIPER_GHOST_X, S.TAPE_W / 2, (IN_Y + TRACK[3]) / 2
    sh.rect(gx - half, mid - WIPER_STRIP / 2, gx + half, mid + WIPER_STRIP / 2, stroke=MUTED, width=0.3,
            dash=(0.8, 0.8))
    sh.text(gx, TRACK[3] + 9, "wiper strip", size=6, color=MUTED, align="center")
    E.lane(sh, [(IN_X[0], IN_Y), (IN_X[1], IN_Y)])
    E.lane(sh, [(OUT_X, IN_Y), (OUT_X, OUT_TURN_Y), (OUT_END_X, OUT_TURN_Y)])


def _parts(sh):
    E.patch_loop(sh, IN_X[0] + 6, IN_Y, "IN", side="above")
    E.patch_loop(sh, OUT_X, 112, "OUT", side="left")
    # The bare-wire join from the OUT lane onto the pencil.
    sh.line(OUT_X, BRIDGE_Y, TRACK[2] - 5, BRIDGE_Y, width=0.5, color=MUTED, cap=1)
    sh.text(OUT_X - 2, BRIDGE_Y - 2.4, "wire", size=6, color=MUTED, align="right")
    gnd_edge = S.RING_BOTTOM - S.TAPE_W / 2
    top = OUT_TURN_Y + S.TAPE_W / 2 - 1
    E.ceramic_cap(sh, C1_X, (top + gnd_edge + 1) / 2, vertical=True, lead=(gnd_edge + 1 - top) / 2 + 1,
                  label="C1")
    E.wiper_card(sh, *WIPER, WIPER_STRIP)


def _schematic(sh):
    lesson.schematic_panel(sh)
    x, box, wiper_y = 66.0, (222.0, 246.0), 234.0
    node, bottom, term_x = 254.0, 272.0, 46.0
    sch.terminal(sh, term_x, wiper_y, "", 0)
    sh.text(term_x - 1.5, wiper_y - 3.4, "IN", size=6.5, bold=True)
    sch.rheostat(sh, x, *box, wiper_y, term_x + 0.8, "Track", "6B pencil")
    sh.text(term_x + 8, wiper_y - 2, "wiper", size=6, color=MUTED)
    sch.wire(sh, [(x, box[1]), (x, node), (93.2, node)])
    sch.junction(sh, x, node)
    sch.terminal(sh, 94, node, "OUT", label_y=node - 3.6, align="right")
    sch.capacitor(sh, x, node, bottom, "C1", CAP, polarised=False)
    sch.wire(sh, [(40.8, bottom), (x, bottom), (x, bottom - 0.01)])
    sch.terminal(sh, 40, bottom, "GND", label_y=bottom + 5)
    lesson.schematic_note(sh, "More pencil before C1: a softer sound.")
