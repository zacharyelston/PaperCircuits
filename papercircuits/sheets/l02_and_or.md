# L02  Two switches, two ways

Wire the same two switches in a row, then side by side, and compare.

## You need

- {LED1.count} red LEDs, 5 mm
- {R1.count} resistors, {R1} ({R1.bands}) {P}
- 5 mm copper tape and scissors
- Power page P1 in the binder
- A multimeter for Test

## Build it

1. Lay the {lanes} lanes, one piece of tape each. Where two lanes run close, keep the {pad_gap} mm
   gap clear. {T0}
2. Cut each flap along its solid line and crease it along the dotted hinge.
3. Stick a {flap_pad} mm piece of tape on each flap where shown. Folded down, it must cross both
   lanes. {T0}
4. {hole_step}
5. Place R1 and R2 either way round, and LED1 and LED2 as printed: long leg on the +.
6. {hold_step}
7. Bind this page with P1 and switch BT1 on. Press the flaps down to test.

## Tables

- top: Top
- bottom: Bottom

## Top rows

- A1 only
- B1 only
- A1 and B1

## Bottom rows

- A2 only
- B2 only
- A2 and B2

## Predict

- prompt: Will the LED light? Write Y or N.

## Test

- prompt: Press the flaps. Black probe on TP3.

## Explain

- prompt: One circuit is called AND, the other OR.
- question: Which is which? Which one is like a door with two locks?

## Schematic note

V+ and GND come from P1.
