"""The circuit layer: what a page is, electrically.

A page lists its parts once, with real values and the nets their pins join. Everything
else reads from that list: the "You need" lines, the labels on footprints and schematic
symbols, any calculation a page or its notes quote, and the placement check, which makes
sure the copper joins what the circuit says it joins.
"""

from dataclasses import dataclass, field

COLOUR_CODE = ("black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "grey", "white")
_PREFIXES = ((1e6, "M"), (1e3, "k"), (1.0, ""), (1e-3, "m"), (1e-6, "µ"), (1e-9, "n"), (1e-12, "p"))


def si(value, unit):
    """A value as the pages print it: 22e3 → "22 kΩ", 4.7e3 → "4.7 kΩ", 1e-6 → "1 µF"."""
    for scale, prefix in _PREFIXES:
        if abs(value) >= scale * 0.999:
            return f"{round(value / scale, 3):g} {prefix}{unit}"
    return f"{value:g} {unit}"


@dataclass
class Part:
    ref: str
    kind: str
    value: float | None
    unit: str
    pins: dict = field(default_factory=dict)  # pin name -> net
    note: str = ""
    polar: bool = False  # True: each named pin must land on its own net

    @property
    def text(self):
        """The value as printed, or the note for a part with no value, such as an LED."""
        return si(self.value, self.unit) if self.value is not None else self.note

    @property
    def bands(self):
        """A resistor's three colour bands: 220 Ω → "red-red-brown"."""
        mantissa, exponent = f"{self.value:.1e}".split("e")
        digits = mantissa.replace(".", "")
        if self.kind != "resistor" or int(exponent) < 1:
            raise ValueError(f"{self.ref}: no three-band colour code for {self.text}")
        return "-".join(COLOUR_CODE[int(d)] for d in (*digits, int(exponent) - 1))

    @property
    def nets(self):
        return tuple(self.pins.values())


def R(ref, ohms, a, b, note=""):
    """A resistor between nets a and b, either way round."""
    return Part(ref, "resistor", ohms, "Ω", {"1": a, "2": b}, note)


def C(ref, farads, a, b, note=""):
    """A capacitor with no polarity between nets a and b."""
    return Part(ref, "capacitor", farads, "F", {"1": a, "2": b}, note)


def LED(ref, anode, cathode, note=""):
    """An LED: current flows from the anode's net to the cathode's."""
    return Part(ref, "led", None, "", {"anode": anode, "cathode": cathode}, note, polar=True)


def SW(ref, a, b, note=""):
    """A switch joining nets a and b while it's closed."""
    return Part(ref, "switch", None, "", {"1": a, "2": b}, note)


class Circuit:
    def __init__(self, *parts):
        self.parts = {p.ref: p for p in parts}
        if len(self.parts) != len(parts):
            raise ValueError("two parts share a ref")

    def __getitem__(self, ref):
        return self.parts[ref]

    @property
    def nets(self):
        seen = {}
        for part in self.parts.values():
            for net in part.nets:
                seen.setdefault(net, None)
        return list(seen)

    def need(self):
        """The parts as "You need" lines: resistors grouped by value on one line, then each
        group of capacitors with the same value and note."""
        lines = []
        resistors = _groups(p for p in self.parts.values() if p.kind == "resistor")
        if resistors:
            lines.append(" · ".join(f"{', '.join(refs)} {text}" for (text, _), refs in resistors))
        for (text, note), refs in _groups(p for p in self.parts.values() if p.kind == "capacitor"):
            lines.append(f"{', '.join(refs)}: {text}, {note}" if note else f"{', '.join(refs)}: {text}")
        return lines


def _groups(parts):
    """Parts with the same printed value and note, in the order they first appear."""
    groups = {}
    for p in parts:
        groups.setdefault((p.text, p.note), []).append(p.ref)
    return list(groups.items())
