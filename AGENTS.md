# AGENTS.md - Codebase Guidelines for AI Agents

## Project Overview

Personal Knowledge Management System built with:
- Frontend: Vue 3 + TypeScript + Vite + Pinia + Tailwind CSS v4
- Backend: Django 5.2 + Django REST Framework + PostgreSQL 17

## Build / Run / Test

### Frontend (from `frontend/package.json`)

```bash
cd frontend
npm install
npm run dev           # Vite dev server
npm run build         # vue-tsc -b && vite build
npm run preview       # Preview production build
npm run lint          # eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix
npm run format        # prettier --write src/
npm run test          # Vitest watch
npm run test:run      # Vitest run (CI)
npm run test:ui       # Vitest UI
```

Single test (frontend): no repo-specific script. Use Vitest CLI args via npm:
`npm run test -- <vitest-args>` (for example, pass a test file path).

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate  # Create venv
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
pytest                                           # Run all tests
pytest apps/users/tests.py::TestUser::test_create_user  # Single test
flake8 apps/                                     # Lint code
```

## Config Files Worth Knowing

- `frontend/vite.config.ts`: `@` alias points to `frontend/src`.
- `frontend/tsconfig.json`: project references to app/node tsconfigs.
- `backend/pyproject.toml`: pytest settings (`DJANGO_SETTINGS_MODULE`, addopts).
- `backend/utils/exceptions.py`: DRF exception handler and error format.
- `backend/utils/responses.py`: shared `{ code, message, data, errors }` response model.

## Code Style Guidelines

### TypeScript / Vue 3

- Use `<script setup lang="ts">` in SFCs, Composition API everywhere.
- Imports: external libs first, then `@/` aliases; use `import type` for types.
- Naming: components PascalCase, files kebab-case, composables `useX`.
- Prefer `withDefaults(defineProps<Props>(), defaults)` for props and typed `defineEmits`.
- Use `ref` for state and `computed` for derived values.
- API modules live in `frontend/src/api/*.ts` and use the shared axios instance.

Example import order:
```typescript
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores';
import type { User } from '@/types';
```

Pinia store pattern:
```typescript
export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const isLoading = ref(false);
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value);
  async function login(params: LoginParams) { /* ... */ }
  return { user, isLoading, isAuthenticated, login };
});
```

Error handling (pattern used in stores):
```typescript
try { await someAsyncCall(); }
catch (error: unknown) {
  const axiosError = error as { response?: { data?: { message?: string } } };
  return { success: false, message: axiosError.response?.data?.message || 'Error' };
}
```

Styling:
- Most components use `<style scoped>` with handcrafted CSS.
- Use `:deep(...)` for nested selectors inside scoped styles.

API response expectations:
- Most endpoints return `{ code, message, data }`.
- List endpoints often return pagination (`count`, `results`, `next`, `previous`).

### Python / Django

- Imports order: standard lib → third party → local apps.
- Naming: functions/vars snake_case, classes PascalCase, constants SCREAMING_SNAKE_CASE.
- Prefer DRF `ModelViewSet` + serializers for CRUD.
- Use `@action` for custom endpoints and return `Response` with `{ code, message, data }`.
- Validation errors use serializer `ValidationError` with explicit messages.
- Exception handling is centralized via `utils.exceptions.custom_exception_handler`.

Example response pattern:
```python
return Response({"code": 200, "message": "success", "data": result})
```

## Directory Structure

```
frontend/src/
├── api/              # API modules
├── components/       # Reusable Vue components
├── composables/      # Composition utilities
├── layouts/          # Layout components
├── pages/            # Route components
├── router/           # Vue Router config
├── stores/           # Pinia stores
└── types/            # TypeScript interfaces

backend/
├── apps/             # Django apps
├── config/           # Settings, URLs, DRF config
└── utils/            # Shared utilities
```

## Environment Variables

Frontend (`frontend/.env`):
`VITE_API_URL=http://localhost:8000/api`

Backend (`backend/.env`):
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_NAME=knowledge_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

## Cursor / Copilot Rules

No `.cursor/rules/`, `.cursorrules`, or `.github/copilot-instructions.md` found.
