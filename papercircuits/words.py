"""The words layer: a page's text lives in a Markdown file beside its sheet module.

    # M7  Output                      the page title
    Mix up to three signals...       the subtitle: the paragraph under the title
    ## Build it                       a section
    1. Lay the power ring...          numbered or "-" items, or plain paragraphs

Lines that wrap without a blank line join into one item. A section of "- key: text"
items can be read as fields, for text the page places itself, such as a workbook box's
prompts. In any text:

- {name} is filled in when the page is built: a value the page passes in (such as
  {lanes}, counted from the copper), a part's value from the circuit ({R1}, or
  {R1.bands} for its colour code), a shared snippet from sheets/shared.md (such as
  {lead_step}), or a provisional tag: {T0}, {T1} or {P}
- **bold** prints bold
"""

import re
from functools import cache
from pathlib import Path

from .provisional import POWER, T0, T1

TAGS = {"T0": T0, "T1": T1, "P": POWER}
SHARED = Path(__file__).parent / "sheets" / "shared.md"
NUMBERS = ("no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve")

_ITEM = re.compile(r"^(?:\d+\.|-)\s+")
_FIELD = re.compile(r"\{([\w.]+)\}")
_BOLD = re.compile(r"\*\*(.+?)\*\*")


def number(n):
    """A count as the steps print it: 5 → "five"."""
    return NUMBERS[n] if n < len(NUMBERS) else str(n)


class Words:
    def __init__(self, path, circuit=None):
        self.path, self.circuit = Path(path), circuit
        self.title, subtitle, self._sections = _parse(self.path.read_text())
        self.subtitle = " ".join(subtitle)

    @classmethod
    def beside(cls, module_file, circuit=None):
        """The words for the sheet module at `module_file`: same name, .md."""
        return cls(Path(module_file).with_suffix(".md"), circuit)

    def items(self, name, **values):
        """A section's items or paragraphs, filled in."""
        if name not in self._sections:
            raise KeyError(f"{self.path.name} has no section '## {name}'")
        try:
            return [_fill(block, values, self.circuit) for block in self._sections[name]]
        except KeyError as e:
            raise KeyError(f"{self.path.name}, ## {name}: nothing to fill {{{e.args[0]}}} with") from None

    def text(self, name, **values):
        """A section that is one paragraph."""
        (only,) = self.items(name, **values)
        return only

    def fields(self, name, **values):
        """A section of "key: text" items, as a dict."""
        return dict(item.split(": ", 1) for item in self.items(name, **values))


def _parse(text):
    title, subtitle, sections = "", [], {}
    target, block = subtitle, None
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:]
        elif line.startswith("## "):
            target = sections.setdefault(line[3:].strip(), [])
            block = None
        elif not line.strip():
            block = None
        elif (m := _ITEM.match(line)) or block is None:
            block = [line[m.end():] if m else line.strip()]
            target.append(block)
        else:
            block.append(line.strip())
    joined = {name: [" ".join(b) for b in blocks] for name, blocks in sections.items()}
    return title, [" ".join(b) for b in subtitle], joined


@cache
def _shared():
    _, _, sections = _parse(SHARED.read_text())
    return {name: blocks[0] for name, blocks in sections.items()}


def _fill(text, values, circuit=None):
    def field(m):
        key = m.group(1)
        ref, _, attr = key.partition(".")
        if key in values:
            return str(values[key])
        if circuit is not None and ref in circuit.parts:
            return str(getattr(circuit[ref], attr or "text"))
        if key in _shared():
            return _fill(_shared()[key], values, circuit)
        if key in TAGS:
            return TAGS[key]
        raise KeyError(key)
    return _BOLD.sub(r"<b>\1</b>", _FIELD.sub(field, text))
