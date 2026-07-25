# Milestone 3: Template-driven front design

This milestone replaces the hard-coded front proof with a YAML template.

## Files added or replaced

- `qslstudio/template.py`
- `qslstudio/front.py`
- `templates/front.yaml`
- `tests/test_template.py`

Copy these into the repository, allowing Windows to replace the existing
`qslstudio/front.py`.

The existing command remains:

```powershell
qsl-front
```

It now generates:

```text
output\AI6K_QSL_front.pdf
```

The front layout can now be changed entirely in:

```text
templates\front.yaml
```

No Python editing is required for normal typography and position changes.

## Run

```powershell
python -m pip install -e .
pytest
qsl-front
```

## Current design

The template contains:

- Large AI6K callsign
- Thin divider
- Name
- Prosper, Texas
- Minimal center placeholder for a future Texas outline
- "73 from North Texas"

The small center rectangle is intentionally temporary. It lets us confirm the
spacing before replacing it with a vector Texas outline.
