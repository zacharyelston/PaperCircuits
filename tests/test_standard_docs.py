from pathlib import Path

from papercircuits.standard_docs import documentation_problems

ROOT = Path(__file__).parents[1]


def test_page_standard_values_match_code():
    assert documentation_problems(ROOT / "docs/page-standard.md") == []


def test_existing_prose_mismatch_is_named(tmp_path):
    original = (ROOT / "docs/page-standard.md").read_text()
    path = tmp_path / "page-standard.md"
    path.write_text(original.replace("standard tape is 5 mm", "standard tape is 6 mm"))
    assert "page standard is missing or has changed: standard tape width" in documentation_problems(path)


def test_existing_normative_table_mismatch_is_named(tmp_path):
    original = (ROOT / "docs/page-standard.md").read_text()
    path = tmp_path / "page-standard.md"
    path.write_text(original.replace("| H2 | (12, 108.5) | V+ |", "| H2 | (12, 109) | V+ |"))
    assert "page standard is missing or has changed: H2 row" in documentation_problems(path)


def test_derived_switch_landing_is_checked(tmp_path):
    original = (ROOT / "docs/page-standard.md").read_text()
    path = tmp_path / "page-standard.md"
    path.write_text(original.replace("centred on (184, 24)", "centred on (185, 24)"))
    assert "page standard is missing or has changed: switch landing" in documentation_problems(path)
