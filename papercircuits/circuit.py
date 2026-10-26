"""The circuit layer: what a page is, electrically.

A page lists its parts once, with real values and the nets their pins join. Everything
else reads from that list: the values and counts in the "You need" lines, the labels on
footprints and schematic symbols, any calculation a page or its notes quote, and the
placement check, which makes sure the copper joins what the circuit says it joins.

Polarised parts name their pins (anode and cathode; plus and minus; E, B and C), and the
check holds each named pin to its own net. A pencil part is a 6B track: its "track" net
is the pencil itself, and its wiper joins it to the "wiper" net's lane.
"""

import heapq
from dataclasses import dataclass, field

COLOUR_CODE = ("black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "grey", "white")
_PREFIXES = ((1e6, "M"), (1e3, "k"), (1.0, ""), (1e-3, "m"), (1e-6, "µ"), (1e-9, "n"), (1e-12, "p"))
_FARAD_PREFIXES = ((1e-6, "µ"), (1e-9, "n"), (1e-12, "p"))  # capacitors are marked 2200 µF, never 2.2 mF


def si(value, unit):
    """A value as the pages print it: 22e3 → "22 kΩ", 4.7e3 → "4.7 kΩ", 2200e-6 → "2200 µF"."""
    for scale, prefix in _FARAD_PREFIXES if unit == "F" else _PREFIXES:
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
    """A switch joining nets a and b while it's closed: a corner flap or a tab."""
    return Part(ref, "switch", None, "", {"1": a, "2": b}, note)


def D(ref, anode, cathode, note=""):
    """A diode: current flows from the anode's net to the cathode's."""
    return Part(ref, "diode", None, "", {"anode": anode, "cathode": cathode}, note, polar=True)


def CE(ref, farads, plus, minus, note=""):
    """An electrolytic capacitor: its + leg on `plus`, its − leg on `minus`."""
    return Part(ref, "electrolytic", farads, "F", {"plus": plus, "minus": minus}, note, polar=True)


def Q(ref, model, e, b, c):
    """An NPN transistor such as a 2N3904, by its emitter, base and collector nets."""
    return Part(ref, "transistor", None, "", {"E": e, "B": b, "C": c}, model, polar=True)


def LDR(ref, a, b, note=""):
    """A light-dependent resistor between nets a and b, either way round."""
    return Part(ref, "ldr", None, "", {"1": a, "2": b}, note)


def F(ref, a, b, note=""):
    """A resettable fuse between nets a and b, either way round."""
    return Part(ref, "fuse", None, "", {"1": a, "2": b}, note)


def BAT(ref, plus, minus, note=""):
    """A battery holder whose red wire goes to `plus` and black to `minus`."""
    return Part(ref, "battery", None, "", {"plus": plus, "minus": minus}, note, polar=True)


def PENCIL(ref, track, wiper, note=""):
    """A pencil track: the `track` net is the pencil, and a wiper joins it to `wiper`'s lane."""
    return Part(ref, "pencil", None, "", {"track": track, "wiper": wiper}, note, polar=True)


def WIRE(ref, a, b, note=""):
    """A bare wire link between nets a and b."""
    return Part(ref, "wire", None, "", {"1": a, "2": b}, note)


# Parts a learner buys or picks out, so every one must appear in "You need". Switches,
# pencil and bare wire are made from the page, the pencil and offcuts.
BOUGHT = ("resistor", "capacitor", "electrolytic", "led", "diode", "transistor", "ldr", "fuse", "battery")


class Circuit:
    def __init__(self, *parts, allow=(), controller=False, controller_outputs=()):
        self.parts = {p.ref: p for p in parts}
        self.allow = frozenset(allow)
        self.controller = controller
        self.controller_outputs = tuple(controller_outputs) or ("PITCH",)
        if len(self.parts) != len(parts):
            raise ValueError("two parts share a ref")
        problems = self.problems()
        if problems:
            raise ValueError("invalid circuit:\n  " + "\n  ".join(problems))

    def __getitem__(self, ref):
        if ref not in self.parts:
            raise KeyError(f"no part {ref} in the circuit (it has {', '.join(self.parts)})")
        return self.parts[ref]

    @property
    def nets(self):
        seen = {}
        for part in self.parts.values():
            for net in part.nets:
                seen.setdefault(net, None)
        return list(seen)

    def group(self, ref):
        """The refs of every part that's interchangeable with `ref`: same kind, value and
        note. "You need" counts and lists parts by group, so a part whose value changes
        drops out of its old line."""
        p = self.parts[ref]
        return [q.ref for q in self.parts.values() if (q.kind, q.value, q.note) == (p.kind, p.value, p.note)]

    def problems(self):
        """Conservative graph checks only; this is deliberately not analogue simulation.

        An intentional exception is named narrowly in ``allow``, for example
        ``Circuit(..., allow={"same-net:R1"})``.
        """
        problems = []
        for part in self.parts.values():
            if len(set(part.nets)) != len(part.nets) and f"same-net:{part.ref}" not in self.allow:
                problems.append(f"{part.ref} has more than one terminal on {part.nets[0]}")
            if part.kind == "wire" and set(part.nets) == {"V+", "GND"} and f"rail-short:{part.ref}" not in self.allow:
                problems.append(f"{part.ref} directly shorts V+ to GND")
        if self.parts and "disconnected" not in self.allow:
            groups = self._connected_part_groups()
            if len(groups) > 1:
                descriptions = [", ".join(group) for group in groups]
                problems.append("disconnected part groups: " + " / ".join(descriptions))
        if self.controller:
            paths = [self.shortest_fixed_resistance("V+", output) for output in self.controller_outputs]
            reachable = [resistance for resistance in paths if resistance is not None]
            if len(reachable) != len(paths):
                problems.append("controller has no path from V+ to PITCH")
            elif (resistance := min(reachable)) < 10e3:
                problems.append(f"controller's shortest V+ to PITCH path is {si(resistance, 'Ω')}, below 10 kΩ")
        unknown = sorted(
            exception
            for exception in self.allow
            if exception != "disconnected"
            and not any(exception == f"{rule}:{ref}" for rule in ("same-net", "rail-short") for ref in self.parts)
        )
        problems += [f"unknown electrical-check exception: {exception}" for exception in unknown]
        return problems

    def shortest_fixed_resistance(self, start, end):
        """Shortest path using fixed resistor values; variable and non-resistive parts cost 0 Ω."""
        graph = {}
        for part in self.parts.values():
            if len(part.nets) != 2 or part.kind not in {"resistor", "pencil", "ldr"}:
                continue
            a, b = part.nets
            weight = part.value if part.kind == "resistor" else 0.0
            graph.setdefault(a, []).append((b, weight))
            graph.setdefault(b, []).append((a, weight))
        queue = [(0.0, start)]
        best = {start: 0.0}
        while queue:
            distance, net = heapq.heappop(queue)
            if net == end:
                return distance
            if distance != best[net]:
                continue
            for neighbour, weight in graph.get(net, []):
                candidate = distance + weight
                if candidate < best.get(neighbour, float("inf")):
                    best[neighbour] = candidate
                    heapq.heappush(queue, (candidate, neighbour))
        return None

    def _connected_part_groups(self):
        remaining = set(self.parts)
        groups = []
        while remaining:
            group = {remaining.pop()}
            nets = set(self.parts[next(iter(group))].nets)
            changed = True
            while changed:
                changed = False
                for ref in list(remaining):
                    if nets.intersection(self.parts[ref].nets):
                        remaining.remove(ref)
                        group.add(ref)
                        nets.update(self.parts[ref].nets)
                        changed = True
            groups.append(sorted(group))
        return sorted(groups)
