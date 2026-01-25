# Personal Knowledge Management System

基于 Vue3 + Django 5.2 + PostgreSQL 17 构建的个人知识管理系统，支持笔记编辑、知识分类、内容收藏和知识图谱。

## 技术栈

- **前端**: Vue 3 + Vite + Pinia + Vue Router
- **后端**: Django 5.2 + Django REST Framework
- **数据库**: PostgreSQL 17
- **编辑器**: TipTap (类Notion块级编辑器)

## 功能特性

- 笔记管理：创建、编辑、归档、搜索
- 分类管理：层级分类、颜色标记
- 标签管理：灵活的标签系统
- 知识图谱：D3.js 可视化展示
- 内容收藏：URL抓取、内容存储
- 用户认证：JWT认证系统

## 快速开始

### 环境要求

- Python 3.12+
- Node.js 20+
- PostgreSQL 17

### 后端设置

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入数据库配置

# 运行迁移
python manage.py migrate

# 启动服务器
python manage.py runserver
```

### 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### Docker 部署

```bash
# 启动所有服务
docker-compose up -d

# 访问应用
# 前端: http://localhost:3000
# 后端 API: http://localhost:8000/api
```

## 项目结构

```
knowledge-manager/
├── backend/                    # Django后端
│   ├── config/                 # 配置模块
│   ├── apps/
│   │   ├── users/              # 用户模块
│   │   ├── notes/              # 笔记模块
│   │   ├── categories/         # 分类模块
│   │   ├── tags/               # 标签模块
│   │   ├── graph/              # 知识图谱模块
│   │   ├── collections/        # 收藏模块
│   │   └── attachments/        # 附件模块
│   └── utils/                  # 工具模块
│
├── frontend/                   # Vue3前端
│   ├── src/
│   │   ├── api/                # API调用
│   │   ├── components/         # 通用组件
│   │   ├── composables/        # 组合式函数
│   │   ├── layouts/            # 布局组件
│   │   ├── pages/              # 页面组件
│   │   ├── router/             # 路由配置
│   │   ├── stores/             # Pinia状态管理
│   │   ├── types/              # TypeScript类型
│   │   └── utils/              # 工具函数
│
├── docker-compose.yml          # Docker部署配置
├── Dockerfile.backend          # 后端Dockerfile
├── Dockerfile.frontend         # 前端Dockerfile
└── nginx.conf                  # Nginx配置
```

## API 文档

### 认证模块

```
POST   /api/auth/register/          - 用户注册
POST   /api/auth/login/             - 用户登录
POST   /api/auth/logout/            - 用户登出
GET    /api/auth/profile/           - 获取用户信息
PUT    /api/auth/profile/           - 更新用户信息
```

### 笔记模块

```
GET    /api/notes/                  - 笔记列表
POST   /api/notes/                  - 创建笔记
GET    /api/notes/{id}/             - 获取笔记详情
PUT    /api/notes/{id}/             - 更新笔记
DELETE /api/notes/{id}/             - 删除笔记
POST   /api/notes/{id}/archive/     - 归档笔记
GET    /api/notes/search/           - 搜索笔记
GET    /api/notes/recent/           - 最近笔记
```

### 分类模块

```
GET    /api/categories/             - 分类列表
POST   /api/categories/             - 创建分类
GET    /api/categories/{id}/        - 获取分类详情
PUT    /api/categories/{id}/        - 更新分类
DELETE /api/categories/{id}/        - 删除分类
GET    /api/categories/tree/        - 分类树
```

### 标签模块

```
GET    /api/tags/                   - 标签列表
POST   /api/tags/                   - 创建标签
PUT    /api/tags/{id}/              - 更新标签
DELETE /api/tags/{id}/              - 删除标签
```

### 知识图谱模块

```
GET    /api/graph/graph/            - 获取图谱数据
GET    /api/graph/related/{id}/     - 获取相关节点
POST   /api/graph/links/            - 创建链接
DELETE /api/graph/links/{id}/       - 删除链接
```

## 许可证

MIT License
