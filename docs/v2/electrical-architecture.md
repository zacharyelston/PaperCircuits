# V2 electrical architecture (proposal)

Status: **proposal** for [#40](https://github.com/zacharyelston/PaperCircuits/issues/40). Every number marked **[T4]** waits on the bench results from the [T4 book interconnect tests](../../out/T4-book-interconnects.pdf) ([#39](https://github.com/zacharyelston/PaperCircuits/issues/39)) and is not final until those are logged. Nothing here changes V1 pages.

V2 pages are two-layer paper PCBs bound in a ring binder. The rings and holes only hold pages; they carry no current. Power and signals travel between pages through a **spine link** at each page boundary.

## Decisions at a glance

| Question | Proposal | Status |
|---|---|---|
| Shared nets | Five conductors: GND, BUS A, V+, BUS B, GND | Proposed |
| Pin order | Supply-symmetric, plus an orientation mark so BUS A and BUS B cannot be swapped | Proposed |
| Topology | A chain of short links, one per page boundary, with every page passing all five conductors on | Proposed; construction **[T4]** |
| Where links sit | Between holes, on or close to the ring axis, not at the page edge | **[T4]** |
| Supply | 3 × AA, 4.5 V nominal, as V1 | Proposed |
| Protection | One resettable fuse (0.1 A hold) at power entry; no series diode | Proposed |
| Book budget | 16 pages (15 boundaries), 100 mA total, 0.25 V drop at most | Proposed; link resistance **[T4]** |
| Removable pages | Not while powered; a page is replaced by cutting and resoldering its two links | Proposed |
| V1 compatibility | V1 and V2 pages don't share a binder | Proposed |

## 1. The hinge sets the geometry

A ring binder turns each page about the line through its holes, the ring axis, at x = 12 mm. That makes the spine zone two very different places:

- **On the axis, between holes:** a point there barely moves when its page turns. A link running along the axis, parallel to the spine, twists by up to 180° along its length instead of folding. A laptop routes its screen cable through the hinge for the same reason.
- **At the page edge (x = 0):** that point is 12 mm from the axis. When the spread between two pages opens fully, their two edge points end up about 24 mm apart, and a link between them flexes that whole distance every time. Ring play adds about 2 mm more, because a page slides on its rings.

So V2 links belong between holes, as close to the axis as the hole keep-outs allow. Edge links stay in the T4 tests as a comparison. If they fail, the standard will prohibit them.

An open spread shows the **back (side B) of the left page and the front (side A) of the right page**. Those are exactly the two faces a link joins. Each page therefore carries the spine pads on both faces: side A pads take the link from the previous page, and side B pads send it on to the next.

## 2. The pin contract

Each page boundary has one link of five conductors, in this order from the top of the page:

| Pin | Net | Use |
|---|---|---|
| 1 | GND | Return, conductor 1 of 2 |
| 2 | BUS A | Signal, 0 V to V+ |
| 3 | V+ | Protected supply, 4.5 V nominal |
| 4 | BUS B | Signal, 0 V to V+ |
| 5 | GND | Return, conductor 2 of 2 |

- **Supply-symmetric on purpose.** A link turned end for end maps GND to GND and V+ to V+, so it cannot reverse the supply. It does swap BUS A and BUS B, which is **not** harmless: the wrong receiver may hear a signal, or two drivers may contend. Every ribbon therefore has a visible pin-1 stripe at C1, every pad block marks C1, and assembly instructions require the stripe to stay on C1 at both ends. A later connector must be keyed as well as marked.
- **Two GND conductors.** They share the return current, halve the return resistance, and keep the book powered if one GND joint cracks. Tie them together on every page.
- **Same nets as V1.** V1 already shares V+, GND, BUS A and BUS B through its holes, so V1 lessons need no new nets, only a new way of reaching them.

**Pads [T4].** Each pin is a 5 mm tape pad at an 8 mm pitch (5 mm tape plus 3 mm clearance), 37 mm overall. A strip between H2 and H3 has 64 mm clear of the hole keep-outs (y 116.5 to 180.5), so a block centred on y = 148.5 fits with room for strain relief. The x position follows the T4 results.

**Pass-through.** Every V2 page carries all five conductors from its side A pads to its side B pads through a validated layer transition, whether it uses them or not. The book's power never depends on which lessons are bound in it. A page taps V+ or GND from its own spine strip with a soldered joint. V2 allows soldered joints; V1's "no unsoldered overlaps" rule still applies.

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
- **GND return:** 15 pairs in series. The two conductors in each pair are tied together at both ends and must measure at most **0.05 Ω as a pair**.
- **Whole path:** 1.5 Ω on V+ plus 0.75 Ω on GND gives 2.25 Ω, or 0.225 V at 100 mA.

Those 0.1 Ω V+ and 0.05 Ω GND-pair limits are T4's pass marks. T4 measures the GND pair as one parallel return; dividing either GND conductor's voltage by the total current would understate its resistance because the current splits between them.

**Measuring it.** A 0.1 Ω link is below what a meter's 200 Ω range can read (its resolution is 0.1 Ω). T4 measures each link as a voltage drop instead:
- Pass a known load current through the book: a 100 Ω resistor at the far page draws about 45 mA.
- Read the millivolts across the link on the 200 mV range.
- Divide by the current: 45 mA through 0.1 Ω is 4.5 mV, easy to read.

**Voltage at the far page.** Fresh alkaline cells give 4.5 to 4.8 V. Through a book at the limit that becomes about 4.3 to 4.6 V at the far page. V1's resistor values were chosen for 4.5 V, so a red LED at the far page runs up to about 8 % below its V1 current. That's not a visible difference.

## 4. Faults

| Fault | What happens | Protection |
|---|---|---|
| V+ shorted to GND on any page | Cell current flows until the fuse trips; the peak and duration depend on the cells, PTC and wiring | **Provisional [T4]:** characterize trip time and peak joint temperature with the intended 0.1 A-hold fuse before making a safety claim. |
| A link fitted end for end | V+ and GND remain correct, but BUS A and BUS B swap | Pin-1 stripe at C1 now; a keyed connector if one is adopted later |
| BUS A or BUS B shorted to V+ or GND | Under 5 mA flows | **Bus drivers:** every page that drives a bus does so through at least 1 kΩ, and receivers are high-impedance. |
| One GND joint cracks | The book stays powered on the other GND conductor | Two GND pins; T4 records it as a fail even so |
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
- **Replacing a page:** switch off, cut or unsolder its two links, swap the page, resolder, then check the voltage on its spine test points before switching on again.
- **Clip-on links,** for classes that want removable pages, are a candidate for a later T4 round. They're out of scope for now.

## 7. V1

- **Separate books:** V1 pages draw power through their holes, which V2 makes mechanical only. So V1 and V2 pages don't share a binder.
- **V1 stays buildable:** its standard, pages and power page P1 stay reproducible and unchanged until V2's bench validation is done.
- **Table-top modules:** the M pages power each other through edge connectors on the table, not through a binder. #46 decides whether they move onto this contract or keep their edge connectors as a table-top variant.

## 8. Prototype that closes #40

A three-page book that is run through T4's chosen flex-life cycles:
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
- The pad x position and exact pitch. **[T4]**
- The flex-life target itself: 500 or 1,000 open-close cycles.
- Whether the synth (#46) puts audio on a bus or keeps patch leads.
