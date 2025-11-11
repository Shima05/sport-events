## AI Collaboration Notes

I used ChatGPT as a support tool throughout this project — mainly to double-check configs, get examples for best practices, and speed up setup or documentation.
All final code, structure, and testing decisions were made and verified by me. I made sure I understood everything that went into the repo.

### Backend

- **Project setup:**
  I asked the AI to review my `backend/pyproject.toml` and suggest improvements for formatting, linting, and testing (using `pytest`, `coverage`, `black`, and `ruff`). I tried out each tool locally to make sure they worked together and aligned with FastAPI conventions.

- **Documentation:**
  The AI helped draft the initial `README.md` files (both root and backend). I then rewrote sections to match my actual setup steps and made sure the examples and commands were accurate.

- **Database and migrations:**
  I used AI guidance to configure Alembic (`alembic.ini`, env setup, and the first migration). I scaffolded the migrations myself and tested them against Postgres to confirm schema creation and downgrades worked properly.

- **ORM setup:**
  I had the AI review my async SQLAlchemy session and model definitions based on the [official docs](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html). I checked all examples it gave and adjusted my implementation where it made sense — especially around async session handling.

- **Testing:**
  The AI helped outline both unit and integration test ideas (like checking metadata or verifying migration upgrades/downgrades). I wrote and ran these tests myself, refining them until coverage looked solid.

- **Service & repository layer:**
  I got a few AI code review suggestions on structure and test coverage. I implemented the final logic for event creation/listing and made sure all end-to-end tests passed cleanly.

- **API routes:**
  The AI helped me expand integration tests for the `/events` endpoints. I wrote the final assertions and verified payloads and responses manually.

### Frontend

- **Tooling:**
  The AI helped me set up the frontend developer tooling — mainly ESLint, Prettier, and TypeScript configs. I adjusted rules to match how I like to structure React code and confirmed everything built successfully.

- **UI/UX feedback:**
  I used the AI for a few design and layout reviews. It gave me quick feedback on styling and readability, but I made the final UI decisions based on my own testing and preferences.

---

### Reflection

AI support primarily helped accelerate setup, documentation, and testing scaffolding.
I treated AI feedback as a peer code review rather than direct implementation — verifying each suggestion for correctness and maintainability before adopting it.
If given more time, I would focus on expanding integration coverage and improving frontend test automation.
