from pathlib import Path

import pytest

from papercircuits.circuit import Circuit, R
from papercircuits.words import Words, _parse, number


def write_words(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "sheet.md"
    path.write_text(text)
    return path


def test_parse_joins_wrapped_lines_and_separates_items():
    title, subtitle, sections = _parse("# Title\nfirst\nsecond\n\n## Steps\n1. one\nwrap\n2. two\n")
    assert title == "Title"
    assert subtitle == ["first second"]
    assert sections == {"Steps": ["one wrap", "two"]}


def test_duplicate_section_is_rejected():
    with pytest.raises(ValueError, match="has '## A' twice"):
        _parse("## A\none\n## A\ntwo", "bad.md")


def test_fill_uses_circuit_values_groups_standard_tags_and_call_values(tmp_path):
    circuit = Circuit(R("R1", 220, "A", "B"), R("R2", 220, "B", "C"))
    words = Words(
        write_words(
            tmp_path,
            "# Page {version}\nSubtitle {T0}\n## You need\n- {R1.count} resistors: {R1.refs}, {R1} ({R1.bands})\n"
            "## Build it\n1. Lay {lanes} lanes.\n",
        ),
        circuit,
    )
    assert words.title == "Page 0.1"
    assert "[T0]" in words.subtitle
    assert words.items("You need") == ["2 resistors: R1, R2, 220 Ω (red-red-brown)"]
    assert words.items("Build it", lanes="three") == ["Lay three lanes."]
    assert words.refs("You need") == {"R1", "R2"}


def test_missing_fill_and_field_have_context(tmp_path):
    words = Words(write_words(tmp_path, "# Page\nSubtitle\n## Text\n{missing}\n## Fields\n- present: yes\n"))
    with pytest.raises(KeyError, match=r"sheet.md, ## Text: nothing to fill \{missing\} with"):
        words.text("Text")
    with pytest.raises(KeyError, match="has no field 'absent'"):
        _ = words.fields("Fields")["absent"]


def test_number_names_small_counts_and_falls_back_to_digits():
    assert number(0) == "no"
    assert number(12) == "twelve"
    assert number(13) == "13"
