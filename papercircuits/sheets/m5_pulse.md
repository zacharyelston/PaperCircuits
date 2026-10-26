# M5  Pulse

A slow oscillator blinks an LED and chops the note into a beat.

## You need

- {Q1.refs}: {Q1} transistors
- {C1.refs}: {C1} electrolytic, 16 V or more
- {R1.refs} {R1} · {R2.refs} {R2} · {R3.refs} {R3}
- {R4.refs} {R4} · {R5.refs} {R5} · {LED1.refs}: {LED1}
- Bare wire for {loops} patch loops
- Copper tape, solder, 2-core cable

## Caption

Patch one GATE to M1's PITCH and the controller's lead to the other. LED1 lights for each note.

## Build it

1. Lay the power ring, then the {lanes} lanes inside it, one piece of tape each. Fold at the creases.
2. {crossing_step}
3. Place R1 to R5 either way round, and LED1 long leg on the +. C1 and C2 go + where printed:
   backwards, they can heat up and fail.
4. Lay Q1 to Q3 flat face up and bend each leg to its letter: E, B and C.
5. {lead_step}
6. Solder a patch loop upright on each GATE loop mark. {T0}
7. {edge_join}

## Play it

- Power up: LED1 should blink about twice a second before anything is patched.
- Patch one GATE loop to M1's PITCH, and clip the controller's lead (M2's stylus, M3 or M4) to the
  other.
- For a slower beat, use 22 µF for C1 and C2. Swap R3 and R4 for short notes and long rests.

## Schematic note

Q3 holds GATE at GND in the rests.
