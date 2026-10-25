"""M3: Pencil ribbon, a slide controller for the M1 oscillator.

A wide 6B pencil ribbon is a resistor you play. R1 joins the V+ rail to the ribbon's right
end. The PITCH lane runs alongside, and a cut-out wiper with copper underneath joins the
two wherever it's pressed. Sliding the wiper left puts more pencil between V+ and PITCH,
so M1's note glides down, with no steps between notes.

R1 (13 kΩ) sets the top note, the same high C as M2's keyboard, and keeps M1 from ever
seeing less than 13 kΩ, which M5's gate relies on. A heavy ribbon adds a few tens of kΩ
end to end, so it reaches down more than an octave. Pencil varies, so finding the notes
with a tuner and marking them is part of the page.

Only V+ is used here. GND just passes through the ring to the next page.
"""

from .. import elements as E
from .. import lesson
from .. import module
from .. import schematic as sch
from .. import standard as S
from ..draw import GUIDE, MUTED, Sheet
from ..provisional import HEADER_STATUS, T0, T1, TAG_NOTE_WITH_T1

PAGE_ID = "M3"

# Waiting on the T0 contact tests.
LEAD_STEP = f"Solder R1's top lead to the V+ rail, or hold it flat with a small patch of copper tape. {T0}"
LOOP_STEP = f"Solder a patch loop upright on the PITCH loop mark. {T0}"
# Waiting on the T1 pencil tests (K4 is this join, as on L03).
PENCIL_STEP = (f"Lay R1's bottom lead flat across the right end of the ribbon and hold it down with "
               f"clear tape. {T1}")

R_TOP = "13 kΩ"

RIBBON = (54.0, 66.0, 178.0, 86.0)  # 124 × 20 mm
PITCH_Y = S.RING_TOP + S.TAPE_W / 2 + 10
PITCH_X = (58.0, 166.0)
R1_X = 172.0
FRETS = (54.0, 100.0, 178.0, 108.0)
WIPER = (102.0, 120.0, 118.0, 162.0)
WIPER_GHOST_X = 130.0  # where the outline shows the wiper in use
WIPER_STRIP = 34.0


def build(path):
    sh = Sheet(path, "M3 Pencil ribbon")
    E.header(sh, PAGE_ID, "M3  Pencil ribbon",
             "Slide a wiper along a pencil line, and the note glides.", status=HEADER_STATUS)
    E.spine(sh)
    module.power_ring(sh)
    _ribbon(sh)
    _parts(sh)
    module.need(sh, PAGE_ID, [
        f"R1: {R_TOP}",
        "A soft 6B pencil and an eraser",
        "Card for the wiper, and clear tape",
    ], [
        "Bare wire for 1 patch loop",
        "A clip lead to M1's PITCH",
        "Copper tape, solder, 2-core cable",
    ])
    module.caption(sh, "Patch PITCH to M1's PITCH, then slide the wiper: right is high, left is low. GND passes through.")
    _schematic(sh)
    module.steps(sh, PAGE_ID, [
        "Shade the ribbon hard with the 6B pencil, at least 10 times, until it shines. Rub out any smudge "
        "between it and the PITCH lane.",
        "Lay the power ring and the PITCH lane, one piece of tape each.",
        PENCIL_STEP,
        LEAD_STEP,
        LOOP_STEP,
        f"Cut out the wiper. Stick {WIPER_STRIP:g} mm of tape on it where marked, then turn it copper side down.",
        "Join the edge connectors to the pages either side with 2-core cable, or with red and black clip leads.",
    ], [
        "Patch PITCH to M1's PITCH. Press the wiper across the PITCH lane and the ribbon, and slide it.",
        "Find C4 to C5 with a tuner app and mark them in pen on the fret strip. If the note fades out on "
        "the left, shade that end darker.",
    ], note=TAG_NOTE_WITH_T1)
    E.footer(sh, PAGE_ID)
    sh.save()


def _ribbon(sh):
    E.pencil_track(sh, *RIBBON, last_number=120)
    x0, y0, x1, y1 = FRETS
    sh.rect(x0, y0, x1, y1, stroke=GUIDE, width=0.3, radius=1)
    sh.text(x0 + 2, y1 + 4, "Fret strip: mark the notes here in pen", size=6.5, color=MUTED)
    sh.text(RIBBON[0], RIBBON[3] + 9, "low", size=6.5, bold=True, color=MUTED)
    sh.text(RIBBON[2], RIBBON[3] + 9, "high", size=6.5, bold=True, color=MUTED, align="right")
    # The wiper in use: its copper strip lies across the PITCH lane and the ribbon.
    gx, half, mid = WIPER_GHOST_X, S.TAPE_W / 2, (PITCH_Y + RIBBON[3]) / 2
    sh.rect(gx - half, mid - WIPER_STRIP / 2, gx + half, mid + WIPER_STRIP / 2, stroke=MUTED, width=0.3,
            dash=(0.8, 0.8))
    sh.text(gx, RIBBON[3] + 9, "wiper strip", size=6, color=MUTED, align="center")
    E.lane(sh, [(PITCH_X[0], PITCH_Y), (PITCH_X[1], PITCH_Y)])


def _parts(sh):
    r_cy = (S.RING_TOP + S.TAPE_W / 2 + RIBBON[1]) / 2 + 1
    E.resistor(sh, R1_X, r_cy, vertical=True, lead=12, label="R1")
    E.patch_loop(sh, PITCH_X[0] + 6, PITCH_Y, "PITCH", side="above")
    E.wiper_card(sh, *WIPER, WIPER_STRIP)


def _schematic(sh):
    lesson.schematic_panel(sh)
    x, top = 72.0, 214.0
    sch.terminal(sh, 44, top, "V+", label_y=top - 3.4)
    sch.wire(sh, [(44.8, top), (x, top), (x, top + 0.01)])
    sch.resistor(sh, x, top, 234, "R1", R_TOP)
    box, wiper_y, term_x = (238.0, 264.0), 252.0, 50.0
    sch.wire(sh, [(x, 234), (x, box[0])])
    sch.rheostat(sh, x, *box, wiper_y, term_x + 0.8, "Ribbon", "6B pencil", open_end="bottom")
    sch.terminal(sh, term_x, wiper_y, "", 0)
    sh.text(term_x - 1.5, wiper_y + 5.4, "PITCH on M1", size=6.5, bold=True)
    sh.text(term_x + 8, wiper_y - 2, "wiper", size=6, color=MUTED)
    lesson.schematic_note(sh, "The wiper picks how much ribbon is in the way.")
