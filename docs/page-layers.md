# Page layers

Every circuit page is built from three layers, one source of truth each. [M7](../papercircuits/sheets/m7_output.py) and [L01](../papercircuits/sheets/l01_led_polarity.py) are the shortest worked examples: read both before making or changing a page.

| Layer | Where | Holds |
|---|---|---|
| Circuit | `CIRCUIT = Circuit(...)` at the top of the sheet module | Every part, with its real value and the nets its pins join |
| Placement | the sheet module's drawing functions, through `Placement` | Where each lane, part, loop and test point goes |
| Words | `<module>.md` beside the module | Every sentence on the page |

## Changing the code without changing a page

A change to how a page is built, rather than what it says or shows, must build to exactly the same PDF. That's how every page moved onto these layers. Check with:

```bash
uv run build.py && git diff --exit-code --stat out/
```

No output means the page is identical. To get there, keep every drawing call in the same order with the same numbers, and keep every string exactly as it was, including double spaces.

If a page can't be identical, stop and show the text difference (`pdftotext` before and after). Don't change wording to make conversion easier.

## Making or changing a page

1. **Circuit.**
   - List the parts: `R`, `C`, `CE` (electrolytic), `LED`, `D`, `Q`, `LDR`, `F` (fuse), `BAT`, `SW` (corner or tab switch), `PENCIL` (a pencil track and its wiper) and `WIRE` (a bare link).
   - Values are numbers: `R("R1", 220, "VSW", "N1")`.
   - Name nets after what they are: `V+`, `GND`, `MIX`, `OUT`, or `N1` for a node with no name.
   - An LED printed backwards on purpose is written backwards in the circuit.
2. **Placement.**
   - `lay = Placement(sh, CIRCUIT)`.
   - Then `lay.lane(net, pts)` for every lane, and `lay.ring()` on an M page.
   - Then `lay.resistor(ref, ...)`, `lay.led(...)` and the rest, with the same numbers as before.
   - Use `label="value"` where the page printed "R1 · 220 Ω", and `label=None` where it printed no label.
   - Draw everything that isn't a circuit part with `E.` as before: crossings, spines, decorations, measuring-only pencil tracks. Call `sh.allow` for switch pairs and crossings as before.
3. **Schematic.**
   - Keep it hand-placed.
   - Fetch each part with `lay.symbol(ref)` and use its `.ref` and `.text`.
   - Fetch each test point's label with `lay.probe("TP1")`.
4. **Words.**
   - Move every sentence into the `.md` file: title, subtitle, "You need", "Build it", "Play it", captions, workbook prompts (`- key: text` fields), drawing labels and the schematic note.
   - In "You need", name parts through the circuit, so counts and values can't drift: `{R1.count} resistors, {R1} ({R1.bands}) {P}`, or `{R1.refs} {R1} · {R4.refs} {R4}`.
   - Use the shared snippets in [`shared.md`](../papercircuits/sheets/shared.md) wherever a step matches one word for word.
   - Lane counts come from `{lanes}`, passed as `number(lay.laid)`.
   - The title and subtitle can use tags and standard values, such as `{T3}` or `{version}`.
   - Where a page's PDF title differs from its printed title, put it in a `## PDF title` section.
   - A section name may appear only once. A mistyped field, section or `{value}` stops the build and names the file and section.
5. **Check.**
   - Call `lay.check(listed=WORDS.refs("You need"))` just before `sh.save()`.
   - Take the PDF's title from the words: `Sheet(path, " ".join(WORDS.title.split()))`.
6. **Prove the check works.**
   - Plant two or three mistakes with [`tools/plant.py`](../tools/plant.py): a part moved off its lane, a wrong net in the circuit, a test point missing from the schematic.
   - Every one must be caught.

```bash
uv run tools/plant.py l01_led_polarity 'R("R1", 220,' 'R("R1", 4.7e3,'
```

## What the check enforces

- Each net has exactly one strip: one lane or one pencil track.
- Every lead lands on its own net's strip, and named pins (anode, cathode, plus, minus, E, B, C) land on their own net.
- Patch loops and test points stand on their own net.
- A pencil track's wiper lane runs alongside it, at least 3 mm away (so a smudge can't bridge them) and close enough for the wiper's strip to reach both.
- Every part and test point appears once in the schematic.
- Every bought part is in "You need".

## Pages that aren't circuits

The template and the test sheets (T0 to T3) are rows of test structures, not one circuit. They have the words layer only, with their sentences in a `.md` file.

- **Procedures:** `ts.section(WORDS, name, ts.steps)` in [`testsheet.py`](../papercircuits/testsheet.py) prints a procedure heading and its items.
- **Test rows:** a row's words are a field, such as `- J3: Overlap + solder · solder across it`, and `ts.row(words["J3"])` splits them into the name and the hint.
