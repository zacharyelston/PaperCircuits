# T6  Multi-page synth buses

Build three double-sided cards so BUS A carries pitch to an oscillator and BUS B carries its audio to a filter.

## PDF title

T6 multi-page synth buses

## Status

V2 three-card synth test

## Controller A

- title: Card 1A · BUS A pencil controller
- subtitle: The first card creates pitch control on side A and sends it through the book.
- body: Adapted from M3. V+ feeds a 13 kΩ resistor and pencil ribbon. The movable wiper drives BUS A; no audio or load current belongs on this bus.
- footer: sheet 1 of 8 · card 1 side A

## Controller B

- page_title: T6  Card 1: controller back
- subtitle: BUS A uses only a short spine stub here; BUS B passes across its named side-B work area.
- title: Pass-through face
- body: This face contains no synth function. Wrap BUS A only far enough to reach its spine stub, and carry BUS B across side B for the next page. Do not extend BUS A through this work area.
- footer: sheet 2 of 8 · card 1 side B

## Oscillator A

- page_title: T6  Card 2: oscillator input
- subtitle: BUS A enters M1 on side A; the oscillator's OUT trace returns to the spine at BUS B height.
- title: M1 oscillator · BUS A in
- body: The M1 astable reads BUS A as PITCH. Its OUT trace is not a side-A BUS B rail: it runs only to the spine, wraps onto side B and becomes BUS B there.
- footer: sheet 3 of 8 · card 2 side A

## Oscillator B

- page_title: T6  Card 2: oscillator output
- subtitle: The wrapped M1 output becomes the full BUS B audio rail on this face.
- title: BUS B audio out
- body: Burnish the side-A OUT wrap onto this BUS B rail. BUS A remains only a short spine stub on side B. Test BUS B to GND here before linking the next card.
- footer: sheet 4 of 8 · card 2 side B

## Filter A

- page_title: T6  Card 3: filter front
- subtitle: BUS A passes across side A; BUS B remains only a spine stub before reaching the back.
- title: Pass-through face
- body: Card 3 does not consume BUS A, but carries it across its named work area. Wrap BUS B only at the spine so the audio reaches the filter on side B.
- footer: sheet 5 of 8 · card 3 side A

## Filter B

- page_title: T6  Card 3: tone filter
- subtitle: BUS B arrives from the oscillator page and feeds the M6 pencil filter.
- title: BUS B · pencil tone filter
- body: Adapted from M6. The wiper selects pencil resistance before OUT, while C1 sends high-frequency buzz to GND. Patch OUT through M7 before a line/AUX input.
- footer: sheet 6 of 8 · card 3 side B

## Sheet 7

- title: T6  Build and test the three-card synth
- subtitle: Print sheets 1-2, 3-4 and 5-6 as three double-sided cards, flipping each on the long edge. Print sheets 7 and 8 once.
- footer: sheet 7 of 8

## You need

- Three double-sided cards, a three-hole punch and a three-ring binder
- 5 mm copper tape for V+ and buses; 12 mm copper tape for GND
- Two sets of four flexible spine links made by the method selected in T4
- Card 1: R1 13 kΩ, a soft 6B pencil, clear tape and card for one wiper
- Card 2: R1/R2 1 kΩ, R3 10 kΩ, R4 4.7 kΩ, LED1 red, C1/C2 100 nF, Q1/Q2 2N3904
- Card 3: C1 47 nF, a soft 6B pencil, clear tape and card for one wiper
- Solder, clip leads, a multimeter, fused 4.5 V power, built M7 output page and a line/AUX amp

## 1 · Print the three cards

1. Duplex-print each numbered pair at 100 %, flipping on the long edge. Do not duplex sheets 2-3 or 4-5 together.
2. Hold each card to a light. Its four spine wraps must register face-to-face, and no rail may enter an 8 mm hole keep-out.
3. Punch all three cards and mark them 1 controller, 2 oscillator and 3 filter.

## 2 · Build card 1

1. Lay V+ and GND on both faces and wrap both at the spine. Lay BUS A across side A and BUS B across side B.
2. Wrap each bus only onto its short opposite-face spine stub. Do not carry it across the wrong work area.
3. Build R1, the pencil ribbon and BUS A wiper on side A. Confirm all four spine pads are isolated before linking pages.

## 3 · Build card 2

1. Lay the four rails and short opposite-face stubs exactly as on card 1.
2. Build the M1 oscillator on side A. BUS A is PITCH. Follow the labelled OUT route to the BUS B-height spine wrap.
3. On side B, burnish that wrap onto BUS B. Power only card 2 and confirm LED1 lights when BUS A is connected through at least 13 kΩ to V+.

## 4 · Build card 3

1. Lay the four rails and short opposite-face stubs. Keep BUS A as pass-through only.
2. On side B, shade the tone track hard with 6B pencil, fit C1, W1 and the BUS B wiper, and leave OUT as a local patch point.
3. Confirm BUS B is isolated from V+, GND, BUS A and OUT before linking pages.

## 5 · Link and test the book

1. Bind the cards in order 1-2-3. With power off, join V+, BUS A, BUS B and GND across both page boundaries using the T4 flexible-link method.
2. Check each net end-to-end and check every pair of unlike nets for OL. Then connect fused 4.5 V power to card 1 V+ and GND.
3. Patch card 3 OUT through M7 to a powered speaker or amp line/AUX input. Never use headphones or a bare speaker.
4. Move the card-1 wiper to change pitch; move the card-3 wiper to change tone. Both controls must work through the bound pages without clip-lead signal bypasses.

## 6 · Flex and inspect

1. Open and close each page 100 times while the synth sounds. Record crackle, pitch jumps, silence or resets, then repeat at 1,000 cycles if it passes.
2. Remove the BUS A link at boundary 1-2: the oscillator must stop. Restore it and remove BUS B at boundary 2-3: LED1 must keep flashing while the amp goes quiet.
3. Inspect all eight boundary joints and every spine wrap for cracked copper, lifted adhesive or a shifted link.

## Pass or fail

- **Pass:** three physical cards exchange pitch and audio only through their labelled spine links, each bus occupies only its named work face, and flexing causes no dropout.
- **Fail:** a clip lead bypass is needed between cards, a bus crosses the wrong work area, a bus carries supply current, or any page requires a through-page via.

## Results

- title: T6  Three-card synth results
- subtitle: Record all four inter-page links and prove that BUS A and BUS B cross real page boundaries.
- footer: sheet 8 of 8
- continuity: End-to-end continuity
- continuity_note: Measure across both page boundaries with power disconnected; every unlike pair must remain OL.
- new: New
- cycles: After flex
- signals: Functional signal tests

## Bus decision

- Three physical synth cards were linked
- BUS A occupied only side-A work areas
- BUS A crossed both page boundaries
- BUS A controlled oscillator pitch
- BUS B occupied only side-B work areas
- BUS B crossed both page boundaries
- BUS B carried oscillator audio
- No clip-lead signal bypass or page via was required

## Notes

- Pitch range and tone change
- Boundary crackle, dropout or flex damage
- Builder / date
