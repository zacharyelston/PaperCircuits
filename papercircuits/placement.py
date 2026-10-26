"""The placement layer: where a page's copper and parts go, bound to its circuit.

Every lane belongs to a net, and every part is placed by its ref, so check() can compare
the page with the circuit:

- each net in the circuit has exactly one strip: one lane of copper, or a pencil track
  (standard §4: one strip per node)
- each lead lands on its own net's strip and touches no other net; a polarised part's
  leads must each land on their own pin's net
- each patch loop and test point stands on its own net's lane
- each pencil track's wiper lane runs alongside it, far enough for no smudge to bridge
  them and near enough for the wiper's strip to reach both
- each part's schematic symbol, and each test point's, is drawn exactly once
- every part a learner buys appears in the "You need" list

The clearance check still runs as before; this one covers what clearance can't: that the
copper joins what the circuit says it joins.

Parts that print a label take `label`: "ref" prints "R1", "value" prints "R1 · 220 Ω"
(or the part's note, such as "LED1 · green"), and None prints nothing.
"""

from . import elements as E
from . import module
from . import standard as S
from .circuit import BOUGHT
from .draw import MUTED
from .drc import distance

RING_NETS = ("V+", "GND")
WIPER_OVERLAP = 2.0  # how far a wiper's strip must reach past the lane and into the pencil


class Placement:
    def __init__(self, sh, circuit):
        self.sh, self.circuit = sh, circuit
        self.strips = {}  # net -> [polygons]: lanes and pencil tracks
        self.laid = 0  # lanes laid with lane(), so not counting an M page's ring
        self.leads = []  # (ref, [lead segments]) or (ref, {pin: lead segment})
        self.loops = []  # (net, feet segment)
        self.points = []  # (label, net, centre) for test points
        self.pencils = {}  # ref -> (track polygon, wiper strip length or None)
        self.symbols = []  # refs and test point labels drawn in the schematic

    # Copper and pencil.

    def ring(self):
        """The M-page power ring: V+ round the top, GND round the bottom."""
        for net, lane_id in zip(RING_NETS, module.power_ring(self.sh)):
            self.strips.setdefault(net, []).append(self.sh.lanes[lane_id])

    def lane(self, net, pts, **kw):
        lane_id = E.lane(self.sh, pts, **kw)
        self.strips.setdefault(net, []).append(self.sh.lanes[lane_id])
        self.laid += 1
        return lane_id

    def pencil(self, ref, x0, y0, x1, y1, **kw):
        """A pencil track to shade. It's the strip of its part's "track" net, so a lead
        laid across it is checked like a lead on copper."""
        E.pencil_track(self.sh, x0, y0, x1, y1, **kw)
        rect = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        self.strips.setdefault(self.circuit[ref].pins["track"], []).append(rect)
        self.pencils[ref] = (rect, None)

    def wiper(self, ref, x0, y0, x1, y1, strip_len, **kw):
        """The cut-out wiper for pencil part `ref`."""
        E.wiper_card(self.sh, x0, y0, x1, y1, strip_len, **kw)
        self.pencils[ref] = (self.pencils[ref][0], strip_len)

    # Parts.

    def _label(self, ref, label):
        return {"ref": ref, "value": f"{ref} · {self.circuit[ref].text}", None: None}[label]

    def _place(self, ref, leads):
        self.leads.append((ref, leads))

    def resistor(self, ref, cx, cy, vertical=True, lead=11.0, label="ref"):
        self._place(ref, E.resistor(self.sh, cx, cy, vertical=vertical, lead=lead, label=self._label(ref, label)))

    def ceramic_cap(self, ref, cx, cy, vertical=False, lead=8.0, label="ref"):
        self._place(ref, E.ceramic_cap(self.sh, cx, cy, vertical=vertical, lead=lead, label=self._label(ref, label)))

    def ldr(self, ref, cx, cy, lead=11.0, label="ref"):
        self._place(ref, E.ldr(self.sh, cx, cy, lead=lead, label=self._label(ref, label)))

    def ptc(self, ref, cx, cy, lead=12.0, label="ref"):
        self._place(ref, E.ptc(self.sh, cx, cy, lead=lead, label=self._label(ref, label)))

    def led(self, ref, cx, cy, anode, lead_anode=12.0, lead_cathode=9.0, label="ref"):
        self._place(
            ref,
            E.led(
                self.sh,
                cx,
                cy,
                anode=anode,
                lead_anode=lead_anode,
                lead_cathode=lead_cathode,
                label=self._label(ref, label),
            ),
        )

    def diode(self, ref, cx, cy, cathode="right", lead=8.0, label="ref"):
        self._place(ref, E.diode(self.sh, cx, cy, lead=lead, label=self._label(ref, label), cathode=cathode))

    def electrolytic(self, ref, x, y_plus, y_minus, label="ref"):
        self._place(ref, E.electrolytic(self.sh, x, y_plus, y_minus, label=self._label(ref, label)))

    def radial_cap(self, ref, x_plus, x_minus, y, label="ref", **kw):
        self._place(ref, E.radial_cap(self.sh, x_plus, x_minus, y, label=self._label(ref, label), **kw))

    def transistor(self, ref, cx, cy, legs, label="ref"):
        self._place(ref, E.transistor(self.sh, cx, cy, legs, label=self._label(ref, label)))

    def battery(self, ref, x0, y0, plus, minus, label="value", cells=3):
        """A battery holder at (x0, y0) whose red and black wires run left from it to end,
        bare, at `plus` and `minus` (each an (x, y))."""
        E.battery_holder(self.sh, x0, y0, cells=cells, label=self._label(ref, label))
        self._place(ref, {pin: E.wire_lead(self.sh, x0, *end) for pin, end in (("plus", plus), ("minus", minus))})

    def wire(self, ref, a, b, end=1.0):
        """A bare wire link from a to b. Its last `end` mm at each end must land."""
        self.sh.line(*a, *b, width=0.5, color=MUTED, cap=1)
        (ax, ay), (bx, by) = a, b
        n = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
        ux, uy = (bx - ax) / n * end, (by - ay) / n * end
        self._place(ref, [(a, (ax + ux, ay + uy)), ((bx - ux, by - uy), b)])

    def fold_switch(self, ref, stubs=True):
        """The corner switch: its flap pad presses on one point on each of its two lanes."""
        self._place(ref, E.fold_switch(self.sh, stubs=stubs))

    def tab_switch(self, ref, x, upper_y, pitch=S.PAIR_PITCH):
        """A tab switch labelled with its ref; its pad presses on one point on each lane."""
        self._place(ref, E.tab_switch(self.sh, x, upper_y, ref, pitch=pitch))

    def loop(self, net, x, y, side="right"):
        """A patch loop on `net`'s lane, labelled with the net's name."""
        self.loops.append((net, E.patch_loop(self.sh, x, y, net, side=side)))

    def test_point(self, net, x, y, label, side="right", **kw):
        E.test_point(self.sh, x, y, label, side=side, **kw)
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
        return {net for net, polys in self.strips.items() for poly in polys if distance(list(seg), poly) < 0.01}

    def check(self, listed=None):
        """Fail the build if the page doesn't match its circuit. `listed` is the set of
        refs the "You need" list covers (Words.refs("You need")); give it on any page with
        a parts list."""
        problems = []
        for net in self.circuit.nets:
            n = len(self.strips.get(net, []))
            if n != 1:
                problems.append(f"net {net} has {n} strips, not 1")
        for net in self.strips:
            if net not in self.circuit.nets and net not in RING_NETS:
                problems.append(f"lane on {net}, which no part uses")
        placed = {}
        for ref, leads in self.leads:
            placed[ref] = placed.get(ref, 0) + 1
            part = self.circuit[ref]
            if part.polar:
                for pin, seg in leads.items():
                    if self._touches(seg) != {part.pins[pin]}:
                        problems.append(
                            f"{ref}'s {pin} lands on {_names(self._touches(seg))}, "
                            f"but the circuit puts it on {part.pins[pin]}"
                        )
                continue
            landed = [self._touches(seg) for seg in leads]
            if any(len(nets) != 1 for nets in landed):
                problems.append(
                    f"{ref}: its leads touch "
                    + "; ".join(_names(n) for n in landed)
                    + " (each must touch exactly one net)"
                )
            elif sorted(n for nets in landed for n in nets) != sorted(part.nets):
                problems.append(
                    f"{ref} lands on {[n for nets in landed for n in nets]}, "
                    f"but the circuit puts it on {list(part.nets)}"
                )
        for ref, (track, strip_len) in self.pencils.items():
            placed[ref] = placed.get(ref, 0) + 1
            problems += self._check_wiper(ref, track, strip_len)
        for net, feet in self.loops:
            if self._touches(feet) != {net}:
                problems.append(f"patch loop {net} stands on {_names(self._touches(feet))}")
        for label, net, centre in self.points:
            if self._touches((centre, centre)) != {net}:
                problems.append(f"{label} sits on {_names(self._touches((centre, centre)))}, not {net}")
            if self.symbols.count(label) != 1:
                problems.append(f"{label} is drawn {self.symbols.count(label)} times in the schematic, not once")
        for ref, part in self.circuit.parts.items():
            if placed.get(ref, 0) != 1:
                problems.append(f"{ref} is placed {placed.get(ref, 0)} times on the page, not once")
            if self.symbols.count(ref) != 1:
                problems.append(f"{ref} is drawn {self.symbols.count(ref)} times in the schematic, not once")
            if listed is not None and part.kind in BOUGHT and ref not in listed:
                problems.append(f"{ref} isn't in the You need list")
        if problems:
            raise RuntimeError(f"{self.sh.title}: the page doesn't match its circuit:\n  " + "\n  ".join(problems))

    def _check_wiper(self, ref, track, strip_len):
        if strip_len is None:
            return [f"{ref} has no wiper"]
        wiper_net = self.circuit[ref].pins["wiper"]
        lanes = self.strips.get(wiper_net, [])
        if not lanes:
            return []  # reported as a net with no strip
        gap = min(distance(track, lane) for lane in lanes)
        if gap < S.NET_CLEARANCE - 0.01:
            return [f"{ref}'s track is {gap:.1f} mm from {wiper_net}, closer than {S.NET_CLEARANCE:g} mm"]
        if gap + S.TAPE_W + WIPER_OVERLAP > strip_len + 0.01:
            return [
                f"{ref}'s wiper strip ({strip_len:g} mm) can't reach from {wiper_net} across "
                f"the {gap:.1f} mm gap and into the pencil"
            ]
        return []


def _names(nets):
    return " and ".join(sorted(nets)) or "no copper"
