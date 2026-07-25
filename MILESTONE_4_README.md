# Milestone 4: SVG and PNG image support

This milestone adds a reusable `image` element to card templates.

Supported formats:

- SVG
- PNG
- JPG/JPEG

It also replaces the temporary NORTH TEXAS rectangle with a simple Texas
outline stored at:

```text
assets\texas-outline.svg
```

## Install

Copy the files into the repository and replace the existing versions.

Add this dependency to `pyproject.toml`:

```toml
"svglib>=1.5",
```

Then refresh the editable installation:

```powershell
python -m pip install -e .
pytest
qsl-front
```

The card template now uses:

```yaml
- type: image
  file: assets/texas-outline.svg
  x_in: 2.22
  y_in: 1.88
  width_in: 1.06
  height_in: 0.82
  preserve_aspect_ratio: true
```

The image path is relative to the repository root.
