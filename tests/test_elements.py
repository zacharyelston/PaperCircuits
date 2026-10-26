from types import SimpleNamespace

import pytest

from papercircuits import elements as E
from papercircuits import standard as S


class RecordingSheet:
    def __init__(self):
        self.texts = []
        self.lines = []
        self.polygons = []
        self.circles = []

    def circle(self, *args, **kwargs):
        self.circles.append((args, kwargs))

    def line(self, *args, **kwargs):
        self.lines.append((args, kwargs))

    def polygon(self, *args, **kwargs):
        self.polygons.append((args, kwargs))

    def rect(self, *_args, **_kwargs):
        pass

    def text(self, _x, _y, value, **_kwargs):
        self.texts.append(value)


def test_mechanical_spine_labels_holes_as_having_no_net():
    sheet = RecordingSheet()
    E.spine(sheet, mechanical=True)
    assert sheet.texts == [f"H{i} · no net" for i in range(1, 5)]


def test_spine_can_hide_labels_on_dense_results_pages():
    sheet = RecordingSheet()
    E.spine(sheet, mechanical=True, show_labels=False)
    assert sheet.texts == []


def test_v2_three_hole_spine_uses_three_mechanical_holes():
    sheet = RecordingSheet()
    E.spine(sheet, mechanical=True, holes=S.V2_HOLES)
    assert sheet.texts == [f"H{i} · no net" for i in range(1, 4)]


def test_mechanical_spine_rejects_electrical_hole_connections():
    with pytest.raises(ValueError, match="mechanical spine cannot connect"):
        E.spine(SimpleNamespace(), connected=("H2",), mechanical=True)


def test_wrap_arrow_draws_one_solid_directional_marker():
    sheet = RecordingSheet()
    E.wrap_arrow(sheet, 20, 4, "up")
    assert len(sheet.polygons) == 1
    points = sheet.polygons[0][0][0]
    assert points[0][1] < points[1][1]


def test_wrap_arrow_rejects_unknown_direction():
    with pytest.raises(ValueError, match="unknown wrap direction"):
        E.wrap_arrow(RecordingSheet(), 20, 4, "diagonal")


def test_wire_via_uses_chevrons_and_no_target_circle():
    sheet = RecordingSheet()
    E.via(sheet, 20, 40, "wire")
    assert len(sheet.lines) == 6
    assert sheet.circles == []
