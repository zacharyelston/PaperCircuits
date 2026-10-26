"""Check the authoritative dimensions table in the page standard against code."""

from pathlib import Path

from . import standard as S


def documentation_problems(path):
    text = Path(path).read_text()
    return [
        f"page standard is missing or has changed: {description}"
        for description, snippet in prose_facts()
        if snippet not in text
    ]


def prose_facts():
    """Existing normative prose/table rows tied directly to their code constants."""
    facts = [
        ("sheet size", f"| Size | A4 portrait, {S.PAGE_W:g} × {S.PAGE_H:g} mm |"),
        ("printable area", f"x {S.PRINT_SAFE[0]:g}–{S.PRINT_SAFE[2]:g}, y {S.PRINT_SAFE[1]:g}–{S.PRINT_SAFE[3]:g}"),
        ("hole size", f"**Hole size:** Ø{S.HOLE_D:g} mm"),
        ("hole keep-out", f"at least {S.HOLE_KEEP_OUT:g} mm from a hole centre"),
        ("standard tape width", f"standard tape is {S.TAPE_W:g} mm"),
        ("wide tape width", f"Use {S.WIDE_TAPE_W:g} mm only"),
        ("net clearance", f"**Clearance:** at least {S.NET_CLEARANCE:g} mm"),
        ("part gap", f"bridge a {S.PART_GAP:g} mm gap"),
        ("test point diameter", f"**Test points** are Ø{S.TEST_POINT_D:g} mm circles"),
        ("scale bar", f"{S.SCALE_BAR:g} mm scale bar"),
        ("patch loop", f"patch loop is a {S.PATCH_LOOP:g} mm piece"),
        (
            "switch fold",
            "from "
            f"({S.SWITCH_FOLD[0][0]:g}, {S.SWITCH_FOLD[0][1]:g}) to "
            f"({S.SWITCH_FOLD[1][0]:g}, {S.SWITCH_FOLD[1][1]:g})",
        ),
        ("switch pad", f"centred at ({S.SWITCH_FLAP_PAD[0]:g}, {S.SWITCH_FLAP_PAD[1]:g})"),
        ("switch landing", f"centred on ({S.SWITCH_CENTER[0]:g}, {S.SWITCH_CENTER[1]:g})"),
        ("switch pair pitch", f"({S.PAIR_PITCH:g} mm centre to centre)"),
        ("edge connector", f"V+ at y = {S.EDGE_V_Y:g} and GND at y = {S.EDGE_GND_Y:g}"),
        ("ring top", f"top of the build zone (y = {S.RING_TOP:g})"),
        ("ring bottom", f"along the bottom (y = {S.RING_BOTTOM:g})"),
    ]
    for hole, (y, net) in S.HOLES.items():
        facts.append((f"{hole} row", f"| {hole} | ({S.HOLE_X:g}, {y:g}) | {net} |"))
    zones = {
        "Header": S.ZONE_HEADER,
        "Switch corner": S.ZONE_SWITCH,
        "Build": S.ZONE_BUILD,
        "Schematic": S.ZONE_SCHEMATIC,
        "Workbook": S.ZONE_WORKBOOK,
        "Footer": S.ZONE_FOOTER,
    }
    for name, (x0, y0, x1, y1) in zones.items():
        facts.append((f"{name} zone", f"| {name} | {x0:g}–{x1:g} | {y0:g}–{y1:g} |"))
    return facts
