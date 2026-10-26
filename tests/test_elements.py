from types import SimpleNamespace

import pytest

from papercircuits import elements as E


class RecordingSheet:
    def __init__(self):
        self.texts = []

    def circle(self, *_args, **_kwargs):
        pass

    def line(self, *_args, **_kwargs):
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


def test_mechanical_spine_rejects_electrical_hole_connections():
    with pytest.raises(ValueError, match="mechanical spine cannot connect"):
        E.spine(SimpleNamespace(), connected=("H2",), mechanical=True)
