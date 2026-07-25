# Milestone 2: Reusable card layout engine

This update adds:

- Card-relative coordinates
- Reusable text, line, and rectangle elements
- A four-card `Sheet` renderer
- A first minimalist AI6K front proof
- A basic coordinate test

## Copy into the repository

Copy the contents of this package into the root of the existing repository.
Allow Windows to merge the `qslstudio` folder.

Then edit `pyproject.toml` and add the new command under `[project.scripts]`:

```toml
qsl-front = "qslstudio.front:main"
```

Also add pytest to the project dependencies or install it separately:

```powershell
python -m pip install pytest
```

Because the project is installed in editable mode, the new modules should
be immediately available. If the command is not found, rerun:

```powershell
python -m pip install -e .
```

Generate the front proof:

```powershell
qsl-front
```

The file will be written to:

```text
output\AI6K_QSL_front_proof.pdf
```

Run the test:

```powershell
pytest
```
