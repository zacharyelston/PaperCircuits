import pytest

from papercircuits.drc import distance, violations


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (rect(0, 0, 1, 1), rect(4, 0, 5, 1), 3),
        (rect(0, 0, 1, 1), rect(1, 0, 2, 1), 0),
        (rect(0, 0, 3, 3), rect(1, 1, 2, 2), 0),
        (rect(0, 0, 2, 2), rect(1, -1, 3, 1), 0),
    ],
)
def test_polygon_distance(a, b, expected):
    assert distance(a, b) == pytest.approx(expected)
    assert distance(b, a) == pytest.approx(expected)


def test_clearance_boundary_and_tolerance():
    lanes = [rect(0, 0, 1, 1), rect(3.99, 0, 4.99, 1)]
    assert violations(lanes, {}) == []  # 2.99 mm is within the check's 0.01 mm tolerance.
    lanes[1] = rect(3.98, 0, 4.98, 1)
    assert violations(lanes, {}) == [(0, 1, pytest.approx(2.98), 3.0)]


def test_allowed_pair_uses_its_specific_limit():
    lanes = [rect(0, 0, 1, 1), rect(3, 0, 4, 1)]
    assert violations(lanes, {})
    assert violations(lanes, {(0, 1): 2.0}) == []
