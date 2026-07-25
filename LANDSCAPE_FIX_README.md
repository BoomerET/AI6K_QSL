# Landscape orientation fix

The perforated sheet contains four physical panels measuring 3.5 x 5.5 inches,
but each finished QSL card should be viewed as a standard landscape
5.5 x 3.5-inch card.

This patch:

- Changes the logical card dimensions to 5.5 x 3.5 inches
- Rotates each card design into its 3.5 x 5.5-inch perforated panel
- Updates the front template for landscape composition
- Keeps the physical sheet geometry unchanged

Copy these files into the repository and allow them to replace the existing
versions.

Then run:

```powershell
python -m pip install -e .
pytest
qsl-front
```

The generated sheet remains portrait Letter paper, but each individual card
will read correctly in landscape orientation after separation.
