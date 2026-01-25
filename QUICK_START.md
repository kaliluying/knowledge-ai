# 快速启动指南

## 环境要求

- Python 3.12+
- Node.js 20+
- PostgreSQL 17 (可选，开发环境使用 SQLite)

## 快速启动

### 方式一：使用启动脚本 (Windows)

```bash
# 双击 start.bat 或在终端运行
start.bat
```

### 方式二：手动启动

#### 1. 启动后端

```bash
cd backend

# 创建虚拟环境 (可选)
python -m venv venv
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行迁移
python manage.py migrate

# 启动服务器
python manage.py runserver
```

#### 2. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 访问地址

| 服务 | 地址 |
|------|------|
| 前端页面 | http://localhost:5173 |
| 后端 API | http://localhost:8000 |
| API 健康检查 | http://localhost:8000/api/health/ |

## API 端点

### 认证模块

```bash
# 注册
POST /api/auth/register/
Body: { "email": "test@example.com", "username": "test", "password": "password123", "password_confirm": "password123" }

# 登录
POST /api/auth/login/
Body: { "email": "test@example.com", "password": "password123" }

# 获取用户信息
GET /api/auth/profile/
Headers: Authorization: Bearer <access_token>

# 更新用户信息
PUT /api/auth/profile/
Body: { "username": "new_name", "bio": "个人简介" }

# 修改密码
POST /api/auth/password/
Body: { "old_password": "old123", "new_password": "new123" }

# 刷新 Token
POST /api/auth/refresh/
Body: { "refresh": <refresh_token> }

# 登出
POST /api/auth/logout/
Body: { "refresh": <refresh_token> }
```

## 开发说明

- **开发环境**: 使用 SQLite 数据库，无需安装 PostgreSQL
- **生产环境**: 修改 `backend/.env` 中 `DEBUG=False`，使用 PostgreSQL

## 项目结构

```
knowledge/
├── backend/            # Django 后端
│   ├── apps/          # 功能模块
│   ├── config/        # 配置
│   └── utils/         # 工具模块
├── frontend/          # Vue3 前端
│   ├── src/          # 源代码
│   └── dist/         # 构建输出
├── start.bat         # 启动脚本 (Windows)
└── README.md         # 项目说明
```

## 下一步

1. 访问 http://localhost:5173
2. 注册新用户
3. 开始使用笔记管理功能
