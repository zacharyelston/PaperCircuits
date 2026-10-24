# Test log

Bench results that feed the [page standard](page-standard.md). Newest first.

Write down readings in ohms where you can. "It works" with no number is a good start, but the standard needs numbers, especially after flexing and on day 7.

## Template

```markdown
### YYYY-MM-DD · Short title

- **Test:** which sheet and station (e.g. T1 O4), or "informal"
- **Setup:** tape, pencil grade, paper, overlap length, how hard you rubbed and burnished
- **Readings:** day 0 / flexed / day 7, in Ω (or kΩ on pencil)
- **Result:** what happened
- **Changes:** which tags or rules this affects; "none yet" until confirmed
- **Next:** what to try next
```

## Entries

### 2026-10-24 · Soldered resistor on copper tape

- **Test:** informal, built on a printed template page (L00), using the resistor footprint in its legend. This is the same idea as T0's M4 station.
- **Setup:**
  - a blue metal-film resistor, nominally 100 Ω, laid across the 10 mm gap between two lanes
  - each lead soldered to the copper tape under it
  - the page's other legend marks also laid in tape: lane, folded corner, joint, crossing, net strips, and the corner switch's stubs and flap pad
- **Paper:** not recorded. The photo suggests plain printer paper, because the sheet underneath shows through.
- **Readings:** 99.2 Ω on the 200 Ω range, measured through the lanes and solder joints. The meter zero and the resistor on its own weren't recorded.
- **Result:** soldering works. The reading is the resistor's own value, so the solder joints add at most about 1 Ω, which is negligible. The photo shows no visible scorching or lifted tape.
- **Changes:** none yet. This supports solder as a reliable fallback for **[T0]** lead attachment (M4) and joints (J3).
- **Next:**
  - To size the joints exactly, measure the resistor on its own (probes on its legs) and subtract that from the lane-to-lane reading.
  - Repeat after flexing, and on day 7.
  - Record the paper.

### 2026-10-24 · Graphite between tape layers

- **Test:** informal, before T1 was printed. It tested the T1 idea: rub pencil graphite into copper tape's non-conducting glue, so a joint conducts through it.
- **Setup:** two configurations:
  1. **Sticky to sticky, on a fold:** two glue faces together, with graphite between them. It's now T1 row O6.
  2. **Sticky onto bare copper:** a glue face pressed onto bare copper tape, with graphite between them. It matches T1 rows O3 and O4.
- **Readings:** not recorded.
- **Result:** both conducted.
- **Not recorded yet:**
  - resistance values
  - pencil grade
  - how hard the glue was rubbed and the joint burnished
  - overlap length
  - paper
  - behaviour after flexing and on day 7
- **Changes:** none yet. This is the first evidence for **[T1]** (pencil-treated overlaps). If T1 confirms it with readings, the standard's §4 could allow pencil-treated overlaps where it now asks for solder.
- **Next:**
  - soldering: T0's J3 (soldered overlap), M4 (soldered leads) and H4 (soldered eyelet)
  - T1 with readings, on the card the workbook will use
