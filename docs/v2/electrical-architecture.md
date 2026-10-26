# V2 electrical architecture (proposal)

Status: **proposal** for [#40](https://github.com/zacharyelston/PaperCircuits/issues/40). Numbers marked **[T4]** wait on the [T4 book interconnect tests](../../out/T4-book-interconnects.pdf) ([#39](https://github.com/zacharyelston/PaperCircuits/issues/39)); power wraps marked **[T5]** wait on the [T5 dual-sided format test](../../out/T5-dual-sided-format.pdf), and face-specific signal buses marked **[T6]** wait on the [T6 synth bus test](../../out/T6-two-sided-synth-buses.pdf). Nothing here changes V1 pages.

V2 pages are two-layer paper PCBs bound in a ring binder. The rings and holes only hold pages; they carry no current. Power and signals travel between pages through four **spine links** at fixed vertical positions.

## Decisions at a glance

| Question | Proposal | Status |
|---|---|---|
| Shared nets | Wrapped V+ and GND power rails; BUS A on side A and BUS B on side B | Power **[T5]**; signals **[T6]** |
| Binding | Three mechanical holes at the common 4.25 inch (107.95 mm) pitch, centred on A4 | Proposed |
| Rail positions | V+ above H1; BUS A above H2; BUS B below H2; GND below H3 | Power **[T5]**; signals **[T6]** |
| Topology | Four short links per page boundary, with every page passing all four rails on | Proposed; construction **[T4]**, format **[T5]** |
| Where links sit | Between holes, on or close to the ring axis, not at the page edge | **[T4]** |
| Layer changes | Wrap the spine edge first; use a soldered wire via only as a documented exception | Proposed **[T5/T6]** |
| Supply | 3 × AA, 4.5 V nominal, as V1 | Proposed |
| Protection | One resettable fuse (0.1 A hold) at power entry; no series diode | Proposed |
| Book budget | 16 pages (15 boundaries), 100 mA total, 0.25 V drop at most | Proposed; link resistance **[T4]** |
| Removable pages | Not while powered; a page is replaced by cutting and resoldering its four links | Proposed |
| V1 compatibility | V1 and V2 pages don't share a binder | Proposed |

## 1. The hinge sets the geometry

A ring binder turns each page about the line through its holes, the ring axis, at x = 12 mm. That makes the spine zone two very different places:

- **On the axis, between holes:** a point there barely moves when its page turns. A link running along the axis, parallel to the spine, twists by up to 180° along its length instead of folding. A laptop routes its screen cable through the hinge for the same reason.
- **At the page edge (x = 0):** that point is 12 mm from the axis. When the spread between two pages opens fully, their two edge points end up about 24 mm apart, and a link between them flexes that whole distance every time. Ring play adds about 2 mm more, because a page slides on its rings.

So V2 links belong between holes, as close to the axis as the hole keep-outs allow. Edge links stay in the T4 tests as a comparison. If they fail, the standard will prohibit them.

V2 uses three mechanical holes at the common 4.25 inch (107.95 mm) pitch, centred vertically on the existing A4 sheet. Their centres are y = 40.55, 148.5 and 256.45 mm. This is a V2-only change: V1 retains its ISO 838-compatible four-hole spine.

An open spread shows the **back (side B) of the left page and the front (side A) of the right page**. Those are exactly the two faces a link joins. Each page therefore carries the spine pads on both faces: side A pads take the link from the previous page, and side B pads send it on to the next.

## 2. The distributed rail contract [T5/T6]

The compact five-pin T4 block is replaced by four rails distributed over the whole page. Their fixed vertical order makes a reversed or shifted link visually obvious and gives hand-laid tape much more clearance:

| Position | Net | Width | Use |
|---|---|---:|---|
| y = 29 mm, below the header and above H1 | V+ | 5 mm | Protected supply, 4.5 V nominal |
| y = 133 mm, above H2 | BUS A | 5 mm | Signal, 0 V to V+ |
| y = 164 mm, below H2 | BUS B | 5 mm | Signal, 0 V to V+ |
| y = 274 mm, below H3 | GND | 12 mm | Wide return rail |

The power-rail centres are provisional until T5 is built and the bus centres until T6 is built, but their order is the format: **V+ is always at the top, GND is always at the bottom, and the buses flank the centre ring.** The wide GND rail preserves the 0.05 Ω boundary target without requiring a second return conductor.

**Wrap-first side changes.** V+ and GND keep their fixed top and bottom rail positions, but both change faces by wrapping around the spine edge. Top- and bottom-edge wraps are unnecessary in the standard page format. BUS A remains on side A and BUS B remains on side B; neither bus is duplicated across the opposite work area. A soldered wire through the page is the last resort: the page must document why no spine-wrap route was safe, keep the via outside fold and hole keep-outs, and expose test points on both faces.

**Printed notation.** A solid arrow at the end of a copper lane means continue the tape to the page edge and fold it onto the other face; the printer is not expected to reach the physical edge. Opposing chevrons point toward every through-page construction. A circle with a centre point is reserved for an electrical solder, clip or meter target and never denotes a layer change.

**Pass-through.** Every V2 page carries V+ and GND between its two faces, BUS A across side A and BUS B across side B whether the lesson uses them or not. The book's power never depends on which lessons are bound in it. A lesson branches from the fixed rails without moving them. V2 allows soldered joints; V1's "no unsoldered overlaps" rule still applies.

**T4 remains useful.** Its link-construction and flex coupons still select wire, ribbon and solder methods for the four distributed spine links. Its compact C1-C5 block is no longer the proposed page format.

## 3. Power budget

Resistances below are for a 35 µm copper foil, the thin end of craft tape.

| Conductor | Resistance |
|---|---|
| 5 mm copper tape | about 0.1 mΩ per mm, so 25 mΩ along a 250 mm spine strip |
| 12 mm copper tape | about 0.04 mΩ per mm |
| 28 AWG stranded wire, 40 mm | about 9 mΩ |
| Good solder joint | about 1 mΩ |
| Unsoldered tape overlap | not yet measured (T0, T1) |

**Design point:** 16 pages, including the power-entry page, and 100 mA in total. The last page is 15 page-to-page boundaries from the source. That's roughly ten lessons with an LED lit on each, or an oscillator page or two. The limit is 0.25 V dropped between the supply and the last page.

- **V+ path:** 15 links in series, each at most **0.1 Ω after the flex-life target**.
- **GND return:** 15 wide links in series, each at most **0.05 Ω after the flex-life target**.
- **Whole path:** 1.5 Ω on V+ plus 0.75 Ω on GND gives 2.25 Ω, or 0.225 V at 100 mA.

The 0.1 Ω V+/bus and 0.05 Ω wide-GND limits are T5's format pass marks. T4 still supplies construction evidence for the flexible page-to-page links.

**Measuring it.** A 0.1 Ω link is below what a meter's 200 Ω range can read (its resolution is 0.1 Ω). T4 measures each link as a voltage drop instead:
- Pass a known load current through the book: a 100 Ω resistor at the far page draws about 45 mA.
- Read the millivolts across the link on the 200 mV range.
- Divide by the current: 45 mA through 0.1 Ω is 4.5 mV, easy to read.

**Voltage at the far page.** Fresh alkaline cells give 4.5 to 4.8 V. Through a book at the limit that becomes about 4.3 to 4.6 V at the far page. V1's resistor values were chosen for 4.5 V, so a red LED at the far page runs up to about 8 % below its V1 current. That's not a visible difference.

## 4. Faults

| Fault | What happens | Protection |
|---|---|---|
| V+ shorted to GND on any page | Cell current flows until the fuse trips; the peak and duration depend on the cells, PTC and wiring | **Provisional [T4]:** characterize trip time and peak joint temperature with the intended 0.1 A-hold fuse before making a safety claim. |
| Two distributed links are crossed | The wrong rail is driven, potentially shorting power | Fixed vertical positions, net labels on both faces and continuity/short tests before power |
| BUS A or BUS B shorted to V+ or GND | Under 5 mA flows | **Bus drivers:** every page that drives a bus does so through at least 1 kΩ, and receivers are high-impedance. |
| A GND joint cracks | Every page beyond it loses its return | Wide GND link, strain relief and a GND test point on every page |
| A V+ joint cracks | Every page beyond it goes dark | **Spine test points:** each page has V+ and GND test points on its spine strip, so a builder can find the break page by page. |
| An intermittent link while turning pages | Flicker or reset | The T4 flex tests set the construction and the service loop |

At the provisional worst case of 1.5 A and the resistance limits above, one boundary could dissipate about 0.225 W in V+ and 0.113 W in the combined GND return. Heat is concentrated at joints and depends on PTC trip time, so the proposal does not claim this is safe until a fused fault test records current, trip time and temperature. Do not perform that test on an unfused T4 coupon.

**No series diode at power entry.** The holder can only take its cells one way, and the contract can't reverse the supply, so a diode would cost about 0.3 V for no benefit. Revisit this if V2 ever allows other supplies, such as USB.

## 5. Signals

- **Levels:** BUS A and BUS B swing between GND and V+, at 1 mA or less.
- **No fixed use:** a page states which bus it drives or reads. The build will check that no two pages drive the same bus at once.
- **Audio:** signals that leave the book, such as the synth's audio, still go through an output page (V1's M7) to a line input. They never go to a speaker or headphones.

## 6. Pages in and out

- **No hot connection:** pages aren't inserted or removed while the book is powered.
- **Replacing a page:** switch off, cut or unsolder its four links, swap the page, resolder, then check continuity and shorts at its spine test points before switching on again.
- **Clip-on links,** for classes that want removable pages, are a candidate for a later T4 round. They're out of scope for now.

## 7. V1

- **Separate books:** V1 pages draw power through their holes, which V2 makes mechanical only. So V1 and V2 pages don't share a binder.
- **V1 stays buildable:** its standard, pages and power page P1 stay reproducible and unchanged until V2's bench validation is done.
- **Table-top modules:** the M pages power each other through edge connectors on the table, not through a binder. #46 decides whether they move onto this contract or keep their edge connectors as a table-top variant.

## 8. Prototypes that close #40

First, one T5 card must demonstrate the fixed power rails and both spine wraps with no bus and no page via. Both LEDs must work before and after the flex target, both rails must meet their resistance limits, and V+ must remain isolated from GND.

Then T6 adapts the synth's M3 controller and M6 filter onto one double-sided card. BUS A must carry pitch control only on side A, BUS B must carry audio only on side B, and disconnecting either bus must interrupt only its stated signal path. This is the first proof that the buses communicate rather than acting as extra power rails. It contributes the incremental controller/bus/filter evidence for [#46](https://github.com/zacharyelston/PaperCircuits/issues/46); M1 and M7 remain external pages for this test.

A three-page book is then run through T4's chosen flex-life cycles:
1. A V2 power-entry page: the holder, fuse, switch and LED, with the spine pads.
2. A T4 test page.
3. A second T4 test page.

It must show:
- link drops within the budget at 45 mA, before and after cycling
- no intermittent loss of V+ while turning pages, watched on the meter's minimum/maximum mode, or as LED flicker
- the fuse tripping on a planted short at page 3, with peak current, trip time and the hottest joint temperature recorded against a pass limit chosen before the test

## Still open

- Link construction: solder bridge, ribbon or stranded wire. **[T4]**
- How far from the axis a link may sit, and the length of its service loop. **[T4]**
- The exact rail centres and whether every lesson can preserve them. **[T5]**
- Which lesson geometries genuinely require a page-via exception. **[T5]**
- The flex-life target itself: 500 or 1,000 open-close cycles.
- Whether the synth (#46) puts audio on a bus or keeps patch leads.
