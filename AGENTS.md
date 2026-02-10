# AGENTS.md - Repository Guide for Agentic Coding

## 1) Project Snapshot
- Personal Knowledge Management System
- Frontend: Vue 3 + TypeScript + Vite + Pinia + Tailwind CSS v4
- Backend: Django 5.2 + DRF + PostgreSQL 17
- Auth: JWT (djangorestframework-simplejwt)

## 2) Build / Lint / Test Commands

### Frontend (`frontend/`)
```bash
npm install
npm run dev
npm run build
npm run preview
npm run lint
npm run format
npm run test
npm run test:run
npm run test:ui
```

Single test (frontend):
```bash
npm run test -- tests/unit/path/to/file.spec.ts
```

Vitest details (`frontend/vitest.config.ts`):
- `environment: 'jsdom'`
- `globals: true`
- include: `tests/unit/**/*.{test,spec}.{js,ts,jsx,tsx}`
- coverage provider: `v8`

### Backend (`backend/`)
```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
uv run pytest
uv run flake8 apps/
```

Single test (backend):
```bash
uv run pytest apps/users/tests.py::TestUser::test_create_user
```

Pytest defaults (`backend/pyproject.toml`):
- `DJANGO_SETTINGS_MODULE = "config.settings"`
- `python_files = ["test_*.py"]`
- `python_classes = ["Test*"]`
- `python_functions = ["test_*"]`
- `addopts = "-v --tb=short"`

## 3) Key Files to Read First
- `frontend/package.json`
- `frontend/vite.config.ts`
- `frontend/tsconfig.app.json`
- `frontend/vitest.config.ts`
- `frontend/src/api/index.ts`
- `frontend/src/stores/auth.ts`
- `backend/pyproject.toml`
- `backend/utils/exceptions.py`
- `backend/utils/responses.py`
- `backend/tests/conftest.py`
- `backend/utils/permissions.py`
- `backend/utils/pagination.py`

## 4) Frontend Style Guide

### Core Patterns
- Use `<script setup lang="ts">` in SFCs.
- Use Composition API (`ref`, `computed`, composables).
- Use strongly typed props/emits.
- Prefer `withDefaults(defineProps<Props>(), defaults)` for optional props.
- Use `import type` for type-only imports.

### Import Conventions
- Recommended order:
  1. Vue/framework imports
  2. third-party packages
  3. internal `@/` modules (`stores`, `api`, `types`)
  4. relative local imports

### Naming Conventions
- Components/pages: PascalCase (`NoteCard.vue`, `Login.vue`)
- Composables: `useX` (`useAuth.ts`, `useNotes.ts`)
- Stores: file `x.ts`, export `useXStore`
- Types: grouped under `frontend/src/types/*.ts`

### State/API/Error Conventions
- Pinia uses setup-style `defineStore('name', () => {})`.
- API modules in `frontend/src/api/*.ts`, shared axios in `frontend/src/api/index.ts`.
- Backend payload expected by UI: `{ code, message, data }`.
- Paginated lists often use `{ count, next, previous, results }`.
- Typical store-level error mapping:

```typescript
catch (error: unknown) {
  const axiosError = error as { response?: { data?: { message?: string } } };
  return { success: false, message: axiosError.response?.data?.message || 'Error' };
}
```

### Styling
- Prefer `<style scoped>` for component isolation.
- Use `:deep(...)` for nested child selectors in scoped styles.
- Keep styles local unless a shared pattern is clearly needed.

## 5) Backend Style Guide

### Python/DRF Conventions
- Import order: standard lib -> third-party -> local modules.
- Naming: snake_case (functions/vars), PascalCase (classes), UPPER_SNAKE_CASE (constants).
- Primary API shape: DRF `ModelViewSet` + serializers.
- Use `@action` for non-CRUD endpoints.

### Response and Exception Conventions
- Keep response payload consistent with `code`, `message`, and optional `data`/`errors`.
- Use centralized error normalization in `utils.exceptions.custom_exception_handler`.
- Raise explicit `ValidationError` messages in serializers/services.

### Permissions / Pagination / Tests
- Reuse `utils.permissions` classes (e.g., `IsOwnerOrReadOnly`).
- Reuse `utils.pagination` classes (e.g., `StandardPagination`, `NotePagination`).
- Reuse fixtures from `backend/tests/conftest.py`.
- Run targeted tests via node id: `pytest path::Class::test_name`.

## 6) Directory Map
```text
frontend/src/
  api/ components/ composables/ layouts/ pages/ router/ stores/ types/

backend/
  apps/ config/ tests/ utils/
```

## 7) Cursor / Copilot Rules
Checked:
- `.cursor/rules/`
- `.cursorrules`
- `.github/copilot-instructions.md`

Current result: no Cursor/Copilot rule files found.
