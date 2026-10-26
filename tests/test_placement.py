from types import SimpleNamespace

import pytest

from papercircuits.circuit import LED, PENCIL, Circuit, R
from papercircuits.draw import Sheet
from papercircuits.placement import Placement


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def placement(circuit):
    return Placement(SimpleNamespace(title="test page"), circuit)


def test_valid_nonpolar_part_and_parts_list():
    lay = placement(Circuit(R("R1", 220, "A", "B")))
    lay.strips = {"A": [rect(0, 0, 2, 2)], "B": [rect(8, 0, 10, 2)]}
    lay.leads = [("R1", [((1, 1), (1, 1)), ((9, 1), (9, 1))])]
    lay.symbols = ["R1"]
    lay.check(listed={"R1"})


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda lay: lay.strips.pop("B"), "net B has 0 strips"),
        (lambda lay: lay.strips["A"].append(rect(20, 0, 22, 2)), "net A has 2 strips"),
        (lambda lay: lay.strips.update({"EXTRA": [rect(20, 0, 22, 2)]}), "lane on EXTRA"),
        (lambda lay: lay.leads.clear(), "R1 is placed 0 times"),
        (lambda lay: lay.symbols.clear(), "R1 is drawn 0 times"),
    ],
)
def test_structural_invariants(mutate, message):
    lay = placement(Circuit(R("R1", 220, "A", "B")))
    lay.strips = {"A": [rect(0, 0, 2, 2)], "B": [rect(8, 0, 10, 2)]}
    lay.leads = [("R1", [((1, 1), (1, 1)), ((9, 1), (9, 1))])]
    lay.symbols = ["R1"]
    mutate(lay)
    with pytest.raises(RuntimeError, match=message):
        lay.check(listed={"R1"})


def test_wrong_nonpolar_nets_and_missing_parts_list_entry():
    lay = placement(Circuit(R("R1", 220, "A", "B")))
    lay.strips = {"A": [rect(0, 0, 2, 2)], "B": [rect(8, 0, 10, 2)]}
    lay.leads = [("R1", [((1, 1), (1, 1)), ((1, 1), (1, 1))])]
    lay.symbols = ["R1"]
    with pytest.raises(RuntimeError, match=r"(?s)lands on.*isn't in the You need list"):
        lay.check(listed=set())


def test_polar_pin_must_land_on_its_declared_net():
    lay = placement(Circuit(LED("LED1", "A", "K")))
    lay.strips = {"A": [rect(0, 0, 2, 2)], "K": [rect(8, 0, 10, 2)]}
    lay.leads = [("LED1", {"anode": ((9, 1), (9, 1)), "cathode": ((1, 1), (1, 1))})]
    lay.symbols = ["LED1"]
    with pytest.raises(RuntimeError, match="LED1's anode lands on K"):
        lay.check(listed={"LED1"})


def test_patch_loop_and_test_point_must_touch_their_net_and_be_in_schematic():
    lay = placement(Circuit(R("R1", 220, "A", "B")))
    lay.strips = {"A": [rect(0, 0, 2, 2)], "B": [rect(8, 0, 10, 2)]}
    lay.leads = [("R1", [((1, 1), (1, 1)), ((9, 1), (9, 1))])]
    lay.loops = [("A", ((9, 1), (9, 1)))]
    lay.points = [("TP1", "B", (1, 1))]
    lay.symbols = ["R1"]
    with pytest.raises(RuntimeError, match=r"(?s)patch loop A.*TP1 sits on A.*TP1 is drawn 0 times"):
        lay.check(listed={"R1"})


def test_pencil_requires_wiper_and_clear_reachable_lane():
    circuit = Circuit(PENCIL("P1", "TRACK", "WIPER"))
    lay = placement(circuit)
    track = rect(0, 0, 10, 5)
    lay.strips = {"TRACK": [track], "WIPER": [rect(12, 0, 17, 5)]}
    lay.pencils = {"P1": (track, None)}
    lay.symbols = ["P1"]
    with pytest.raises(RuntimeError, match="has no wiper"):
        lay.check()

    lay.pencils["P1"] = (track, 9)
    with pytest.raises(RuntimeError, match="closer than 3 mm"):
        lay.check()

    lay.strips["WIPER"] = [rect(13, 0, 18, 5)]
    with pytest.raises(RuntimeError, match="can't reach"):
        lay.check()

    lay.pencils["P1"] = (track, 10)
    lay.check()


@pytest.mark.parametrize(("strip_len", "passes"), [(12.0, True), (11.5, False)])
def test_wiper_reach_boundary(strip_len, passes):
    circuit = Circuit(PENCIL("P1", "TRACK", "WIPER"))
    lay = placement(circuit)
    track = rect(0, 0, 10, 5)
    lay.strips = {"TRACK": [track], "WIPER": [rect(15, 0, 20, 5)]}
    lay.pencils = {"P1": (track, strip_len)}
    lay.symbols = ["P1"]
    if passes:
        lay.check()
    else:
        with pytest.raises(RuntimeError, match="can't reach"):
            lay.check()


def test_real_sheet_lane_and_resistor_footprint(tmp_path):
    circuit = Circuit(R("R1", 220, "TOP", "BOTTOM"))
    sheet = Sheet(tmp_path / "placement.pdf", "placement test")
    lay = Placement(sheet, circuit)
    lay.lane("TOP", [(40, 40), (60, 40)])
    lay.lane("BOTTOM", [(40, 60), (60, 60)])
    lay.resistor("R1", 50, 50, vertical=True, lead=10)
    lay.symbols = ["R1"]
    lay.check(listed={"R1"})
    sheet.save()
    assert (tmp_path / "placement.pdf").stat().st_size > 0
