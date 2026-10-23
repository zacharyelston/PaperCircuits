# PaperCircuits

Printable A4 paper-circuit workbook pages. Circuits are built from copper tape and real through-hole parts, and pages bind into a shared power-and-signal backplane through the binder holes.

| File | What it is |
|---|---|
| [docs/page-standard.md](docs/page-standard.md) | The page standard every sheet follows (v0.1 draft) |
| [out/T0-contact-tests.pdf](out/T0-contact-tests.pdf) | Contact tests to run before fixing the standard |
| [out/template.pdf](out/template.pdf) | Lesson page template: zones, nets and drawing marks |
| [out/P1-power.pdf](out/P1-power.pdf) | Power page P1: 3 × AA, resettable fuse, feeds H2/H3 (draft; [teacher notes](docs/lessons/P1.md)) |
| [out/L01-led-polarity.pdf](out/L01-led-polarity.pdf) | Lesson L01: LEDs only work one way (draft; [teacher notes](docs/lessons/L01.md)) |
| [out/L02-and-or.pdf](out/L02-and-or.pdf) | Lesson L02: two switches, two ways, AND and OR (draft; [teacher notes](docs/lessons/L02.md)) |

## Build

```bash
uv run build.py
```

This writes the PDFs to `out/` and PNG previews to `docs/img/`. Previews need `pdftoppm` from poppler.

## Code

- `papercircuits/standard.py`: every number from the standard. It must agree with the spec.
- `papercircuits/draw.py`: an A4 canvas in standard coordinates (mm, origin top-left, y down).
- `papercircuits/elements.py`: standard elements such as the spine, tape lanes, test points and part footprints.
- `papercircuits/schematic.py`: circuit-diagram symbols for the schematic panel.
- `papercircuits/provisional.py`: the `[T0]` and `[P]` tags for choices that wait on an open decision.
- `papercircuits/sheets/`: one module per sheet. Add new sheets to `SHEETS` in `build.py`.

## Printing

Print at 100 % ("actual size"), never "fit to page". Every page has a 100 mm bar in the footer; check it with a ruler.
