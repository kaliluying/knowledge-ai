# 部署文档

## 环境要求
- Python 3.12+
- Node.js 20+
- PostgreSQL 17
- uv

## 后端部署

```bash
cd backend
uv sync
uv run python manage.py migrate
uv run python manage.py collectstatic --noinput
uv run python manage.py runserver 0.0.0.0:8000
```

## 前端部署

```bash
cd frontend
npm install
npm run build
npm run preview -- --host 0.0.0.0 --port 3000
```

## Docker 部署

```bash
docker-compose up -d --build
```

默认端口：
- 前端: `3000`
- 后端: `8000`

## 健康检查
- 后端 API 可访问
- 前端页面可加载
- 登录、笔记列表接口可用
