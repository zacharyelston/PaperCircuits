# T4  Book interconnects

Print sheets 1 and 2 on the two sides of one card, flipping on the long edge. Make three.

## PDF title

T4 book interconnects

## Status

V2 bench test

## Sheet 1

- footer: sheet 1 of 4 (side A)

## Labels

- axis: ring axis

## Wraps

- title: 1  Edge wraps
- body: Lay each W lane on side A, run the tape over the edge and down side B to the test point
  behind. W1 and W2 cross the top edge, W3 and W4 the outer edge, W5 and W6 the bottom edge.
  W1, W3 and W5 are 5 mm tape; W2, W4 and W6 are 12 mm.

## Links

- edge_title: 2  Links at the edge and inboard
- axis_title: 4  Links on the ring axis
- E1: At the edge · solder bridge across the wrapped edges
- E2: At the edge · stranded wire, 30 mm service loop
- E3: At the edge · one ribbon conductor, 30 mm loop
- I1: 10 mm inboard · stranded wire, 30 mm loop
- I2: 10 mm inboard · one ribbon conductor, 30 mm loop
- X1: On the axis · stranded wire laid 15 mm along it
- X2: On the axis · one ribbon conductor laid along it
- X3: On the axis · wire under a stitched card patch
- X4: On the axis · solder bridge
- X5: Your version

## Contract

- title: 3  The spine contract
- hint: Proposed pins, 8 mm apart. Each passes to side B through a wire via.
- C1: GND
- C2: BUS A
- C3: V+
- C4: BUS B
- C5: GND

## About

Print three cards: pages 1, 2 and 3 of a test book. Side A, this side, takes each link from the
page before; side B sends it on to the page after.

With the book open, the back of one page lies beside the front of the next, so both ends of a
link can be probed at once. Sheet 3 says how to build and test the links.

## Sheet 2

- title: T4  Book interconnects: side B
- subtitle: This side prints on the back of sheet 1. Links leave from here for the next page.

## Sheet 3

- title: T4  Running the book interconnect tests
- subtitle: Print sheets 3 and 4 once on plain paper. Print sheets 1 and 2 double-sided on card,
  three times.
- footer: sheet 3 of 4

## You need

- Three cards printed double-sided (sheets 1 and 2), and a ring binder that fits them
- 5 mm and 12 mm copper tape, solder and a soldering iron
- Stranded hookup wire, about 28 AWG, and a strip of ribbon cable
- Thin card, clear tape, a needle and thread for strain relief
- A 100 Ω resistor (½ W or more), a 3 × AA holder and clip leads
- A multimeter with a 200 mV range

## 1 · Wraps

1. Lay W1 to W6 on side A of one card, run the tape over the edge and on down side B to the test
   point behind. Burnish the fold.
2. Measure each wrap from its side A test point to its side B test point, as in step 3.
3. Bend each wrapped edge back and forth ten times and measure again. Look for cracks.

## 2 · Build the test book

1. On all three cards, lay every link lane (E1 to X5) and the contract lanes (C1 to C5) on both
   sides. Keep all five contract lanes separate: do not join C1 to C5 at the contract block.
2. Make the contract block's wire vias: push a cut-off resistor leg through each via mark and
   solder it on both sides. Each via is an independent route between sides A and B.
3. Bind the cards in order, page 1 on top.
4. For every row, join the back of page 1 to the front of page 2, and the back of page 2 to the
   front of page 3, the way the row's label says. Keep each solder joint at least 5 mm from the
   ring axis, except X4's, which tests a joint on it. On the axis rows, lay the wire or ribbon
   along the axis between the two joints.
5. Join each of C1 to C5 to its matching pin on the next page with a five-conductor strip of
   ribbon laid along the axis. Do not bridge C1 and C5 in the contract footprint. Mark the C1
   edge with a stripe and keep that stripe on C1 at both ends; reversing the ribbon swaps BUS A
   and BUS B even though V+ and GND stay safe.

## 3 · Measuring a link

1. Clip the holder, the 100 Ω resistor and the link in a loop: holder +, resistor, the link's
   test point on the back of one page, the link, its test point on the front of the next page,
   holder −.
2. Measure the voltage across the resistor and divide by 100 Ω: that's the current, about 45 mA.
3. On the 200 mV range, measure from one test point to the other. 4.5 mV at 45 mA is 0.1 Ω.

## 4 · The spine contract chain

1. Temporarily join C1 and C5 with clip leads on page 1, outside the contract footprint. Clip
   the holder to page 1: red to C3 (V+), black to that temporary GND junction.
2. Temporarily join C1 and C5 on page 3. Clip the 100 Ω resistor across C3 and that temporary
   GND junction.
3. Measure C3 from one page to the next. Its drop divided by the total current must be 0.1 Ω or
   less.
4. Measure between the temporary GND junctions from one page to the next. The drop divided by
   total current must be 0.05 Ω or less. Do not calculate either GND conductor from total
   current; the current splits.
5. Remove the temporary GND joins. Test C1, C2, C4 and C5 one at a time in the separate loop
   from section 3; each must be 0.1 Ω or less. Confirm that the ribbon's striped edge is on C1
   at both ends before applying power.

## 5 · Flex cycles

1. One cycle: open the spread between pages 1 and 2 all the way, close it, then do the same for
   pages 2 and 3.
2. Measure every link after 10, 100, 500 and 1,000 cycles.
3. While turning the pages slowly, watch the meter across the load on page 3. Any jump is a
   flicker; note which link moved.
4. Check every joint with a magnifier for cracks, lifted tape and torn paper.

## 6 · Repair

1. Unclip the holder. Cut every link to page 2, take it out, bind a fresh page 2 and resolder.
2. Note how long it took, then measure page 2's links again.

## Pass or fail

- **Pass:** each individual link and contract conductor is 0.1 Ω or less, the temporarily
  paired GND conductors are 0.05 Ω or less, and the load stays steady while the pages turn.
- **Fail:** a crack, lifted tape, torn paper or any flicker.
- Links at the edge move about 24 mm each cycle. If they fail, the V2 standard will prohibit
  them.

## Sheet 4

- title: T4  Results
- subtitle: Readings in mV at the measured current. Divide by the current for ohms.
- footer: sheet 4 of 4

## Results

- wraps: Wraps, side A to side B
- new: New
- handled: Bent
- cracks: Cracks?
- chain: The spine contract chain
- current: Current, from the load: ________ mA
- first: 1 to 2
- second: 2 to 3
- gnd_1: C1  GND 1
- gnd_pair: C1 + C5  GND pair
- bus_a: C2  BUS A
- power: C3  V+
- bus_b: C4  BUS B
- gnd_2: C5  GND 2
- links_1: Links, page 1 to page 2
- links_2: Links, page 2 to page 3
- flicker: Flicker?

## Results for the standard

- Best link construction
- Pin-1 stripe stayed on C1 at every joint
- Closest safe distance from the axis
- Service loop needed
- Wrap tape: 5 mm or 12 mm
- Flex-life target met (cycles)
- Constructions to prohibit
