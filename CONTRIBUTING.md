# Contributing to EngFlow

## Branches

Always branch off `master`. Use this naming format:

- `feature/short-description` — new functionality
- `fix/short-description` — bug fixes
- `chore/short-description` — setup, config, tooling

Examples:
- `feature/github-api-client`
- `fix/rate-limit-handling`
- `chore/setup-project-structure`

---

## Commits

Keep commits small and focused — one logical change per commit.

Format:
```
type: short description in lowercase

Examples:
feat: add github api client
fix: handle rate limit backoff
chore: add requirements.txt
refactor: simplify silver layer transform
```

Types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`

---

## Pull Requests

- Every piece of work gets its own PR — no committing directly to `main`
- PR title should match the issue title
- Link the issue in the PR description with `Closes #issue-number`
- The other person reviews before merging — no self-merging

---

## Local Setup

1. Clone the repo
2. Create and activate the virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Copy `.env.example` to `.env` and fill in your values:
```bash
   cp .env.example .env
```
5. Run the app:
```bash
   uvicorn api.main:app --reload
```

---

## Code Style

- Formatter: Black (runs on save in VS Code)
- Linter: Ruff (runs on save in VS Code)
- Don't disable linting rules without discussing first