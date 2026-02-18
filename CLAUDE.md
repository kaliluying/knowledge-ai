# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal Knowledge Management System - Vue 3 + Django 5.2 + PostgreSQL 17. Supports notes, categories, tags, knowledge graph, content collections, and attachments.

## Build Commands

### Frontend (Vue 3)
```bash
cd frontend
npm install
npm run dev          # Development server at localhost:3000
npm run build        # Type check + build (vue-tsc -b && vite build)
npm run preview      # Preview production build
npm run lint         # Lint with ESLint
npm run format       # Format with Prettier
npm run test         # Run vitest unit tests
npm run test:run     # Run tests in CI mode
npm run test:ui      # Run tests with UI
```

### Backend (Django)
```bash
cd backend

# Using uv (recommended - 10-100x faster than pip)
uv sync
uv run python manage.py migrate
uv run python manage.py runserver          # API server at localhost:8000
uv run pytest                              # Run all tests
uv run pytest apps/users/tests.py::TestUser::test_create_user  # Single test
uv run flake8 apps/                        # Lint code
```

### Docker
```bash
docker-compose up -d
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api
```

## Architecture

```
knowledge/
├── frontend/                    # Vue 3 SPA
│   └── src/
│       ├── api/                # Axios API modules (authApi, notesApi, etc.)
│       ├── components/         # Reusable Vue components (common/, editor/, layout/, tags/)
│       ├── composables/        # Composition API functions (useAuth, useNotes, etc.)
│       ├── pages/              # Route page components
│       ├── stores/             # Pinia stores (auth, notes, categories, tags)
│       ├── types/              # TypeScript interfaces
│       ├── router/             # Vue Router config
│       └── layouts/            # Layout components
│
├── backend/                    # Django REST API
│   └── apps/
│       ├── users/              # User authentication (register, login, profile)
│       ├── notes/              # Notes CRUD, archive, search
│       ├── categories/         # Hierarchical categories (django-mptt)
│       ├── tags/               # Tag management
│       ├── graph/              # Knowledge graph (D3.js visualization)
│       ├── collections/        # URL/content collections
│       └── attachments/        # File attachments
│
├── config/                     # Django settings, URLs, CORS, JWT config
└── utils/                      # Shared utilities (responses, permissions, middleware)
```

## Key Libraries

| Layer | Technologies |
|-------|-------------|
| Frontend | Vue 3, Vite, Pinia, Vue Router, TypeScript, Axios, Tailwind CSS v4 |
| Editor | TipTap (block-based, Notion-like) |
| Visualization | D3.js for knowledge graph |
| Backend | Django 5.2, Django REST Framework |
| Tree Structure | django-mptt for hierarchical categories |
| Auth | djangorestframework-simplejwt |
| Database | PostgreSQL 17 |
| Python Package Manager | uv |

## Key Files to Read First

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

## Code Conventions

### TypeScript/Vue 3
- Imports: `@/` alias, order: Vue/framework → third-party → internal `@/` modules → relative imports
- Components: `.vue` files use PascalCase
- Pinia stores: Composition API pattern (`defineStore('name', () => {...})`)
- API responses: `{ code, message, data }` wrapper
- Use `<script setup lang="ts">` in SFCs
- Use strongly typed props/emits with `withDefaults(defineProps<Props>(), defaults)`
- Use `import type` for type-only imports
- Prefer `<style scoped>` for component isolation
- Use `:deep(...)` for nested child selectors in scoped styles

### Python/Django
- Imports order: standard lib → third party → local apps
- Naming: snake_case (functions/vars), PascalCase (classes), UPPER_SNAKE_CASE (constants)
- Response format: `{"code": 200, "message": "Success", "data": result}`
- Validation: explicit `serializer.is_valid()` with error handling
- Primary API shape: DRF `ModelViewSet` + serializers
- Use `@action` for non-CRUD endpoints

## API Patterns

All API responses follow this structure:
```json
{
  "code": 200,
  "message": "Success",
  "data": { ... }
}
```

Paginated lists use:
```json
{
  "count": 100,
  "next": "http://...",
  "previous": null,
  "results": [...]
}
```

Common endpoints:
- `POST /api/auth/register/`, `/api/auth/login/`, `/api/auth/logout/`
- `GET/POST/PUT/DELETE /api/notes/`, `/api/categories/`, `/api/tags/`
- `GET /api/graph/graph/` - Knowledge graph data
- `POST /api/collections/` - Create collection with URL fetch

## Error Handling

### Frontend
Typical store-level error mapping:
```typescript
catch (error: unknown) {
  const axiosError = error as { response?: { data?: { message?: string } } };
  return { success: false, message: axiosError.response?.data?.message || 'Error' };
}
```

### Backend
- Use centralized error normalization in `utils.exceptions.custom_exception_handler`
- Raise explicit `ValidationError` messages in serializers/services
- Reuse `utils.permissions` classes (e.g., `IsOwnerOrReadOnly`)
- Reuse `utils.pagination` classes (e.g., `StandardPagination`, `NotePagination`)

## Environment Variables

**Frontend (.env)**: `VITE_API_URL=http://localhost:8000/api`

**Backend (.env)**:
```
SECRET_KEY=...
DEBUG=True
DATABASE_NAME=knowledge_db
DATABASE_USER=postgres
DATABASE_PASSWORD=...
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

## Testing

### Frontend (Vitest)
- `environment: 'jsdom'`
- `globals: true`
- Include: `tests/unit/**/*.{test,spec}.{js,ts,jsx,tsx}`
- Single test: `npm run test -- tests/unit/path/to/file.spec.ts`

### Backend (Pytest)
- `DJANGO_SETTINGS_MODULE = "config.settings"`
- `python_files = ["test_*.py"]`
- `python_classes = ["Test*"]`
- `python_functions = ["test_*"]`
- `addopts = "-v --tb=short"`
- Single test: `uv run pytest apps/users/tests.py::TestUser::test_create_user`
- Reuse fixtures from `backend/tests/conftest.py`
