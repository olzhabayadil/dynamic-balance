# Local Setup

## Installed Tools

- Git
- Node.js / npm
- Docker Desktop
- Codex Desktop / Codex CLI bundle
- Claude Code via npm global package
- Python virtual environment in `.venv`

## Python Environment

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run project checks:

```powershell
.\scripts\check.ps1
```

Run the Streamlit UI:

```powershell
.\scripts\run_ui.ps1
```

## Claude Code

Claude Code is installed globally through npm.

If `claude` is not visible in a fresh terminal, use the full path:

```powershell
& "$env:APPDATA\npm\claude.cmd" --version
```

Or use the project wrapper:

```powershell
.\scripts\run_claude.ps1 --version
```

## Data Safety

Keep real data under:

- `data/raw/`
- `data/private/`
- `reports/private/`

These folders are ignored by Git.

Use `sample_data/` for synthetic datasets that AI agents can inspect freely.

## Docker Note

Docker Desktop is installed, but Docker Engine access may require starting Docker Desktop
or fixing Windows user permissions for the Docker engine.
