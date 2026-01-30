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
```

### Backend (Django)
```bash
cd backend

# Using uv (recommended - 10-100x faster than pip)
uv venv && source venv/bin/activate  # Linux/Mac
# or: uv venv && venv\Scripts\activate  # Windows
uv pip install -r requirements.txt
python manage.py migrate
python manage.py runserver          # API server at localhost:8000
pytest                              # Run all tests
pytest apps/users/tests.py::TestUser::test_create_user  # Single test
flake8 apps/                        # Lint code
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
| Frontend | Vue 3, Vite, Pinia, Vue Router, TypeScript, Axios |
| Editor | TipTap (block-based, Notion-like) |
| Visualization | D3.js for knowledge graph |
| Backend | Django 5.2, Django REST Framework |
| Tree Structure | django-mptt for hierarchical categories |
| Auth | djangorestframework-simplejwt |
| Database | PostgreSQL 17 |

## Code Conventions

### TypeScript/Vue 3
- Imports: `@/` alias, order: external libs → internal modules
- Components: `.vue` files use PascalCase
- Pinia stores: Composition API pattern (`defineStore('name', () => {...})`)
- API responses: `{ code, message, data }` wrapper

### Python/Django
- Imports order: standard lib → third party → local apps
- Response format: `{"code": 200, "message": "Success", "data": result}`
- Validation: explicit `serializer.is_valid()` with error handling

## API Patterns

All API responses follow this structure:
```json
{
  "code": 200,
  "message": "Success",
  "data": { ... }
}
```

Common endpoints:
- `POST /api/auth/register/`, `/api/auth/login/`, `/api/auth/logout/`
- `GET/POST/PUT/DELETE /api/notes/`, `/api/categories/`, `/api/tags/`
- `GET /api/graph/graph/` - Knowledge graph data
- `POST /api/collections/` - Create collection with URL fetch

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
