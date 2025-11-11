# 🏆 Sports Events Platform

A full-stack **Sports Events Management** project built with:

- ⚙️ **Backend:** FastAPI + PostgreSQL + SQLAlchemy (async)
- 🖥️ **Frontend:** React + Vite + TypeScript

This setup demonstrates clean project structure, modern development tooling, and type-safe integration between backend and frontend through an OpenAPI-generated client.

---

## 📂 Project Structure

```
.
├── .dev/                   # Local Docker setup (Postgres + pgAdmin)
├── backend/                # FastAPI app, models, migrations, and tests
├── frontend/               # React + Vite + TypeScript UI
├── docs/                   # ER diagram and domain model docs
├── .gitignore
├── .pre-commit-config.yaml # Shared lint/format/test hooks
├── AI_Reflection.md        # AI collaboration and usage notes
└── README.md               # This file

```

---

## 🚀 Getting Started

1. **Set up and run the backend**
   Follow instructions in [`backend/README.md`](backend/README.md)
   → Includes environment setup, database configuration, migrations, and testing.

2. **Set up and run the frontend**
   Follow instructions in [`frontend/README.md`](frontend/README.md)
   → Includes Vite dev server, environment variables, and OpenAPI client generation.

Once both are running:

- **Backend API:** [http://localhost:8000/api/v1](http://localhost:8000/api/v1)
- **Frontend UI:** [http://localhost:5173](http://localhost:5173)

The frontend automatically connects to the backend defined by `VITE_API_BASE_URL`.

---

## 💡 Notes & Assumptions

- Designed for **local development**; Docker is used only for the database.
- Backend and frontend can be deployed independently if desired.
- Type safety is shared via generated OpenAPI schema.
