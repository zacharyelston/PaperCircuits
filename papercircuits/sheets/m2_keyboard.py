"""M2: Keyboard, a stylus keyboard for the M1 oscillator.

Eight keys, a C major scale from C4 on the left to C5 on the right. A ladder of resistors
runs from the V+ rail down to C5, then key to key towards C4, so each key sits further from
V+ than the one to its right. A clip lead from M1's PITCH is the stylus: touching a key
puts that key's resistance between V+ and PITCH, and M1 plays its note.

Values come from M1's timing, R_pitch = 1 / (0.693 × 100 nF × f) − 14.7 kΩ, rounded to E24.
They land within about 1.5 % on paper; real parts drift, so tuning by ear or with a phone
tuner is part of the page.

Only V+ is used here. GND just passes through the ring to the next page.
"""

from .. import elements as E
from .. import lesson
from .. import module
from .. import schematic as sch
from .. import standard as S
from ..draw import GUIDE, MUTED, Sheet
from ..provisional import HEADER_STATUS, T0

PAGE_ID = "M2"

# Waiting on the T0 contact tests.
LEAD_STEP = f"Solder every lead to its lane, or hold it flat with a small patch of copper tape. {T0}"

NOTES = ("C", "D", "E", "F", "G", "A", "B", "C")
# R1 runs from V+ to the top C; R2 to R8 join neighbouring keys, right to left.
R_TOP = "13 kΩ"
LADDER = ("1.6 kΩ", "3.6 kΩ", "3.9 kΩ", "4.3 kΩ", "2.4 kΩ", "5.1 kΩ", "6.2 kΩ")

KEY_X = tuple(58.0 + 16 * i for i in range(8))
KEY_TOP, KEY_BOTTOM = S.RING_TOP + S.TAPE_W / 2 + 10, 158.0
LADDER_Y = (68.0, 80.0)  # alternate rows, so leads sharing a key don't overlap


def build(path):
    sh = Sheet(path, "M2 Keyboard")
    E.header(sh, PAGE_ID, "M2  Keyboard",
             "Touch a key with the stylus lead from M1 to play a note.", status=HEADER_STATUS)
    E.spine(sh)
    module.power_ring(sh)
    _keys(sh)
    module.need(sh, PAGE_ID, [
        f"R1 {R_TOP} · R2 {LADDER[0]} · R3 {LADDER[1]}",
        f"R4 {LADDER[2]} · R5 {LADDER[3]} · R6 {LADDER[4]}",
        f"R7 {LADDER[5]} · R8 {LADDER[6]}",
    ], [
        "A clip lead from M1's PITCH: the stylus",
        "Copper tape and solder",
        "2-core cable to join the pages",
    ])
    module.caption(sh, "Touch anywhere on a key. Low C on the left, high C on the right. Only V+ is used; GND passes through.")
    _schematic(sh)
    module.steps(sh, PAGE_ID, [
        "Lay the power ring and the eight key lanes, one piece of tape each.",
        "Place R1 from the top rail to the high C on the right. Place R2 to R8 between the keys, "
        "right to left, as labelled. Either way round.",
        LEAD_STEP,
        "Join the edge connectors to the pages either side with 2-core cable, or with red and black clip leads.",
    ], [
        "Clip one end of a lead to M1's PITCH loop. Hold the other clip by its cover and touch its jaws to a key.",
        "Check each note with a tuner app on a phone. A note that's off can be tuned by swapping the "
        "resistor to its right for the next value up or down.",
    ])
    E.footer(sh, PAGE_ID)
    sh.save()


def _keys(sh):
    for i, (x, note) in enumerate(zip(KEY_X, NOTES)):
        sh.rect(x - 7.5, KEY_TOP - 4, x + 7.5, KEY_BOTTOM + 10, stroke=GUIDE, width=0.3, radius=1.5)
        E.lane(sh, [(x, KEY_TOP), (x, KEY_BOTTOM)])
        octave = "5" if i == len(NOTES) - 1 else "4"
        sh.text(x, KEY_BOTTOM + 7, f"{note}{octave}", size=7.5, bold=True, align="center")
    r_cy = (S.RING_TOP + S.TAPE_W / 2 + KEY_TOP) / 2
    E.resistor(sh, KEY_X[-1], r_cy, vertical=True, lead=12, label=f"R1 {R_TOP}")
    for i, value in enumerate(LADDER):
        right, left = KEY_X[-1 - i], KEY_X[-2 - i]
        E.resistor(sh, (left + right) / 2, LADDER_Y[i % 2], vertical=False, lead=10, label=f"R{i + 2}")


def _schematic(sh):
    lesson.schematic_panel(sh)
    top, ladder_y, key_y = 216.0, 244.0, 252.0
    xs = [40.0 + 7.5 * i for i in range(8)]
    sch.terminal(sh, 40, top, "V+", label_y=top - 3.4)
    sch.wire(sh, [(40.8, top), (xs[-1], top)])
    sch.resistor(sh, xs[-1], top, ladder_y, "", "")
    sh.text(xs[-1] - 2.6, (top + ladder_y) / 2 - 0.4, "R1", size=6.5, bold=True, align="right")
    sh.text(xs[-1] - 2.6, (top + ladder_y) / 2 + 2.8, R_TOP, size=6, color=MUTED, align="right")
    for i in range(7):
        right, left = xs[-1 - i], xs[-2 - i]
        sch.resistor_h(sh, left, right, ladder_y, f"R{i + 2}", box_w=4.2)
    for i, (x, note) in enumerate(zip(xs, NOTES)):
        sch.junction(sh, x, ladder_y)
        sch.wire(sh, [(x, ladder_y), (x, key_y - 0.9)])
        sh.circle(x, key_y, 1.8, stroke=sch.INK, fill=sch.WHITE, width=sch.W)
        sh.text(x, key_y + 5, note, size=6.5, bold=True, align="center")
    sch.terminal(sh, 66, 270, "", 0)
    sh.line(66, 269.2, xs[2], key_y + 0.9, width=0.3, color=MUTED, dash=(1, 0.8))
    sh.text(68, 271.2, "PITCH on M1", size=6.5, bold=True)
    sh.text(56, 266, "stylus", size=6, color=MUTED, align="right")
    lesson.schematic_note(sh, "Each key further left adds a resistor: a lower note.")
