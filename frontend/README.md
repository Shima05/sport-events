# Frontend (Vite + React)

This is the UI for the sports events calendar.

It renders the calendar, filters, pagination, responsive layout — and talks to our FastAPI backend (default: `http://localhost:8000/api/v1`) using generated OpenAPI types so we stay fully typesafe end-to-end.

## Requirements

- Node.js 20+
- A local backend running — otherwise you won’t have live data + you can’t regenerate the OpenAPI client

## Install

```bash
cd frontend
npm install
```

## Scripts

| Command                | What it does                                                     |
| ---------------------- | ---------------------------------------------------------------- |
| `npm run dev`          | Start Vite dev server w/ HMR                                     |
| `npm run build`        | Type check + production build                                    |
| `npm run preview`      | Preview production build locally                                 |
| `npm run lint`         | Run ESLint (Prettier opinions enforced) over the entire source   |
| `npm run format`       | Prettier write (generated schema is auto skipped)                |
| `npm run test`         | Run Vitest in CI mode (jsdom + Testing Library)                  |
| `npm run test:watch`   | Vitest watch mode                                                |
| `npm run generate:api` | Re-generate our typed OpenAPI client from `backend/openapi.json` |

### Environment Variables

Create a `.env` file (or export in shell):

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

If not set — the above default is used.

### Re-generating the OpenAPI Client

1. make sure FastAPI backend is running
   (from `/backend`)

2. pull fresh schema:

```bash
curl http://localhost:8000/openapi.json -o backend/openapi.json
```

3. re-build the TS client:

```bash
cd frontend
npm run generate:api
```

The generated file ends up in `src/api/generated-schema.ts`.
