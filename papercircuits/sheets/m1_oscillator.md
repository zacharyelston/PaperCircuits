# M1  Oscillator

Two transistors switch each other on and off: that's a tone.

## You need

- {Q1.refs}: {Q1} transistors
- {C1.refs}: {C1} capacitors, no polarity
- {R1.refs} {R1} · {R3.refs} {R3} · {R4.refs} {R4}
- {LED1.refs}: {LED1}
- Bare wire for {loops} patch loops; 22 kΩ to test
- Copper tape, solder, 2-core cable

## Caption

Patch PITCH to a controller such as M2's keyboard, and OUT to an IN on M7.

## Build it

1. Lay the power ring, then the {lanes} lanes inside it, one piece of tape each. Fold at the creases.
2. {crossing_step}
3. Place R1 to R4, C1 and C2 across their gaps, either way round. Place LED1 as printed: long leg
   on the +.
4. Lay Q1 and Q2 flat face up and bend each leg to its letter: E, B and C.
5. {lead_step}
6. Solder a patch loop upright on each loop mark: V+, PITCH and OUT. {T0}
7. {edge_join}

## Play it

- To test, clip a 22 kΩ resistor between the V+ and PITCH loops: M7 should play a steady note, and
  LED1 glows.
- Then patch PITCH to M2's stylus. More resistance on PITCH gives a lower note.

## Schematic note

C1 and C2 ({C1}) flip Q1 and Q2 in turn.
