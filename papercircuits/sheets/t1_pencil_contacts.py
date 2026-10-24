"""T1 pencil contacts.

Can pencil make copper tape's glue conduct? Two tests, each with a control:
1. Tape overlaps: the upper piece's glue is scratched, rubbed with pencil, or both,
   against a plain overlap (the T0 J2 control) and a continuous reference lane.
2. Tape on pencil: copper joined to a shaded track by plain tape, treated glue, a folded
   copper tab, or L03's bare wire under clear tape.

Sheet 1 holds the fixtures and results: print on card, once per paper being compared.
Sheet 2 is the procedure: print once on plain paper.
"""

from reportlab.platypus import Paragraph

from .. import elements as E
from .. import standard as S
from .. import testsheet as ts
from ..draw import GUIDE, MUTED, Sheet, style

PAGE_ID = "T1"
LEFT, RIGHT = S.ZONE_BUILD[0], S.ZONE_BUILD[2]

OVERLAPS = [
    ("O0", "Continuous", "the reference", False),
    ("O1", "Plain overlap", "control: glue untouched", True),
    ("O2", "Scratched", "fingernail through the glue", True),
    ("O3", "Pencil rubbed", "6B rubbed into the glue", True),
    ("O4", "Scratched + pencil", "scratch, then rub 6B in", True),
    ("O5", "Scratched + HB", "harder tip, less graphite", True),
    ("O6", "Your version", "", True),
]
OVERLAP_A, OVERLAP_B, OVERLAP_J = 80.0, 152.0, 116.0

JOINS = [
    ("K1", "Plain tape on pencil", "control: glue on the pencil"),
    ("K2", "Scratched + pencil", "treat the glue, as O4"),
    ("K3", "Folded tab", "copper faces down, clear tape"),
    ("K4", "Bare wire", "wire onto pencil, clear tape"),
    ("K5", "Your version", ""),
]
TRACK = (96.0, 136.0)            # 40 mm of pencil between the two joins
TRACK_W = 10.0
JOIN_OVERLAP = 10.0
LANE_A, LANE_B = (74.0, TRACK[0] + JOIN_OVERLAP), (TRACK[1] - JOIN_OVERLAP, 158.0)
WIRE_LANE_A, WIRE_LANE_B = (74.0, 92.0), (140.0, 158.0)
PROBE_X = (LANE_A[1] + 2, LANE_B[0] - 2)

PAPERS = [
    "Smooth card, 160–200 gsm: the standard's choice",
    "Heavier card, 250–300 gsm, if your printer takes it",
    "Cartridge or drawing paper, 120–160 gsm: more tooth for pencil",
    "Coated (silk or gloss) card: tape grips well, pencil may not",
    "Plain 80 gsm paper, as a baseline",
]


def build(path):
    sh = Sheet(path, "T1 pencil contacts")
    _fixtures(sh)
    sh.next_page()
    _procedure(sh)
    sh.save()


def _fixtures(sh):
    E.header(sh, PAGE_ID, "T1  Pencil contacts",
             "Can pencil make copper tape's glue conduct? Build on 160–200 gsm card.", part="1/2")
    E.spine(sh)
    _overlaps(sh)
    _joins(sh)
    sh.rect(LEFT, 226, RIGHT, 281, stroke=GUIDE, width=0.25, radius=1.2)
    sh.text(LEFT + 2, 230, "Notes", size=6.5, bold=True, color=MUTED)
    E.footer(sh, f"{PAGE_ID} sheet 1 of 2")


def _row_label(sh, y, code, name, hint):
    sh.text(LEFT, y - 0.4, f"{code}  {name}", size=7, bold=True)
    if hint:
        sh.text(LEFT, y + 3.2, hint, size=6.5, color=MUTED)


def _overlaps(sh):
    sh.text(LEFT, 30, "1  Tape overlaps", size=10, bold=True)
    sh.paragraph(LEFT, 32, 136,
                 "Each lane is two pieces of tape overlapping by 10 mm at J. Before you lay the right-hand "
                 "piece, treat the glue on its first 10 mm as labelled. Measure A to B in ohms.",
                 style(7, color=MUTED))
    sh.runs(LEFT, 43.5, [("Meter zero ", True), ("_______ Ω", False), ("      Built on ", True),
                         ("______________", False)], size=7)
    sh.runs(LEFT, 48.5, [("Paper ", True), ("_________________________", False)], size=7)
    ts.result_headers(sh, 48.5)
    for i, (code, name, hint, joined) in enumerate(OVERLAPS):
        y = 55.0 + 11 * i
        E.lane(sh, [(OVERLAP_A - 2, y), (OVERLAP_B + 2, y)])
        if joined:
            E.joint(sh, OVERLAP_J, y)
        for x, end in ((OVERLAP_A, "A"), (OVERLAP_B, "B")):
            E.test_point(sh, x, y)
            sh.text(x, y - 4.6, end, size=6, color=MUTED, align="center")
        _row_label(sh, y, code, name, hint)
        ts.result_boxes(sh, y)


def _joins(sh):
    sh.text(LEFT, 133, "2  Tape on pencil", size=10, bold=True)
    sh.paragraph(LEFT, 135, 136,
                 "Shade each track with 6B, then join copper to both ends as labelled. Measure A to B, "
                 "then the bare pencil between the two small circles. Readings are in kΩ.",
                 style(7, color=MUTED))
    ts.result_headers(sh, 146.5, ("A to B", "Pencil", "Day 7"))
    for i, (code, name, hint) in enumerate(JOINS):
        y = 154.0 + 15 * i
        E.pencil_track(sh, TRACK[0], y - TRACK_W / 2, TRACK[1], y + TRACK_W / 2, tick=None)
        if code == "K4":
            lanes = (WIRE_LANE_A, WIRE_LANE_B)
            for x0, x1 in ((WIRE_LANE_A[1] - 4, TRACK[0] + 8), (TRACK[1] - 8, WIRE_LANE_B[0] + 4)):
                sh.line(x0, y, x1, y, width=0.6, color=MUTED, cap=1)
        else:
            lanes = (LANE_A, LANE_B)
        for x0, x1 in lanes:
            E.lane(sh, [(x0, y), (x1, y)])
        for x in PROBE_X:
            sh.circle(x, y, 3.0, stroke=MUTED, width=0.3)
        for x, end in ((LANE_A[0] + 4, "A"), (LANE_B[1] - 4, "B")):
            E.test_point(sh, x, y)
            sh.text(x, y - 4.6, end, size=6, color=MUTED, align="center")
        _row_label(sh, y, code, name, hint)
        ts.result_boxes(sh, y)


def _procedure(sh):
    E.header(sh, PAGE_ID, "T1  Running the pencil tests",
             "Print this sheet once on plain paper. Print sheet 1 on card, once per paper you compare.",
             part="2/2")
    E.spine(sh)
    left = [Paragraph("You need", ts.H)] + ts.bullets([
        "5 mm copper tape and clear tape",
        "A 6B and an HB pencil, sharpened, and an eraser",
        "A few centimetres of bare wire, or cut-off resistor legs, for K4",
        "A multimeter with 200 Ω and 200 kΩ ranges",
        "Your T0 results: O1 should behave like T0's J2",
    ])
    left += [Paragraph("Before you start", ts.H)] + ts.steps([
        "Print sheet 1 at 100 % on card. Write the paper on it: brand, weight and finish.",
        "Zero the meter on its 200 Ω range and write the reading on sheet 1.",
        "Keep fingers off the glue except where a step says to treat it: skin oil changes results.",
    ])
    left += [Paragraph("1 · Tape overlaps", ts.H)] + ts.steps([
        "Lay the left-hand piece of each lane from A to just past J.",
        "Cut the right-hand piece and peel its backing. Treat the glue on its first 10 mm: "
        "<b>scratched</b> means a criss-cross scored with a fingernail; <b>pencil</b> means rubbing the "
        "tip back and forth until the glue looks grey.",
        "Lay it over the left-hand piece by 10 mm, from J to B, and burnish the overlap hard with a fingernail.",
        "Brush loose graphite off the paper. A smudge beside a lane is a leak.",
        "Measure A to B on the 200 Ω range. <b>Flexed</b> and <b>Day 7</b> work as on T0.",
    ])

    right = [Paragraph("2 · Tape on pencil", ts.H)] + ts.steps([
        "Shade each track with the 6B: at least 10 passes, until it shines.",
        "Join copper to both ends of each track. <b>K1:</b> lay the tape straight on. <b>K2:</b> scratch and "
        "rub 6B into the glue's end first. <b>K3:</b> fold the tape's last 10 mm back on itself, sticky to "
        "sticky, so copper faces down; hold it on the pencil with clear tape. <b>K4:</b> stop the tape short, "
        "and bridge to the pencil with bare wire under clear tape. <b>K5:</b> your idea.",
        "Switch to the 200 kΩ range. Measure A to B, then the bare pencil between the two small circles.",
        "<b>Day 7:</b> measure A to B again.",
    ])
    right += [Paragraph("Pass or fail", ts.H)] + ts.bullets([
        "<b>Overlaps:</b> pass if within 1 Ω of O0 and steady. If O3 to O5 pass where O1 fails, "
        "pencil-treated overlaps could replace solder.",
        "<b>On pencil:</b> a good join makes A to B only a little more than the pencil-only reading. "
        "Several times more, OL, or a wandering reading means a poor contact.",
    ])
    left += [Paragraph("Trying different papers", ts.H),
              Paragraph("Paper changes how pencil takes, how well tape grips and how flaps spring back. "
                        "Build sheet 1 on each paper you're considering and compare:", style(7.5, leading=9.6))]
    left += ts.bullets(PAPERS)
    left += [Paragraph("The pencil-only reading compares how each paper takes graphite: lower is better. "
                        "Overlays are a separate question: try printing on vellum or tracing paper too, "
                        "as inkjet may smudge.", ts.NOTE)]
    right += [Paragraph("Results for standard v0.2", ts.H),
              ts.decision_table(["Pencil overlaps OK?", "Best overlap treatment", "Best join to pencil",
                                 "Best paper"], widths=(38, 42))]

    rest = sh.flow([(LEFT, 27.0, 115.0, 282.0)], left) + sh.flow([(121.0, 27.0, RIGHT, 282.0)], right)
    if rest:
        raise RuntimeError(f"T1 sheet 2 overflowed by {len(rest)} items")
    E.footer(sh, f"{PAGE_ID} sheet 2 of 2")
