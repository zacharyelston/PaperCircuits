# T6  Two-sided synth buses

Use BUS A for pitch control and BUS B for audio: signals, not power returns.

## PDF title

T6 two-sided synth buses

## Status

V2 synth test

## Side A

- title: BUS A · pencil pitch controller
- body: Adapted from M3. V+ feeds a 13 kΩ resistor and pencil ribbon. The movable wiper puts the selected resistance onto BUS A for M1's PITCH input.
- footer: sheet 1 of 4 (side A)

## Side B

- page_title: T6  Synth bus: side B
- subtitle: BUS B receives audio from M1; V+ and GND arrive through their spine wraps.
- title: BUS B · pencil tone filter
- body: Adapted from M6. BUS B is the audio input. The wiper selects pencil resistance before OUT, while C1 sends high-frequency buzz to GND. OUT still goes through M7 before an amp.
- footer: sheet 2 of 4 (side B)

## Sheet 3

- title: T6  Build and test the synth buses
- subtitle: Print sheets 1 and 2 double-sided on card, flipping on the long edge. Print sheets 3 and 4 once.
- footer: sheet 3 of 4

## You need

- One double-sided card, a three-hole punch and a three-ring binder
- 5 mm copper tape for V+ and the buses; 12 mm copper tape for GND
- R1: 13 kΩ; C1: 47 nF ceramic
- A soft 6B pencil, an eraser, clear tape and card for two wipers
- Solder, clip leads and a multimeter
- Built M1 oscillator and M7 output pages; a powered speaker or amp with a line/AUX input

## 1 · Print and lay power

1. Check the 100 mm scale bars and side registration. Punch the three mechanical holes.
2. Lay V+ and GND around the spine edge at their fixed rail heights, following the solid arrows.
3. Confirm V+ and GND are continuous face-to-face and read OL between them.

## 2 · Build side A

1. Lay BUS A only on side A. Shade the ribbon hard with 6B pencil until it shines.
2. Fit R1 from V+ to the ribbon's high end.
3. Cut out the BUS A wiper and tape copper underneath. It must bridge BUS A to the ribbon when pressed.
4. Keep BUS A isolated from V+, GND and every side-B conductor.

## 3 · Build side B

1. Lay BUS B only on side B. Shade the tone track hard with 6B pencil.
2. Join the track's bright end to OUT with W1. Fit C1 between OUT and GND.
3. Cut out the BUS B wiper and tape copper underneath. It must bridge BUS B to the track when pressed.
4. Keep BUS B isolated from V+, GND and every side-A conductor.

## 4 · Patch the synth

1. Power M1, M7 and this card from the same fused 4.5 V supply and common GND.
2. Patch BUS A to M1 PITCH. Press the side-A wiper on the ribbon and BUS A.
3. Patch M1 OUT to BUS B. Patch this card's OUT to M7 IN1.
4. Connect M7 only to a powered speaker's or amp's line/AUX input with its volume low. Never use headphones or a bare speaker.

## 5 · Test the buses

1. Slide the side-A wiper from high to low. The note must glide down without BUS A powering anything.
2. Hold the pitch steady and slide the side-B wiper from bright to soft. The buzz must soften without BUS B carrying supply current.
3. Remove BUS A: M1 must stop. Restore it, then remove BUS B: the amp must go quiet while M1's LED still shows oscillation.

## 6 · Flex and inspect

1. Flex both power spine wraps through 100 cycles, then repeat both signal tests while opening and closing the binder.
2. Record crackle, dropouts, changing pitch or lifted pencil/tape contacts. Repeat at 1,000 cycles if the 100-cycle test passes.

## Pass or fail

- **Pass:** BUS A controls pitch, BUS B carries audio, removing either bus breaks only its stated signal path, and flexing causes no dropout.
- **Fail:** either bus acts as power or return, appears across the wrong face, shorts a rail, or requires a through-page via.

## Results

- title: T6  Synth bus results
- subtitle: Record power-wrap resistance and whether each signal bus keeps its one job.
- footer: sheet 4 of 4
- continuity: Power-wrap continuity
- continuity_note: Measure with power disconnected; V+ to GND must remain OL.
- new: New
- cycles: After flex
- signals: Functional signal tests

## Bus decision

- BUS A existed only on side A
- BUS A controlled M1 pitch
- BUS B existed only on side B
- BUS B carried M1 audio
- Removing BUS A stopped M1
- Removing BUS B muted the output
- No bus carried load current
- No page via was required

## Notes

- Pitch range and tone change
- Crackle, dropout or flex damage
- Builder / date
