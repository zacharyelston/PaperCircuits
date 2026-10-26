# T3  Copper oxide wafer

Grow diodes on one sheet of copper, cut them apart and test every one. Print on card.

## PDF title

T3 copper oxide wafer

## Sheet 1

- footer: sheet 1 of 3

## Fixtures

- wafer: 1  Wafer
- wafer_intro: After oxidising, lay the wafer on the frame. Rule the streets from tick to tick in fine
  permanent marker and number the dies. After dicing, put each die back on its number.
- name: name
- scrap: scrap
- wafer_size: {wafer} mm square, {die} mm dies, corners clipped
- packages: 2  Packages
- packages_intro: Put your best dies in packages. Stick a die face up in a landing, then lay each
  lead from its test point onto the die so its tip covers S or the dot. Sheet 3, section 6, says
  how.
- trays: 3  Bin trays

## Die key

One die, {key_scale}× size

- **T**  top contact: a {dot} mm dot of 6B pencil, pressed hard.
- **S**  scrape this corner back to bare copper.
- **17**  the die's number, in fine marker.
- **Dashed lines** are streets: cut along them.
- The clipped corners aren't dies. Write your wafer's name in the top-left one.

## Bin trays

- Bin 1: good
- Bin 2: fair
- Bin 3: weak
- Reject: R, S and O

## Sheet 2

- title: T3  Wafer map and results
- subtitle: Readings on the diode range, in volts. OL means over range.
- footer: sheet 2 of 3
- bins: Bins {T3}
- yield: Yield
- every_die: Every die
- every_die_hint: **Fwd:** red on T, black on S {T3}. **Rev:** red on S, black on T.
- map: Wafer map
- map_hint: write each die's bin: sort / final
- centre: dashed: the centre {centre}
- reversed: If a die reads lower with red on S, it conducts the other way: bin it on the larger
  reading ÷ the smaller, and circle its number.

## Wafer record

- Wafer
- Meter
- Open circuit
- Test current

## Recipe record

- Plate
- Heat
- Cool
- Foil
- Date

## Bin table

- 1: Good · Rev OL, Fwd reads
- 2: Fair · Rev ≥ {fair} × Fwd
- 3: Weak · Rev {weak}–{fair} × Fwd
- R: Resistor · Rev < {weak} × Fwd
- S: Short · both < {short_v} V
- O: Open · both OL
- pass: Pass · bins 1, 2 and 3

## Bin table columns

- Bin
- Rule
- Sort
- Final

## Yield table

- sort: Wafer sort
- final: Final test
- packages: Packages
- overall: Overall
- centre: Centre {centre}, sort
- edge: Edge {edge}, sort

## Yield table columns

- Stage
- In
- Pass
- Yield

## Die table

- sort: Wafer sort
- final: Final test

## Die table columns

- Die
- Fwd
- Rev
- Bin

## Sheet 3

- title: T3  Running the wafer test
- subtitle: Print on plain paper. An adult runs every hot-plate step.
- footer: sheet 3 of 3

## Why it works

Copper(I) oxide is a semiconductor. Where it meets the copper underneath, there's a barrier that
lets current through far more easily one way than the other: a diode. The pencil dot only has to
reach the oxide. How well each die works depends on how its oxide grew, so dies from one wafer
differ, just as real chips do.

## You need

- A {wafer} mm square of bare, uncoated copper foil, {foil} thick {T3}, and a spare scrap
- A single-coil electric hot plate, {plate_w} W or more {T3}, on a heatproof board
- Tongs, and safety glasses for everyone near the plate
- Washing-up liquid, a kitchen scouring pad and kitchen roll
- Old scissors, a ruler, a fine permanent marker, a craft knife or fine sandpaper, and a 6B pencil
- A multimeter with a diode range, and a 1N4148 diode (L06's D1) to check it

## Safety

- **An adult runs the hot plate** and moves the copper with tongs. Keep everyone else an arm's
  length away, and open a window or run an extractor.
- **Heat only clean, bare copper.** Never copper tape, coated foil, brass, zinc or galvanised metal:
  glue and coatings smoke, and zinc fumes make people ill.
- **Goggles on while it cools:** black flakes jump off. Hot copper looks like cold copper.
- **No acids, lye or lead.** Wipe flakes up with damp kitchen roll, and wash hands afterwards.
- Cut foil is sharp. Craft knives are for adults.

## 1 · Prepare the wafer

1. Cut the square. Clip each corner off along a diagonal from {die} mm along one edge to {die} mm
   along the other.
2. Scrub both sides with washing-up liquid and the scouring pad until bright. Rinse, dry, and hold
   it by its edges from now on.

## 2 · Oxidise

2 · Oxidise {T3}

1. **Adult:** lay the wafer flat in the middle of the cold plate and turn it to full.
2. It turns orange, purple and red, then black. Keep it at full heat for {heat_min} min after the
   coil starts to glow.
3. Switch off and leave it on the plate for {cool_min} min. The black layer flakes off as it shrinks.
   Moving it too soon keeps the black on.
4. Rinse it under the tap, rubbing gently with fingertips only, and pat it dry. The red-orange layer
   left is copper(I) oxide. Don't bend it.

## 3 · Mark the dies

1. Lay the wafer on sheet 1's frame. Rule the streets from tick to tick in fine marker. Never use
   pencil: graphite would join the dies.
2. Write the wafer's name in its top-left corner, and each die's number in its own top-left corner.
3. **S:** scrape each die's top-right corner back to shiny copper, about {scrape} mm square.
4. **T:** draw a {dot} mm dot of 6B where sheet 1 shows it, pressing hard. Keep it clear of S and the
   streets.

## 4 · Wafer sort

1. Check the meter on the 1N4148: about 0.6 V one way, OL the other.
2. On the diode range, measure every die. **Fwd:** red on T, black on S {T3}. **Rev:** red on S,
   black on T. Keep the light and the probe pressure the same throughout.
3. Bin each die by the table on sheet 2, and write its bin on the wafer map.

## 5 · Dice and final test

1. Cut along the streets with old scissors, rows first. Put each die back on its number on sheet 1.
2. Test every die again, re-bin it, and move it to its bin tray.
3. Count the bins and fill in the yields. A stage's **In** is the number that passed the stage
   before it.

## 6 · Package, if you like

1. Stick a Bin 1 die face up in a D landing with glue stick.
2. Lay each lead from its test point onto the die, its tip over S or the dot. Rub 6B into the tip's
   glue first, or solder the S lead. {T1}
3. Measure Fwd and Rev between the T and S test points.

## Pass or fail

- A die passes in bins 1, 2 or 3. Bin 1 is the goal: it blocks the meter completely in reverse.
- No die rectifies? Check the meter on the 1N4148 again, then try a sharpened 6B pencil point
  pressed on a die in place of its dot.
- Compare the centre {centre} with the edge {edge}. A difference means the plate heats unevenly.

## Results

- Did any die rectify?
- Fwd is red on T?
- Sort yield, final yield
- Centre or edge better?
- Bin limits to keep

{T3} marks recipe numbers and bin limits that the first wafer will settle. {T1} waits on the pencil
tests. Background, sources and hazards: docs/explorations/paper-semiconductors.md.
