"""Check the authoritative dimensions table in the page standard against code."""

from pathlib import Path

from .standard import DOCUMENTED_VALUES

START = "<!-- standard-values:start -->"
END = "<!-- standard-values:end -->"


def documented_values(text):
    try:
        table = text.split(START, 1)[1].split(END, 1)[0]
    except IndexError as error:
        raise ValueError("page standard is missing its machine-checked values table") from error
    values = {}
    for line in table.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 2:
            raise ValueError(f"malformed standard value row: {line}")
        key = cells[0].strip("`")
        raw = cells[1]
        values[key] = raw if key == "VERSION" else float(raw)
    return values


def documentation_problems(path):
    actual = documented_values(Path(path).read_text())
    problems = []
    for key in sorted(DOCUMENTED_VALUES.keys() - actual.keys()):
        problems.append(f"{key} is missing from the documented values table")
    for key in sorted(actual.keys() - DOCUMENTED_VALUES.keys()):
        problems.append(f"{key} is documented but absent from DOCUMENTED_VALUES")
    for key in sorted(DOCUMENTED_VALUES.keys() & actual.keys()):
        if actual[key] != DOCUMENTED_VALUES[key]:
            problems.append(f"{key}: documentation says {actual[key]!r}, code says {DOCUMENTED_VALUES[key]!r}")
    return problems
