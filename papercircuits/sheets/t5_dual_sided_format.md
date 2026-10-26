# T5  Dual-sided power format

Validate wrapped V2 power rails and a working load on both faces.

## PDF title

T5 dual-sided power format

## Status

V2 format test

## Rail labels

- V+: V+ · top rail
- GND: GND · wide bottom rail

## Side A

- load_title: Side A load
- load_body: R1 and LED1 run directly from V+ to GND. A simple load does not use a signal bus.
- rule_title: Routing rule
- rule_body: Wrap around an edge to change faces. A soldered wire via is an exception only when no safe wrap path exists.
- footer: sheet 1 of 4 (side A)

## Side B

- title: T5  Power test: side B
- subtitle: This side prints behind sheet 1. V+ and GND reach it through the two edge wraps.
- load_title: Side B load
- load_body: R2 and LED2 run directly from V+ to GND, independently of the side-A load.
- wrap_title: No page vias
- wrap_body: V+ wraps over the top and GND over the bottom. Build no signal bus and no through-page via on this power test.
- footer: sheet 2 of 4 (side B)

## Sheet 3

- title: T5  Build and test the dual-sided format
- subtitle: Print sheets 1 and 2 double-sided on card, flipping on the long edge. Print sheets 3 and 4 once.
- footer: sheet 3 of 4

## You need

- One card printed double-sided (sheets 1 and 2), a three-hole punch and a three-ring binder
- 5 mm copper tape for V+; 12 mm copper tape for GND
- Two 1 kΩ resistors, R1 and R2; two red 5 mm LEDs, LED1 and LED2
- A soldering iron and solder, clip leads and a multimeter
- A fused 3 × AA holder, 4.5 V nominal

## 1 · Print and inspect

1. Check the 100 mm scale bar on both faces. Hold the card to a light: each side-B rail must sit directly behind its side-A partner.
2. Punch the three mechanical holes. Confirm that no copper guide enters an 8 mm hole keep-out.
3. Mark the two faces A and B before laying tape.

## 2 · Lay the power rails

1. Lay V+ as one continuous 5 mm strip from the side-A spine, across the top rail, over the top edge and along the side-B top rail to its spine.
2. Lay GND the same way with 12 mm tape, using the bottom-edge wrap.
3. Burnish every fold. Do not add a bus or through-page via.
4. Follow each solid arrow to the physical edge even though the printed lane stops short. Round circle-and-dot marks are electrical test or clip points, not vias.

## 3 · Add the loads

1. On side A, add R1 and LED1 between V+ and GND. Put the LED's long anode leg toward V+.
2. On side B, add R2 and LED2 between V+ and GND. Put the LED's long anode leg toward V+.
3. Solder every component lead to its tape lane. Check that no trimmed lead reaches the other face.

## 4 · Continuity before power

1. Measure V+ and GND from side A to side B. Record the resistance on sheet 4.
2. V+ must be 0.1 Ω or less. The wide GND rail must be 0.05 Ω or less.
3. Check V+ to GND. It must read OL; find any bridge before connecting power.

## 5 · Powered proof

1. Connect the fused holder red lead to V+ A and black lead to GND A.
2. LED1 on side A and LED2 on side B must both light. The side-B load proves both power wraps.
3. Disconnect power before moving or inspecting tape.

## 6 · Flex and inspect

1. Flex each wrapped edge through 100 cycles, measure both rails, and repeat at 1,000 cycles.
2. Repeat the powered test while gently opening and closing the card in the binder. Record flicker or resets.
3. Inspect for cracked copper, lifted adhesive, torn card or a wrap that has crept sideways.

## Pass or fail

- **Pass:** both LEDs light, both rails meet their resistance limits, V+ stays isolated from GND and no flicker occurs through 1,000 cycles.
- **Fail:** any wrap needs a through-page via to complete this layout, or any copper, paper or electrical failure appears.
- If a future lesson cannot reach an edge safely, record why before permitting a soldered wire via as a documented exception.

## Results

- title: T5  Results
- subtitle: Record rail resistance in ohms and decide whether this becomes the V2 page format.
- footer: sheet 4 of 4
- continuity: Power-wrap continuity
- continuity_note: Measure V+ and GND from side A to side B with power disconnected.
- new: New
- cycles_100: 100
- cycles_1000: 1,000
- powered: Powered proof
- before: Before flex
- after: After flex

## Format decision

- V+ stayed above the first hole
- GND stayed at the bottom
- Side A/B registration was usable
- Both power edge wraps passed
- Any page via was required
- Adopt this format for the first V2 lesson

## Notes

- Page-via exception and reason
- Damage, flicker or routing changes
- Builder / date
