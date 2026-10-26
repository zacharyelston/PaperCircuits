from pathlib import Path

import pytest

from papercircuits.standard_docs import documentation_problems, documented_values

ROOT = Path(__file__).parents[1]


def test_page_standard_values_match_code():
    assert documentation_problems(ROOT / "docs/page-standard.md") == []


def test_missing_table_is_actionable():
    with pytest.raises(ValueError, match="missing its machine-checked values table"):
        documented_values("# Page standard")


def test_mismatch_names_constant(tmp_path):
    original = (ROOT / "docs/page-standard.md").read_text()
    path = tmp_path / "page-standard.md"
    path.write_text(original.replace("| `TAPE_W` | 5 |", "| `TAPE_W` | 6 |"))
    assert documentation_problems(path) == ["TAPE_W: documentation says 6.0, code says 5.0"]
