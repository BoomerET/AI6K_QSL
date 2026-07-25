# Milestone 5: QSO model and card back

This milestone introduces real application data models:

- `StationProfile`
- `QSO`

It also adds a template-driven back design populated with four sample contacts.

## Install

Copy the files into the repository.

Add this command under `[project.scripts]` in `pyproject.toml`:

```toml
qsl-back = "qslstudio.back:main"
```

Refresh the editable installation:

```powershell
python -m pip install -e .
pytest
qsl-back
```

The generated proof is:

```text
output\AI6K_QSL_back_proof.pdf
```

Each of the four cards contains a different sample QSO. This verifies that one
sheet can contain independently populated cards.

## Why this matters

The renderer and templates no longer need to know where contact data comes
from. Today it comes from demo Python objects. Later it can come from:

- Wavelog API responses
- ADIF files
- CSV imports
- Manual entry
