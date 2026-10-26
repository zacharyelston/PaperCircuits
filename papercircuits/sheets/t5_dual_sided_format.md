# T5  Dual-sided page format

Validate fixed V2 rails, wrap-first layer changes and a working circuit on both faces.

## PDF title

T5 dual-sided page format

## Status

V2 format test

## Rail labels

- V+: V+ · top rail
- BUS A: BUS A · above centre ring
- BUS B: BUS B · below centre ring
- GND: GND · wide bottom rail

## Side A

- load_title: Side A load
- load_body: R1 and LED1 run from V+ down to BUS A. BUS A exists only on side A.
- rule_title: Routing rule
- rule_body: Wrap around an edge to change faces. A soldered wire via is an exception only when no safe wrap path exists.
- footer: sheet 1 of 4 (side A)

## Side B

- title: T5  Dual-sided format: side B
- subtitle: This side prints behind sheet 1. V+ and GND wrap between faces; BUS B stays on side B.
- load_title: Side B load
- load_body: R2 and LED2 run from BUS B down to GND. BUS B exists only on side B.
- wrap_title: No page vias
- wrap_body: V+ wraps over the top and GND over the bottom. BUS A stays on side A and BUS B stays on side B. Build no through-page via.
- footer: sheet 2 of 4 (side B)

## Sheet 3

- title: T5  Build and test the dual-sided format
- subtitle: Print sheets 1 and 2 double-sided on card, flipping on the long edge. Print sheets 3 and 4 once.
- footer: sheet 3 of 4

## You need

- One card printed double-sided (sheets 1 and 2), a three-hole punch and a three-ring binder
- 5 mm copper tape for V+ and the buses; 12 mm copper tape for GND
- Two 1 kΩ resistors, R1 and R2; two red 5 mm LEDs, LED1 and LED2
- A soldering iron and solder, clip leads and a multimeter
- A fused 3 × AA holder, 4.5 V nominal

## 1 · Print and inspect

1. Check the 100 mm scale bar on both faces. Hold the card to a light: each side-B rail must sit directly behind its side-A partner.
2. Punch the three mechanical holes. Confirm that no copper guide enters an 8 mm hole keep-out.
3. Mark the two faces A and B before laying tape.

## 2 · Lay the four rails

1. Lay V+ as one continuous 5 mm strip from the side-A spine, across the top rail, over the top edge and along the side-B top rail to its spine.
2. Lay GND the same way with 12 mm tape, using the bottom-edge wrap.
3. Lay BUS A across side A only. Lay BUS B across side B only. Do not wrap either bus onto the opposite face.
4. Burnish every fold. Do not add a through-page via.
5. Follow each solid arrow to the physical edge even though the printed lane stops short. Round circle-and-dot marks are electrical test or clip points, not vias.

## 3 · Add the loads

1. On side A, add R1 and LED1 between V+ and BUS A. Put the LED's long anode leg toward V+.
2. On side B, add R2 and LED2 between BUS B and GND. Put the LED's long anode leg toward BUS B.
3. Solder every component lead to its tape lane. Check that no trimmed lead reaches the other face.

## 4 · Continuity before power

1. Measure V+ and GND from side A to side B. Measure BUS A end-to-end on side A and BUS B end-to-end on side B. Record the resistance on sheet 4.
2. V+, BUS A and BUS B must each be 0.1 Ω or less. The wide GND rail must be 0.05 Ω or less.
3. Check every pair of different rails. Every reading must be OL; find any bridge before connecting power.

## 5 · Powered proof

1. Connect the fused holder red lead to V+ A and black lead to GND A.
2. **Test 1:** clip BUS A's outer test point to GND A. LED1 on side A must light without using side B.
3. Remove that clip. **Test 2:** clip V+ B to BUS B's outer test point. LED2 on side B must light. This path proves the V+ top wrap and GND bottom wrap.
4. Disconnect power before moving or inspecting tape.

## 6 · Flex and inspect

1. Flex each wrapped edge through 100 cycles, measure all four rails, and repeat at 1,000 cycles.
2. Repeat both powered tests while gently opening and closing the card in the binder. Record flicker or resets.
3. Inspect for cracked copper, lifted adhesive, torn card or a wrap that has crept sideways.

## Pass or fail

- **Pass:** both LEDs work only in their stated test, all four rails meet their resistance limits, no rail shorts another and no flicker occurs through 1,000 cycles.
- **Fail:** any wrap needs a through-page via to complete this layout, or any copper, paper or electrical failure appears.
- If a future lesson cannot reach an edge safely, record why before permitting a soldered wire via as a documented exception.

## Results

- title: T5  Results
- subtitle: Record rail resistance in ohms and decide whether this becomes the V2 page format.
- footer: sheet 4 of 4
- continuity: Power wraps and bus continuity
- continuity_note: Measure power rails face-to-face and each bus end-to-end on its named face.
- new: New
- cycles_100: 100
- cycles_1000: 1,000
- powered: Powered proof
- before: Before flex
- after: After flex

## Format decision

- V+ stayed above the first hole
- GND stayed at the bottom
- BUS A and BUS B cleared the centre hole
- Side A/B registration was usable
- Both power edge wraps passed
- BUS A stayed on side A and BUS B stayed on side B
- Any page via was required
- Adopt this format for the first V2 lesson

## Notes

- Page-via exception and reason
- Damage, flicker or routing changes
- Builder / date
