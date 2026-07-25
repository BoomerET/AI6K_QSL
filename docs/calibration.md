# Epson ET-3760 calibration procedure

1. Generate the PDF with `qsl-calibration`.
2. First print it on ordinary Letter paper.
3. Use **Actual Size / 100%**.
4. Turn **Borderless**, **Fit**, **Shrink**, and automatic scaling off.
5. Compare the ordinary-paper print with a blank perforated sheet by holding
   them together against a bright light.
6. When the geometry looks sensible, print one perforated sheet.
7. Measure the target positions relative to the perforations.

## Offset convention

`x_offset_in`:

- Positive moves printed content right.
- Negative moves printed content left.

`y_offset_in`:

- Positive moves printed content down.
- Negative moves printed content up.

Only change scale if the one-inch ruler does not physically measure one inch.
Most alignment problems should require offsets only.
