"""M2: Keyboard, a stylus keyboard for the M1 oscillator.

Eight keys, a C major scale from C4 on the left to C5 on the right. A ladder of resistors
runs from the V+ rail down to C5, then key to key towards C4, so each key sits further from
V+ than the one to its right. A clip lead from M1's PITCH is the stylus: touching a key
puts that key's resistance between V+ and PITCH, and M1 plays its note.

Values come from M1's timing, R_pitch = 1 / (0.693 × 100 nF × f) − 14.7 kΩ, rounded to E24.
They land within about 1.5 % on paper; real parts drift, so tuning by ear or with a phone
tuner is part of the page.

Only V+ is used here. GND just passes through the ring to the next page.

The page is built in three layers: CIRCUIT says what it is, _keys() and _schematic() say
where things go, and m2_keyboard.md holds the words.
"""

from .. import elements as E
from .. import lesson, module
from .. import schematic as sch
from .. import standard as S
from ..circuit import Circuit, R
from ..draw import GUIDE, MUTED, Sheet
from ..placement import Placement
from ..provisional import HEADER_STATUS
from ..words import Words, number

PAGE_ID = "M2"

NOTES = ("C", "D", "E", "F", "G", "A", "B", "C")
# Each key's lane is its own net, named for its note: C4 on the left up to C5.
KEYS = tuple(f"{note}{5 if i == len(NOTES) - 1 else 4}" for i, note in enumerate(NOTES))

# R1 runs from V+ to the top C; R2 to R8 join neighbouring keys, right to left.
CIRCUIT = Circuit(
    R("R1", 13e3, "V+", "C5"),
    R("R2", 1.6e3, "C5", "B4"),
    R("R3", 3.6e3, "B4", "A4"),
    R("R4", 3.9e3, "A4", "G4"),
    R("R5", 4.3e3, "G4", "F4"),
    R("R6", 2.4e3, "F4", "E4"),
    R("R7", 5.1e3, "E4", "D4"),
    R("R8", 6.2e3, "D4", "C4"),
    controller=True,
    controller_outputs=KEYS,
)
WORDS = Words.beside(__file__, CIRCUIT)

KEY_X = tuple(58.0 + 16 * i for i in range(8))
KEY_TOP, KEY_BOTTOM = S.RING_TOP + S.TAPE_W / 2 + 10, 158.0
LADDER_Y = (68.0, 80.0)  # alternate rows, so leads sharing a key don't overlap


def build(path):
    sh = Sheet(path, " ".join(WORDS.title.split()))
    E.header(sh, PAGE_ID, WORDS.title, WORDS.subtitle, status=HEADER_STATUS)
    E.spine(sh)
    lay = Placement(sh, CIRCUIT)
    lay.ring()
    _keys(lay)
    need = WORDS.items("You need")
    module.need(sh, PAGE_ID, need[:3], need[3:])
    module.caption(sh, WORDS.text("Caption"))
    _schematic(sh, lay)
    module.steps(sh, PAGE_ID, WORDS.items("Build it", lanes=number(lay.laid)), WORDS.items("Play it"))
    E.footer(sh, PAGE_ID)
    lay.check(listed=WORDS.refs("You need"))
    sh.save()


def _keys(lay):
    sh = lay.sh
    for x, key in zip(KEY_X, KEYS):
        sh.rect(x - 7.5, KEY_TOP - 4, x + 7.5, KEY_BOTTOM + 10, stroke=GUIDE, width=0.3, radius=1.5)
        lay.lane(key, [(x, KEY_TOP), (x, KEY_BOTTOM)])
        sh.text(x, KEY_BOTTOM + 7, key, size=7.5, bold=True, align="center")
    r_cy = (S.RING_TOP + S.TAPE_W / 2 + KEY_TOP) / 2
    # R1's label is its ref and value with no "·" between them, so it's written here, where
    # the footprint puts a label: just right of the 2.4 mm body.
    lay.resistor("R1", KEY_X[-1], r_cy, vertical=True, lead=12, label=None)
    r1 = CIRCUIT["R1"]
    sh.text(KEY_X[-1] + 2.4 / 2 + 1, r_cy + 1, f"{r1.ref} {r1.text}", size=6, color=MUTED)
    for i in range(len(KEYS) - 1):
        right, left = KEY_X[-1 - i], KEY_X[-2 - i]
        lay.resistor(f"R{i + 2}", (left + right) / 2, LADDER_Y[i % 2], vertical=False, lead=10)


def _schematic(sh, lay):
    lesson.schematic_panel(sh)
    labels = WORDS.fields("Labels")
    top, ladder_y, key_y = 216.0, 244.0, 252.0
    xs = [40.0 + 7.5 * i for i in range(8)]
    sch.terminal(sh, 40, top, "V+", label_y=top - 3.4)
    sch.wire(sh, [(40.8, top), (xs[-1], top)])
    r1 = lay.symbol("R1")
    sch.resistor(sh, xs[-1], top, ladder_y, "", "")
    sh.text(xs[-1] - 2.6, (top + ladder_y) / 2 - 0.4, r1.ref, size=6.5, bold=True, align="right")
    sh.text(xs[-1] - 2.6, (top + ladder_y) / 2 + 2.8, r1.text, size=6, color=MUTED, align="right")
    for i in range(7):
        right, left = xs[-1 - i], xs[-2 - i]
        sch.resistor_h(sh, left, right, ladder_y, lay.symbol(f"R{i + 2}").ref, box_w=4.2)
    for i, (x, note) in enumerate(zip(xs, NOTES)):
        sch.junction(sh, x, ladder_y)
        sch.wire(sh, [(x, ladder_y), (x, key_y - 0.9)])
        sh.circle(x, key_y, 1.8, stroke=sch.INK, fill=sch.WHITE, width=sch.W)
        sh.text(x, key_y + 5, note, size=6.5, bold=True, align="center")
    sch.terminal(sh, 66, 270, "", 0)
    sh.line(66, 269.2, xs[2], key_y + 0.9, width=0.3, color=MUTED, dash=(1, 0.8))
    sh.text(68, 271.2, labels["pitch"], size=6.5, bold=True)
    sh.text(56, 266, labels["stylus"], size=6, color=MUTED, align="right")
    lesson.schematic_note(sh, WORDS.text("Schematic note"))
