# 快速启动指南

## 环境要求

- Python 3.12+
- Node.js 20+
- **PostgreSQL 17** (必须安装)

## 安装 PostgreSQL

### Windows
1. 下载 PostgreSQL 17: https://www.postgresql.org/download/windows/
2. 安装时设置:
   - 用户名: postgres
   - 密码: postgres
   - 端口: 5432
3. 创建数据库: knowledge_db

```bash
# 创建数据库 (在 psql 或 pgAdmin 中执行)
CREATE DATABASE knowledge_db;
```

### macOS
```bash
brew install postgresql@17
brew services start postgresql@17
createdb knowledge_db
```

### Linux (Ubuntu/Debian)
```bash
sudo apt install postgresql-17
sudo -u postgres createdb knowledge_db
```

## 快速启动

### 方式一：使用启动脚本 (Windows)

```bash
# 双击 start.bat 或在终端运行
start.bat
```

### 方式二：手动启动

#### 1. 配置数据库

```bash
# 编辑 backend/.env，设置正确的数据库密码
```

#### 2. 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行迁移
python manage.py migrate

# 启动服务器
python manage.py runserver
```

#### 3. 启动前端

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

## 数据库配置

项目使用 PostgreSQL 17，配置在 `backend/.env` 中:

```env
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=knowledge_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

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

## 故障排除

### 连接数据库失败

1. 检查 PostgreSQL 服务是否运行
2. 检查用户名和密码是否正确
3. 检查数据库 knowledge_db 是否存在

### 端口被占用

```bash
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :5173

# 停止占用端口的进程
taskkill /PID <PID> /F
```

## 下一步

1. 安装并启动 PostgreSQL 17
2. 创建 knowledge_db 数据库
3. 启动后端和前端服务
4. 访问 http://localhost:5173 注册用户
