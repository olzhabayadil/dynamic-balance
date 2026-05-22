# Dynamic Balance

ALM dynamic balance modeling toolkit.

## Quick Start

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Project Layout

- `dbal/`: core Python package.
- `app/ui/`: Streamlit UI.
- `specs/`: methodology and acceptance criteria.
- `tests/`: automated tests.
- `sample_data/`: synthetic data safe for AI agents.
- `data/raw/`: private raw data, ignored by Git.
- `reports/`: generated reports.

## Data Safety

Keep real bank data under `data/raw/` or `data/private/`. These folders are ignored by Git.
Use `sample_data/` for synthetic examples and AI-assisted development.

## Streamlit Community Cloud

Deploy from GitHub with:

- branch: `main`;
- main file path: `app/ui/Home.py`;
- dependencies: `requirements.txt`.

See `docs/deploy_streamlit.md`.
