# AI6K QSL Studio

A small Python project for generating precisely aligned four-up QSL card sheets.

## Cardstock

- US Letter: 8.5 x 11 inches, portrait
- Four cards: 3.5 x 5.5 inches, portrait
- Two columns by two rows
- No gutters
- Cards begin at the top-left paper edge
- Unused strip: 1.5 x 11 inches on the right

## Setup on Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Generate the calibration PDF:

```powershell
qsl-calibration
```

The PDF will be written to `output/AI6K_QSL_calibration.pdf`.

Print using:

- Letter paper
- Portrait orientation
- Actual Size / 100%
- Borderless printing OFF
- Fit, Shrink, or Scale to Page OFF
- Use the same tray and paper settings each time

The printed targets intentionally sit inside the card edges because the Epson
cannot print all the way to every physical paper edge. Measure each target
relative to its perforation and record the offset in `config/printer.yaml`.
