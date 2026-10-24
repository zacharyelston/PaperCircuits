# Paper synth — group project notes

Pages:
- [M1 Oscillator](../../out/M1-oscillator.pdf)
- [M2 Keyboard](../../out/M2-keyboard.pdf)
- [M7 Output](../../out/M7-output.pdf)

Status: draft, not yet built. Needs [P1](../lessons/P1.md) for power.

## The idea

Each person builds one module page. The pages lie side by side on a table, power runs along the row from page to page, and clip leads patch the signals between them. M1 makes the tone, M2 plays it, and M7 sends it to a real amp or powered speaker. Nothing on the paper drives a speaker itself.

This is the first table-top project in the [page standard](../page-standard.md) (§10). Pages to add later: M3 pencil ribbon, M4 light pitch, M5 pulse and M6 tone.

## Setting up the table

1. **Lay the pages in a row,** left to right: P1, M2, M1, M7.
2. **Join the power.**
   - P1 to M2: clip leads from P1's V+ (H2) and GND (H3) strips to M2's left edge connector.
   - M2 to M1, and M1 to M7: solder a short 2-core cable from each page's right connector to the next page's left one, or use red and black clip leads.
3. **Patch.**
   - Clip one end of a lead to M1's PITCH loop. Its free clip is the stylus.
   - Patch M1's OUT to M7's IN1.
   - Clip M7's OUT to the 3.5 mm plug's tip and ring, and M7's GND to its sleeve.
4. **Plug in.** Turn the amp right down, plug into its line or AUX input, switch P1's BT1 on, touch a key, and bring the volume up slowly.

## M1 · How the oscillator works

- **Taking turns:** Q1 and Q2 take turns being on. When one switches on, its collector drops, and through C1 or C2 that pulls the other's base below 0 V. The other transistor stays off until its base resistor recharges the capacitor.
- **The timing:** each half of the cycle lasts about 0.693 × R × C:

  > f ≈ 1 / (0.693 × 100 nF × (10 kΩ + 4.7 kΩ + R_pitch))

  - Q1's half is set by R3, 10 kΩ.
  - Q2's half is set by R4 (4.7 kΩ) plus whatever the controller puts between V+ and PITCH.
- **Range:** about 980 Hz with R_pitch at zero, down to about 125 Hz at 100 kΩ. Above about 100 kΩ, Q2 may not switch on fully, and the note fades out.
- **No controller, no sound:** with nothing patched to PITCH, Q2 never switches on, so the oscillator is silent. That's why touching a key starts the note.
- **LED1** sits in Q1's collector path and glows while M1 is oscillating, a quick check that it works before involving the amp.
- **One crossing:** the page needs one insulated crossing. Both power rails come from outside the loop of parts, so one lane has to cross another. The standard allows crossings (§4), and the build's clearance check knows about this one.

## M2 · Keyboard values and tuning

The ladder runs from V+ through R1 to high C, then key by key to low C. Each key's resistance from V+ sets its note through M1's formula.

| Key | Target | From V+ | Resistor to its right | On paper |
|---|---|---|---|---|
| C5 | 523 Hz | 13.0 kΩ | R1 13 kΩ (to V+) | 521 Hz |
| B4 | 494 Hz | 14.6 kΩ | R2 1.6 kΩ | 493 Hz |
| A4 | 440 Hz | 18.2 kΩ | R3 3.6 kΩ | 439 Hz |
| G4 | 392 Hz | 22.1 kΩ | R4 3.9 kΩ | 392 Hz |
| F4 | 349 Hz | 26.4 kΩ | R5 4.3 kΩ | 351 Hz |
| E4 | 330 Hz | 28.8 kΩ | R6 2.4 kΩ | 332 Hz |
| D4 | 294 Hz | 33.9 kΩ | R7 5.1 kΩ | 297 Hz |
| C4 | 262 Hz | 40.1 kΩ | R8 6.2 kΩ | 263 Hz |

**Tuning:**
- **On paper versus on the bench:** "on paper" is the formula's answer. Real resistors (±5 %), M1's capacitors (often ±10 %) and the transistors shift every note, so expect the whole scale to sit a little sharp or flat.
- **Shifting the whole octave:** change R1. A bigger R1 lowers every note.
- **Fixing one note:** swap the resistor to its right for the next value up or down. A tuner app on a phone shows the frequency.
- **If you only have E12 values:** use R1 12 kΩ, then 1.5k, 3.3k, 3.9k, 4.7k, 2.2k, 5.6k and 5.6k. They're a little further off, so tune by ear.

## M7 · Output levels

- **Level:** a 0–4.5 V square wave through R1 (22 kΩ) into R4 (4.7 kΩ) arrives at OUT as about 0.8 V peak to peak, close to consumer line level.
- **Blocking DC:** C1 (1 µF) blocks the battery's DC. With R4 as its load, it passes everything above about 34 Hz.
- **Mixing:** each input has its own 22 kΩ resistor, so two oscillators on IN1 and IN2 add without fighting.

## Safety

- **Inputs:** only a powered speaker's or an amp's line or AUX input. M7 can't drive a speaker on its own, and isn't meant to.
- **Volume:** turn the amp down before plugging in, then bring it up slowly. A square wave is harsh, and loud square waves hurt ears.
- **Never** headphones, and never a bare speaker on any page.
- **Patch leads:** never patch an OUT straight to V+ or GND. P1's fuse protects the batteries, but the transistor may not survive.

## Common faults

| Symptom | Likely cause |
|---|---|
| Nothing, and LED1 dark | M1 has no power: check P1's switch and the edge cables. Or nothing is on PITCH, which is silent by design. |
| LED1 glows but no sound | M7 not patched, the plug wired wrong, or the amp on the wrong input or turned down |
| Every key plays the same note | The stylus is touching the ladder's resistor leads rather than a key's lane; touch lower down the key |
| Crackles as you play | A loose clip or a dry contact: press the stylus firmly, check the patch loops |
| One key is silent | A ladder resistor isn't touching its lane, so every key to its left goes quiet too |
| Hum when plugged in | The amp's mains earth. Try a battery-powered speaker. |

## Provisional

- **[T0] Lead attachment and patch loops without solder:** the pages say to solder. A copper tape patch is the fallback T0 will judge.
- **Not built yet:** the values above are calculated, not measured. Log real frequencies in the [test log](../test-log.md).
- **Transistors:** M1 is the first page with transistors. It works best after a transistor-switch lesson, which is planned for chapter 3 but not drafted.
