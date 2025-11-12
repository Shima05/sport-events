# 🖥️ Sports Events Frontend (Vite + React)

A modern **React + TypeScript** frontend built with **Vite**.
This UI provides a clean interface for browsing and creating sports events, including filters, pagination, and a modal-based create flow.
All API calls use **OpenAPI-generated TypeScript clients**, ensuring the frontend stays in sync with the FastAPI backend (`http://localhost:8000/api/v1`).

---

## 🧭 Overview

This frontend is designed to complement the FastAPI backend from the Sports Events project.
It focuses on:

- Clean developer experience with **Vite** and **TypeScript**.
- Consistent data typing with backend via **OpenAPI generation**.
- Simple, declarative **hooks-based data fetching** (`useEvents`, `useSports`, `useTeams`).
- Modular structure that’s easy to extend for future features (e.g., authentication, scheduling, analytics).

---

## ⚙️ Requirements

- **Node.js 20+**
- A **running backend** at `http://localhost:8000`
  (required to fetch live data and regenerate the OpenAPI client)

---

## 🚀 Setup & Run

```bash
cd frontend
npm install
npm run dev
```

Then open [http://localhost:5173](http://localhost:5173) in your browser.
Make sure your backend is running and available at the URL defined by `VITE_API_BASE_URL`.

> **CI**: `.github/workflows/frontend.yml` installs dependencies, runs `npm run lint`, and executes `npm run test` on every push/PR touching frontend files.

---

## ⚡ Environment Variables

Create a `.env` file (or export values in your shell):

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

If not set, this default URL is used.

---

## 🧰 Available Scripts

| Command                | Description                                              |
| ---------------------- | -------------------------------------------------------- |
| `npm run dev`          | Start Vite dev server with hot reloading                 |
| `npm run build`        | Type check and build for production                      |
| `npm run preview`      | Serve and preview the production build locally           |
| `npm run lint`         | Run ESLint with Prettier formatting rules                |
| `npm run format`       | Auto-format code using Prettier                          |
| `npm run test`         | Run Vitest in CI mode (with jsdom + Testing Library)     |
| `npm run test:watch`   | Run Vitest in watch mode                                 |
| `npm run generate:api` | Re-generate the typed OpenAPI client from backend schema |

---

## 🔁 Regenerating the OpenAPI Client

1. Make sure the **FastAPI backend** is running (`/backend` directory).
2. Download the latest OpenAPI schema:

   ```bash
   curl http://localhost:8000/openapi.json -o backend/openapi.json
   ```

3. Generate the TypeScript client:

   ```bash
   cd frontend
   npm run generate:api
   ```

The generated file is saved at:
`src/api/generated-schema.ts`

---

## 💡 Key Decisions & Assumptions

- **Typed networking:**
  All API calls are generated from the backend’s OpenAPI schema, ensuring strong typing and consistency between backend and frontend.

- **Modal-based create flow:**
  The “Create Event” flow is handled inside a modal. This keeps the main list view focused and avoids unnecessary page navigation.

- **Hooks per resource:**
  Each resource (`events`, `sports`, `teams`) has its own hook (`useEvents`, `useSports`, etc.) for simple and declarative data fetching.
  Currently, there’s no global state manager; **React Query** or similar could be added later for caching or mutations.

- **Tooling parity:**
  ESLint, Prettier, Vitest, and Vite configs are aligned with backend conventions for consistency across the project.
  Code style and type rules are centralized in shared configs where possible.

- **Assumed environment:**
  The app expects the backend to be available locally on port **8000**.
  Docker or remote APIs could easily be configured later via `.env`.

---

## 🧪 Testing

Tests use **Vitest** with **jsdom** and **React Testing Library**.
Run all tests:

```bash
npm run test
```

Or run continuously in watch mode:

```bash
npm run test:watch
```
