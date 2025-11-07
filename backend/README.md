## Sports Events Backend

FastAPI skeleton for the Sports Events platform.

---

## Requirements

- Python 3.12+
- `pip`
- (Recommended) a virtual environment tool such as `venv` or `uv`

---

## Installation

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e backend/.[dev]
```

Dependencies are defined in `backend/pyproject.toml`.

---

## Running the API locally

```bash
uvicorn app.main:app --reload --app-dir backend/src --host 0.0.0.0 --port 8000
```

## Add configuration values to `backend/.env` (see `.env.dist` for inspiration)

## Tests & Coverage

Run the test suite:

```bash
pytest backend/tests
```

Collect coverage (configuration lives in `backend/pyproject.toml`):

```bash
coverage run -m pytest backend/tests
coverage report
```

---

## Linting & Formatting

All style tools share their configuration via `backend/pyproject.toml`.

```bash
ruff check backend/src backend/tests         # static analysis
black backend/src backend/tests              # code formatter
isort backend/src backend/tests              # import sorter
```

Apply Ruff’s auto-fixes if desired:

```bash
ruff check backend/src backend/tests --fix
```
