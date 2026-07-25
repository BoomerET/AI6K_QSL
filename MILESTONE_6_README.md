# Milestone 6: Reusable template components

This milestone adds two higher-level YAML elements:

- `qso_table`
- `station_signature`

Each component expands into the same low-level text and line elements already
supported by the renderer. The PDF drawing engine remains unchanged.

## Install

Copy the files into the repository, replacing the existing template loader and
back template.

Then run:

```powershell
pytest
qsl-back
```

## New back-template syntax

```yaml
- type: qso_table
  x_in: 0.35
  y_in: 1.12
  width_in: 4.80

- type: station_signature
  x_in: 2.65
  y_in: 2.70
  width_in: 2.50
  align: right
```

## Architecture

```text
YAML component
      |
      v
Component builder
      |
      v
TextElement / LineElement
      |
      v
Existing PDF renderer
```

This avoids teaching the sheet renderer about QSL-specific concepts. It only
continues to draw ordinary elements.
