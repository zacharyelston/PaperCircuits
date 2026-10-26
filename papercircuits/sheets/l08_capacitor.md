# L08  Store some charge

A capacitor keeps an LED lit after the power goes. For how long?

## You need

- {LED1.count} red LEDs, 5 mm
- {R1.refs}: {R1} ({R1.bands}) {P}
- {R2.refs}: {R2} ({R2.bands}) {P}
- {C1.refs}: {C1} electrolytic capacitor, 10 V or more
- 5 mm copper tape; P1 in the binder; a multimeter

## Build it

1. {lanes_step}
2. {flap_step}
3. {hole_step}
4. Place R1, R2 and R3 across their gaps, either way round.
5. Place C1 **exactly as printed**: the striped leg (−) down to GND, the other leg up to the lane.
   Backwards, a capacitor can heat up and fail.
6. Place LED1 and LED2 as printed: long leg on the +.
7. {hold_step}
8. Bind with P1. Hold the corner down, then let go and watch both LEDs. If C1 ever feels warm,
   switch BT1 off and check it.

## Labels

- switch: fold the corner down
- with: LED1 · with C1
- without: LED2 · no capacitor

## Predict

- prompt: When you let go of the corner, what will each LED do?
- choices: goes out at once  /  fades
- question: Circle one for each. Why do you think so?

## Measure

- prompt: Count the seconds each LED glows after you let go.
- table: Press
- tap: A quick tap
- hold_1: Hold 1 s
- hold_5: Hold 5 s
- probe: Black probe on TP4:
- when: TP2 when LED1
- dark: goes dark

## Explain

- prompt: Where does LED1's light come from after you let go?
- question: How could you make it glow for longer?

## Schematic note

C1 charges while S1 is held down.
