# T6  Multi-page synth buses

Build four double-sided cards so power, pitch control and audio cross real page boundaries and the last card provides a safe line-level output.

## PDF title

T6 multi-page synth buses

## Status

V2 four-card synth test

## Power A

- title: Card 1A · fused power entry
- subtitle: A switched 3×AA holder and resettable fuse feed the book from its first page.
- body: LED1 confirms protected V+ is live. Switch off before changing any spine link.
- footer: sheet 1 of 10 · card 1 side A

## Power B

- title: T6  Card 1: power back and book map
- subtitle: Follow the four-card signal flow before laying copper or joining the spine.
- body: Each boundary gets four independent flexible links. V+ and GND cross every card; BUS A is used on side A and BUS B on side B. The rings remain mechanical only.
- footer: sheet 2 of 10 · card 1 side B

## Controller A

- title: Card 2A · BUS A pencil controller
- subtitle: The controller creates pitch control on side A and sends it through the book.
- body: Adapted from M3. V+ feeds a 13 kΩ resistor and pencil ribbon. The movable wiper drives BUS A; no audio or load current belongs on this bus.
- footer: sheet 3 of 10 · card 2 side A

## Controller B

- page_title: T6  Card 2: controller back
- subtitle: BUS A uses only a short spine stub here; BUS B crosses its named side-B work area.
- title: Pass-through face
- body: This face contains no synth function. Wrap BUS A only far enough to reach its spine link, and carry BUS B across side B. Do not extend BUS A through this work area.
- footer: sheet 4 of 10 · card 2 side B

## Oscillator A

- page_title: T6  Card 3: oscillator input
- subtitle: BUS A ends at R4; four separated node pairs wrap to the reverse routing layer.
- title: M1 oscillator · BUS A in
- body: The astable reads BUS A as PITCH. Its upper and lower copper islands never cross either bus; matching wrap labels continue each node on side B.
- footer: sheet 5 of 10 · card 3 side A

## Oscillator B

- page_title: T6  Card 3: oscillator output
- subtitle: Four parallel back routes replace every insulated crossing on the oscillator face.
- title: Side-B routes · protected BUS B
- body: Match both ends of each Q1C, Q2B, Q1B and OUT route to side A. R5 connects only OUT to the shortened BUS B rail; the four channels must remain isolated.
- footer: sheet 6 of 10 · card 3 side B

## Filter A

- page_title: T6  Card 4: filter front
- subtitle: BUS A passes across side A; BUS B remains only a spine stub before reaching the back.
- title: Pass-through face
- body: Card 4 does not consume BUS A, but carries it across its named work area. Wrap BUS B only at the spine so audio reaches the filter on side B.
- footer: sheet 7 of 10 · card 4 side A

## Filter B

- page_title: T6  Card 4: filter and output
- subtitle: BUS B feeds the M6 pencil filter and an integrated one-input M7 line-output stage.
- title: BUS B · filter · LINE out
- body: The wiper selects pencil resistance before FILTER. C1 removes buzz; R1, C2 and R2 make an AC-coupled line output. Connect LINE and GND only to a line/AUX input.
- footer: sheet 8 of 10 · card 4 side B

## Sheet 7

- title: T6  Build and test the four-card synth
- subtitle: Duplex-print pairs 1–2, 3–4, 5–6 and 7–8 at 100 %, flipping on the long edge. Print sheets 9 and 10 once.
- footer: sheet 9 of 10

## You need

- Four double-sided cards, a three-hole punch and a three-ring binder
- 5 mm copper tape for V+ and buses; 12 mm copper tape for GND
- Three sets of four flexible spine links made by the method selected in T4
- Card 1: switched 3×AA holder, 0.1 A resettable fuse, R1 1 kΩ and LED1
- Card 2: R1 13 kΩ, a soft 6B pencil, clear tape and card for one wiper
- Card 3: R1/R2/R5 1 kΩ, R3 10 kΩ, R4 4.7 kΩ, LED1 red, C1/C2 100 nF, Q1/Q2 2N3904
- Card 4: R1 22 kΩ, R2 4.7 kΩ, C1 47 nF, C2 1 µF, a soft 6B pencil, clear tape and card for one wiper
- Solder, clip leads, a multimeter, 3 AA cells, a line/AUX amp and a suitable cable

## 1 · Print the four cards

1. Duplex-print only the numbered pairs 1–2, 3–4, 5–6 and 7–8 at 100 %, flipping on the long edge.
2. Hold each card to a light. Its four spine wraps and link targets must register face-to-face, and no rail may enter a hole keep-out.
3. Punch and mark the cards 1 power, 2 controller, 3 oscillator and 4 filter/output.

## 2 · Build power and controller

1. On card 1, connect the switched holder through F1 to V+ and connect black to GND. Fit R1 and LED1; verify the switch and fuse are upstream of every other card.
2. On card 2, lay V+ and GND on both faces, BUS A on side A and BUS B on side B. Wrap each bus only to its opposite-face spine stub.
3. Build the pencil controller. With power off, verify all four link targets are isolated from unlike nets.

## 3 · Build oscillator

1. On side A, stop BUS A at R4 and keep BUS B as a spine stub. Lay the eight labelled node ends without extending any across a bus.
2. On side B, join each matching pair through its own 10 mm-pitch channel. Fit R5 between OUT and the shortened BUS B rail; no channel may overlap another.
3. Check Q1C, Q2B, Q1B and OUT end-to-end through their reverse routes, then check every unlike pair for OL. Power the card and confirm LED1 flashes.

## 4 · Build filter and output

1. Lay the four rails and short opposite-face stubs. Keep BUS A as pass-through only.
2. Shade the tone track, fit C1 and the BUS B wiper, then add R1, C2 and R2 exactly as shown.
3. Verify LINE is AC-coupled and isolated from V+. Connect LINE and GND only to a powered speaker or amplifier line/AUX input—never headphones or a bare speaker.

## 5 · Link and test the book

1. Bind cards 1–2–3–4. With power off, join V+, BUS A, BUS B and GND at all three boundaries using the labelled targets.
2. Record each of the 12 link checks separately. Check every unlike pair for OL before inserting batteries.
3. Switch on and record BUS A and BUS B idle/active voltage, total current and LINE output amplitude.
4. Move the controller wiper to change pitch and the filter wiper to change tone. No clip-lead signal bypass is allowed.

## 6 · Flex and inspect

1. Open and close each page 100 times while the synth sounds. Record crackle, pitch jumps, silence or resets, then repeat at 1,000 cycles if it passes.
2. Remove BUS A at boundary 2–3: the oscillator must stop. Restore it and remove BUS B at boundary 3–4: LED1 must keep flashing while LINE goes quiet.
3. Recheck all 12 links and inspect every spine wrap for cracked copper, lifted adhesive or a shifted link.

## Pass or fail

- **Pass:** four physical cards exchange power, pitch and audio only through labelled spine links; R5 protects BUS B; LINE drives a line input; flexing causes no dropout.
- **Fail:** a clip-lead bypass is needed, a bus crosses the wrong work area, BUS B can be hard-shorted by its driver, or any page requires a through-page via.

## Results

- title: T6  Four-card synth results
- subtitle: Record every inter-page link, bench voltage and current before and after flexing.
- footer: sheet 10 of 10
- continuity: Boundary-by-boundary continuity
- continuity_note: Measure with power disconnected. Every unlike pair must remain OL.
- new: New
- cycles: After flex
- signals: Powered bench measurements

## Bus decision

- Four physical cards were linked in the printed order
- Every boundary passed all four continuity checks
- BUS A occupied only side-A work areas
- BUS A controlled oscillator pitch across boundary 2–3
- BUS B occupied only side-B work areas
- R5 limited the BUS B short-circuit current
- BUS B carried audio across boundary 3–4
- LINE drove a line/AUX input without an external M7 page

## Notes

- Pitch range, tone change and LINE level
- Idle/active current and BUS voltages
- Boundary crackle, dropout or flex damage
- Builder / date
