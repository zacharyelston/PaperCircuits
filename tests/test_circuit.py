import pytest

from papercircuits.circuit import WIRE, C, Circuit, R, si


@pytest.mark.parametrize(
    ("value", "unit", "expected"),
    [(22e3, "Ω", "22 kΩ"), (4.7e3, "Ω", "4.7 kΩ"), (2200e-6, "F", "2200 µF"), (47e-9, "F", "47 nF")],
)
def test_si(value, unit, expected):
    assert si(value, unit) == expected


def test_resistor_bands():
    assert R("R1", 220, "A", "B").bands == "red-red-brown"
    assert R("R1", 4.7e3, "A", "B").bands == "yellow-violet-red"


def test_bands_reject_unsupported_parts_and_sub_ten_ohm_values():
    with pytest.raises(ValueError, match="no three-band"):
        _ = C("C1", 1e-6, "A", "B").bands
    with pytest.raises(ValueError, match="no three-band"):
        _ = R("R1", 4.7, "A", "B").bands


def test_circuit_rejects_duplicate_refs():
    with pytest.raises(ValueError, match="two parts share a ref"):
        Circuit(R("R1", 220, "A", "B"), R("R1", 1000, "B", "C"))


def test_group_uses_kind_value_and_note_and_nets_keep_first_seen_order():
    circuit = Circuit(
        R("R1", 220, "V+", "N1", "red"),
        R("R2", 220, "N1", "GND", "red"),
        R("R3", 220, "V+", "GND", "blue"),
    )
    assert circuit.group("R1") == ["R1", "R2"]
    assert circuit.nets == ["V+", "N1", "GND"]


def test_unknown_ref_has_actionable_error():
    with pytest.raises(KeyError, match="no part R9"):
        _ = Circuit(R("R1", 220, "A", "B"))["R9"]


def test_rejects_same_net_terminals_and_allows_narrow_exception():
    with pytest.raises(ValueError, match="R1 has more than one terminal on A"):
        Circuit(R("R1", 220, "A", "A"))
    Circuit(R("R1", 220, "A", "A"), allow={"same-net:R1"})


def test_rejects_direct_bare_wire_rail_short():
    with pytest.raises(ValueError, match=r"W1 directly shorts V\+ to GND"):
        Circuit(WIRE("W1", "V+", "GND"))


def test_rejects_disconnected_part_groups_and_can_declare_intent():
    parts = (R("R1", 220, "A", "B"), R("R2", 1000, "C", "D"))
    with pytest.raises(ValueError, match=r"disconnected part groups: R1 / R2"):
        Circuit(*parts)
    Circuit(*parts, allow={"disconnected"})


def test_unknown_exception_is_rejected():
    with pytest.raises(ValueError, match="unknown electrical-check exception: typo:R1"):
        Circuit(R("R1", 220, "A", "B"), allow={"typo:R1"})
