# T0  Contact tests

Which joints, part contacts and binder contacts stay reliable? Build on 160–200 gsm card.

## PDF title

T0 contact tests

## Labels

- notes: Notes

## Sheet 1

- footer: sheet 1 of 3

## Hole fixtures

- H1: Bare hole · tape only, no eyelet
- H2: Eyelet · clamps the 5 mm strip
- H3: Eyelet · on 12 mm tape
- H4: Eyelet · soldered to the strip

## Tape joint fixtures

- title: 1  Tape joints
- intro: Lay each lane from pad A to pad B as marked, then measure A to B in ohms and subtract the
  meter zero. Write OL for an open circuit. Sheet 2 explains Flexed and Day 7.
- zero: Meter zero
- built: Built on
- J1: Continuous · the reference
- J2: Overlap · cut, overlap 10 mm
- J3: Overlap + solder · solder across it
- J4: Folded corners · fold, don't cut
- J5: Cut corners · cut + overlap at each
- J6: Your tape · e.g. conductive glue

## Part joint fixtures

- title: 2  Part joints
- intro: Bridge each gap with a 10 Ω resistor, leads flat on the tape, attached as labelled.
  Measure A to B. Contact resistance is the reading minus R alone.
- alone: R alone
- alone_hint: one resistor, probes on its leads
- day0: Day 0
- flexed: Flexed
- day7: Day 7
- flicker: Flicker?
- M1: Flat leads · clear tape over
- M2: Flat leads · copper patch over
- M3: Spiral leads · copper patch over
- M4: Soldered
- M5: Your method

## Sheet 2

- title: T0  Running the contact tests
- subtitle: Print this sheet once on plain paper. Print sheet 1 on card three times and sheet 3 once.
- footer: sheet 2 of 3

## You need

- 5 mm copper tape, plus about 15 cm of 12 mm tape for H3
- Five 10 Ω resistors per sheet (brown-black-black)
- Plain brass eyelets for a 6 mm hole, and a setting tool. Not painted aluminium.
- A 2- or 4-hole punch with 80 mm pitch
- A ring binder, and four brass Chicago screws (binding posts) long enough for three sheets
- A multimeter with a 200 Ω range
- A soldering iron for J3, M4 and H4; clear tape; scissors for sheet 3

## Before you start

1. Print sheets 1 and 3 at 100 % on 160–200 gsm card. Check a footer bar measures 100 mm with a ruler.
2. Lay the four hole lanes (test 3) first, then punch through the crosshairs, through the tape.
3. Set eyelets in H2, H3 and H4. Leave H1 bare. Solder H4's eyelet to its strip.
4. Zero the meter: 200 Ω range, probes touching. Write the reading on sheet 1 and subtract it from
   every reading.

## 1 · Tape joints

1. Lay each lane as one piece of 5 mm tape, except at the marks: J means cut and overlap the two
   pieces by 10 mm.
2. J3: solder across the overlap. J4: turn each corner by folding along the printed crease. J5: cut at
   each corner and overlap.
3. Measure from pad A to pad B. Write OL if the meter shows an open circuit.
4. **Flexed:** bend the card gently over a table edge 10 times, rub each joint firmly with a thumb 5
   times, then measure again.
5. **Day 7:** leave the sheet in the binder for a week, then measure again.

## 2 · Part joints

1. Measure one resistor on its own and write it as R alone.
2. Bridge each station's gap with a resistor, leads flat on the tape. M1: clear tape over flat leads.
   M2: a copper tape patch over flat leads. M3: coil each lead into a flat spiral, then a copper patch.
   M4: solder each lead. M5: your own idea.
3. Measure A to B. Contact resistance is the reading minus R alone.
4. **Flicker:** press on the part while watching the meter. Write Y if the reading jumps.
5. Repeat after flexing and on day 7.

10 Ω is low on purpose: a contact of a few ohms shows up clearly against it.

## 3 · Binder contacts

1. Build the hole treatments on all three copies, as labelled on sheet 1.
2. Bind the three sheets on rings. On each sheet, measure from TP-H<i>n</i> to the bare metal of ring
   <i>n</i>. Write the worst of the three readings below.
3. **Turning:** keep the probes on and turn the other sheets back and forth 5 times. Write the highest
   reading, or OL.
4. Repeat with Chicago screws, finger-tight.

## Binder table columns

- H1: bare
- H2: eyelet
- H3: 12 mm
- H4: solder

## Binder table rows

- Rings, still
- Rings, turning
- Screws, still
- Screws, turning

## 4 · Switch contacts

Build, test and record the switches on sheet 3; its steps and pass rule are there.

## Pass or fail

- **Pass:** within 1 Ω of the reference (J1, R alone, or 0 Ω for test 3) and no flicker.
- **Fail:** OL, any flicker, or a reading that drifts by day 7.

Why 1 Ω: lesson circuits use resistors of 100 Ω and up, so 1 Ω changes the current by 1 % or less.
Flicker matters more than the exact value.

## Results for the standard

- Tape overlaps OK?
- Lead attachment
- Hole treatment
- Binding
- Switch gap
- Corner switch OK?

## Sheet 3

- title: T0  Switch contacts
- subtitle: Do fold switches close every time, and does the gap stay open? Build on 160–200 gsm card.
- footer: sheet 3 of 3

## Switch fixtures

- title: 4  Switch contacts
- intro: Each switch joins lane A to lane B while its flap is pressed. Measure A to B with the meter
  on its 200 Ω range.
- corner: S1 · corner switch
- corner_hint: fold the corner down to press
- TA: 2 mm gap, the standard
- TB: 3 mm gap
- TC: your version

## Switch table columns

- Open: OL?
- Light press: Ω
- Firm press: Ω
- Flicker?: Y / N
- After 20: Ω
- Day 7: Ω

## Switch table rows

- S1 corner
- TA 2 mm
- TB 3 mm
- TC yours

## How to test

1. Lay each switch's A and B lanes as separate pieces of tape. Keep the gap between them clear.
2. S1: stick a {flap_pad} mm piece of tape on the corner flap where shown. Tabs: cut the solid lines,
   crease the dotted hinges and stick a {flap_pad} mm piece on each flap.
3. **Open:** with nothing pressed, measure A to B. It must read OL; a number means the gap is bridged.
4. **Light and firm:** rest one finger on the flap and read the meter. Then press hard with a thumb.
5. **Flicker:** keep pressing and rock your finger. Write Y if the reading jumps or drops to OL.
6. **After 20:** press and release 20 times, then take a firm reading. **Day 7:** repeat a week later.

## Switch pass or fail

Pass or fail

- **Pass:** open reads OL, and pressed reads under 10 Ω with no flicker.
- **Fail:** any reading when open, OL or flicker when pressed, or a rise by day 7.

Why 10 Ω: lesson LEDs use 220 Ω, so 10 Ω changes their current by under 5 %. Flicker matters more:
it shows up as a flickering LED.

If TB passes as well as TA, standard v0.2 can widen switch gaps to 3 mm and drop the 2 mm exception.
Write the result on sheet 2.
