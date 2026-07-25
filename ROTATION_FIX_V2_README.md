# Rotation fix v2

The previous canvas transform combined rotation with a negative scale. That
reflected the coordinate system, which mirrored the text, and its translation
also moved part of the artwork outside the page.

This replacement does not transform the whole canvas. It explicitly maps every
landscape-card point into the correct physical perforated panel and rotates
text only.

Copy `qslstudio/sheet.py` into the repository, replacing the current version,
and add `tests/test_rotation.py`.

Then run:

```powershell
pytest
qsl-front
```

Do not print directly on cardstock first. Open the PDF and verify:

- Four cards are visible
- All text reads normally
- Each card is sideways on the portrait sheet
- Rotating the page counterclockwise makes each card read as landscape
