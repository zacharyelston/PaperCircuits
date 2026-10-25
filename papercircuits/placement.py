"""The placement layer: where a page's copper and parts go, bound to its circuit.

Every lane belongs to a net, and every part is placed by its ref, so check() can compare
the page with the circuit:

- each net in the circuit has exactly one strip of copper (standard §4: one strip per node)
- each lead lands on copper of its own net, and touches no other net; a polarised
  part's leads must each land on their own pin's net
- each patch loop and test point stands on its own net's lane
- each part's schematic symbol, and each test point's, is drawn exactly once

The clearance check still runs as before; this one covers what clearance can't: that the
copper joins what the circuit says it joins.
"""

from . import elements as E
from . import module
from .drc import distance

RING_NETS = ("V+", "GND")


class Placement:
    def __init__(self, sh, circuit):
        self.sh, self.circuit = sh, circuit
        self.lanes = {}    # net -> [lane ids]
        self.laid = 0      # lanes laid with lane(), so not counting an M page's ring
        self.leads = []    # (ref, [lead segments]) or (ref, {pin: lead segment})
        self.loops = []    # (net, feet segment)
        self.points = []   # (label, net, centre) for test points
        self.symbols = []  # refs and test point labels drawn in the schematic

    # Copper.

    def ring(self):
        """The M-page power ring: V+ round the top, GND round the bottom."""
        for net, lane_id in zip(RING_NETS, module.power_ring(self.sh)):
            self.lanes.setdefault(net, []).append(lane_id)

    def lane(self, net, pts, **kw):
        lane_id = E.lane(self.sh, pts, **kw)
        self.lanes.setdefault(net, []).append(lane_id)
        self.laid += 1
        return lane_id

    # Parts.

    def resistor(self, ref, cx, cy, vertical=True, lead=11.0, show_value=False):
        """`show_value` labels it "R1 · 220 Ω" rather than "R1"."""
        label = f"{ref} · {self.circuit[ref].text}" if show_value else ref
        self.leads.append((ref, E.resistor(self.sh, cx, cy, vertical=vertical, lead=lead, label=label)))

    def ceramic_cap(self, ref, cx, cy, vertical=False, lead=8.0):
        self.leads.append((ref, E.ceramic_cap(self.sh, cx, cy, vertical=vertical, lead=lead, label=ref)))

    def led(self, ref, cx, cy, anode, lead_anode=12.0, lead_cathode=9.0):
        self.leads.append((ref, E.led(self.sh, cx, cy, anode=anode, lead_anode=lead_anode,
                                      lead_cathode=lead_cathode, label=ref)))

    def fold_switch(self, ref, stubs=True):
        """The corner switch: its flap pad presses on one point on each of its two lanes."""
        self.leads.append((ref, E.fold_switch(self.sh, stubs=stubs)))

    def loop(self, net, x, y, side="right"):
        """A patch loop on `net`'s lane, labelled with the net's name."""
        self.loops.append((net, E.patch_loop(self.sh, x, y, net, side=side)))

    def test_point(self, net, x, y, label, side="right"):
        E.test_point(self.sh, x, y, label, side=side)
        self.points.append((label, net, (x, y)))

    # Schematic.

    def symbol(self, ref):
        """The part a schematic symbol stands for, so its label and value come from the
        circuit. Every part must be drawn exactly once."""
        self.symbols.append(ref)
        return self.circuit[ref]

    def probe(self, label):
        """A test point's schematic symbol. Every test point must be drawn exactly once."""
        self.symbols.append(label)
        return label

    # The check.

    def _touches(self, seg):
        return {net for net, ids in self.lanes.items()
                for i in ids if distance(list(seg), self.sh.lanes[i]) < 0.01}

    def check(self):
        problems = []
        for net in self.circuit.nets:
            n = len(self.lanes.get(net, []))
            if n != 1:
                problems.append(f"net {net} has {n} strips of copper, not 1")
        for net in self.lanes:
            if net not in self.circuit.nets and net not in RING_NETS:
                problems.append(f"lane on {net}, which no part uses")
        placed = {}
        for ref, leads in self.leads:
            placed[ref] = placed.get(ref, 0) + 1
            part = self.circuit[ref]
            if part.polar:
                for pin, seg in leads.items():
                    if self._touches(seg) != {part.pins[pin]}:
                        problems.append(f"{ref}'s {pin} lands on {_names(self._touches(seg))}, "
                                        f"but the circuit puts it on {part.pins[pin]}")
                continue
            landed = [self._touches(seg) for seg in leads]
            if any(len(nets) != 1 for nets in landed):
                problems.append(f"{ref}: its leads touch " + "; ".join(_names(n) for n in landed)
                                + " (each must touch exactly one net)")
            elif sorted(n for nets in landed for n in nets) != sorted(part.nets):
                problems.append(f"{ref} lands on {[n for nets in landed for n in nets]}, "
                                f"but the circuit puts it on {list(part.nets)}")
        for net, feet in self.loops:
            if self._touches(feet) != {net}:
                problems.append(f"patch loop {net} stands on {_names(self._touches(feet))}")
        for label, net, centre in self.points:
            if self._touches((centre, centre)) != {net}:
                problems.append(f"{label} sits on {_names(self._touches((centre, centre)))}, not {net}")
            if self.symbols.count(label) != 1:
                problems.append(f"{label} is drawn {self.symbols.count(label)} times in the schematic, not once")
        for ref in self.circuit.parts:
            if placed.get(ref, 0) != 1:
                problems.append(f"{ref} is placed {placed.get(ref, 0)} times on the page, not once")
            if self.symbols.count(ref) != 1:
                problems.append(f"{ref} is drawn {self.symbols.count(ref)} times in the schematic, not once")
        if problems:
            raise RuntimeError(f"{self.sh.title}: the page doesn't match its circuit:\n  " + "\n  ".join(problems))


def _names(nets):
    return " and ".join(sorted(nets)) or "no copper"
