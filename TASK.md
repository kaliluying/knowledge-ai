# Personal Knowledge Management System - 开发任务文档

> 最后更新: 2026-01-25

## 项目概述

基于 Vue3 + Django 5.2 + PostgreSQL 17 的个人知识管理系统，包含笔记管理、分类标签、知识图谱、内容收藏等功能。

### 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + Pinia + Vue Router + TypeScript |
| 后端 | Django 5.2 + Django REST Framework + uv |
| 数据库 | PostgreSQL 17 |
| 编辑器 | TipTap |
| 可视化 | D3.js |
| 部署 | Docker + Nginx |

### Python 包管理

本项目使用 [uv](https://github.com/astral-sh/uv) 作为 Python 包管理器，相比 pip 快 10-100 倍。

```bash
# 安装 uv (如果未安装)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
winget install astral-sh.uv
```

---

## 一、项目初始化任务

### 1.1 仓库与结构初始化

| 任务ID | 任务名称 | 描述 | 优先级 | 状态 |
|--------|----------|------|--------|------|
| T-001 | 创建项目目录结构 | 创建 backend/frontend 目录及基础结构 | P0 | 待开发 |
| T-002 | 初始化 Git 仓库 | 配置 gitignore、README、基础分支策略 | P0 | 待开发 |
| T-003 | 配置开发环境 | Python 虚拟环境、Node.js 版本配置 | P0 | 待开发 |

### 1.2 后端初始化

| 任务ID | 任务名称 | 描述 | 优先级 | 状态 |
|--------|----------|------|--------|------|
| T-004 | 创建 Django 项目 | 使用 django-admin startproject 创建项目 | P0 | 待开发 |
| T-005 | 配置基础依赖 | 创建 requirements.txt，添加 Django、DRF 等依赖 | P0 | 待开发 |
| T-006 | 配置环境变量 | 创建 .env.example，配置数据库、JWT 等 | P0 | 待开发 |
| T-007 | 配置数据库连接 | 配置 PostgreSQL 连接，设置 DATABSE_URL | P0 | 待开发 |
| T-008 | 配置日志系统 | 配置 logging.py，设置日志格式和输出 | P1 | 待开发 |
| T-009 | 配置 CORS | 安装并配置 django-cors-headers | P0 | 待开发 |

### 1.3 前端初始化

| 任务ID | 任务名称 | 描述 | 优先级 | 状态 |
|--------|----------|------|--------|------|
| T-010 | 创建 Vue3 项目 | 使用 Vite 创建 Vue3 + TypeScript 项目 | P0 | 待开发 |
| T-011 | 配置基础依赖 | 安装 vue-router、pinia、axios 等 | P0 | 待开发 |
| T-012 | 配置代码规范 | 安装并配置 ESLint、Prettier | P1 | 待开发 |
| T-013 | 配置环境变量 | 创建 .env.development、.env.production | P1 | 待开发 |
| T-014 | 配置 Sass | 安装 sass，设置全局样式变量 | P1 | 待开发 |

---

## 二、后端开发任务

### 2.1 公共模块

#### 2.1.1 工具模块 (utils/)

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-020 | 统一响应格式 | 创建 ResponseModel 类，统一 API 响应格式 | utils/responses.py | P0 | 待开发 |
| T-021 | 自定义权限类 | 创建 IsOwnerOrReadOnly 等权限类 | utils/permissions.py | P0 | 待开发 |
| T-022 | 分页器 | 创建 StandardPagination 分页类 | utils/pagination.py | P1 | 待开发 |
| T-023 | 异常处理器 | 创建自定义异常及 handler | utils/exceptions.py | P1 | 待开发 |
| T-024 | 工具函数集 | 创建日期处理、字符串处理等工具函数 | utils/helpers.py | P2 | 待开发 |

#### 2.1.2 配置模块 (config/)

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-025 | 主配置 | 配置 Django settings.py | config/settings.py | P0 | 待开发 |
| T-026 | 主路由 | 配置主 URL 路由 | config/urls.py | P0 | 待开发 |
| T-027 | WSGI/ASGI 配置 | 配置生产环境入口 | config/wsgi.py | P1 | 待开发 |
| T-028 | REST Framework 配置 | 配置 DRF pagination、renderer 等 | config/rest_framework.py | P1 | 待开发 |

---

### 2.2 用户认证模块 (users)

#### 2.2.1 数据模型

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-030 | 创建用户模型 | 继承 AbstractUser，添加 avatar、bio 字段 | apps/users/models.py | P0 | 待开发 |
| T-031 | 创建用户管理器 | 自定义用户创建方法 | apps/users/managers.py | P0 | 待开发 |
| T-032 | 创建 Profile 模型 | 扩展用户详细信息（可选） | apps/users/models.py | P2 | 待开发 |

#### 2.2.2 序列化器

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-033 | 用户注册序列化器 | UserCreateSerializer | apps/users/serializers.py | P0 | 待开发 |
| T-034 | 用户详情序列化器 | UserSerializer | apps/users/serializers.py | P0 | 待开发 |
| T-035 | 登录序列化器 | LoginSerializer | apps/users/serializers.py | P0 | 待开发 |
| T-036 | 密码重置序列化器 | PasswordResetSerializer | apps/users/serializers.py | P2 | 待开发 |

#### 2.2.3 视图集

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-037 | 注册视图 | RegisterView | apps/users/views.py | P0 | 待开发 |
| T-038 | 登录视图 | LoginView，获取 JWT Token | apps/users/views.py | P0 | 待开发 |
| T-039 | 登出视图 | LogoutView | apps/users/views.py | P1 | 待开发 |
| T-040 | Token 刷新视图 | RefreshTokenView | apps/users/views.py | P0 | 待开发 |
| T-041 | 用户信息视图 | ProfileView (GET/PUT) | apps/users/views.py | P0 | 待开发 |
| T-042 | 密码修改视图 | ChangePasswordView | apps/users/views.py | P1 | 待开发 |

#### 2.2.4 URL 路由

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-043 | 用户模块路由 | 配置 /api/auth/ 路由 | apps/users/urls.py | P0 | 待开发 |

#### 2.2.5 管理后台

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-044 | 用户管理注册 | 注册用户模型到 Admin | apps/users/admin.py | P1 | 待开发 |

#### 2.2.6 测试

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-045 | 用户单元测试 | 测试用户注册、登录等功能 | apps/users/tests.py | P1 | 待开发 |
| T-046 | 用户 API 测试 | 测试所有 API 端点 | apps/users/tests.py | P1 | 待开发 |

---

### 2.3 分类管理模块 (categories)

#### 2.3.1 数据模型

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-050 | 创建分类模型 | 使用 django-mptt 实现树形结构 | apps/categories/models.py | P0 | 待开发 |
| T-051 | 添加层级验证 | 限制最大层级为 3 | apps/categories/models.py | P1 | 待开发 |

#### 2.3.2 序列化器

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-052 | 分类序列化器 | CategorySerializer | apps/categories/serializers.py | P0 | 待开发 |
| T-053 | 分类树序列化器 | CategoryTreeSerializer | apps/categories/serializers.py | P0 | 待开发 |

#### 2.3.3 视图集

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-054 | 分类 CRUD 视图 | CategoryViewSet | apps/categories/views.py | P0 | 待开发 |
| T-055 | 分类树视图 | 获取完整分类树 | apps/categories/views.py | P0 | 待开发 |

#### 2.3.4 URL 路由

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-056 | 分类模块路由 | 配置 /api/categories/ 路由 | apps/categories/urls.py | P0 | 待开发 |

#### 2.3.5 管理后台

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-057 | 分类管理注册 | 注册分类模型到 Admin | apps/categories/admin.py | P1 | 待开发 |

---

### 2.4 标签管理模块 (tags)

#### 2.4.1 数据模型

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-060 | 创建标签模型 | Tag 模型 (name, slug, color) | apps/tags/models.py | P0 | 待开发 |
| T-061 | 自动生成 slug | 保存时自动生成 slug | apps/tags/models.py | P0 | 待开发 |

#### 2.4.2 序列化器

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-062 | 标签序列化器 | TagSerializer | apps/tags/serializers.py | P0 | 待开发 |
| T-063 | 标签列表序列化器 | TagListSerializer (精简版) | apps/tags/serializers.py | P1 | 待开发 |

#### 2.4.3 视图集

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-064 | 标签 CRUD 视图 | TagViewSet | apps/tags/views.py | P0 | 待开发 |
| T-065 | 热门标签视图 | 获取使用频率最高的标签 | apps/tags/views.py | P1 | 待开发 |

#### 2.4.4 URL 路由

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-066 | 标签模块路由 | 配置 /api/tags/ 路由 | apps/tags/urls.py | P0 | 待开发 |

---

### 2.5 笔记管理模块 (notes)

#### 2.5.1 数据模型

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-070 | 创建笔记模型 | Note 模型 (title, content, category) | apps/notes/models.py | P0 | 待开发 |
| T-072 | 添加封面图字段 | cover_image URL 字段 | apps/notes/models.py | P1 | 待开发 |
| T-073 | 添加归档字段 | is_archived 布尔字段 | apps/notes/models.py | P0 | 待开发 |
| T-074 | 添加置顶字段 | is_pinned 布尔字段 | apps/notes/models.py | P1 | 待开发 |
| T-075 | 添加索引 | 为 author、created_at 添加数据库索引 | apps/notes/models.py | P1 | 待开发 |

#### 2.5.2 序列化器

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-076 | 笔记详情序列化器 | NoteSerializer (完整字段) | apps/notes/serializers.py | P0 | 待开发 |
| T-077 | 笔记列表序列化器 | NoteListSerializer (精简版) | apps/notes/serializers.py | P0 | 待开发 |
| T-078 | 笔记创建序列化器 | NoteCreateSerializer | apps/notes/serializers.py | P0 | 待开发 |

#### 2.5.3 视图集

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-079 | 笔记 CRUD 视图 | NoteViewSet | apps/notes/views.py | P0 | 待开发 |
| T-080 | 归档操作视图 | archive action | apps/notes/views.py | P0 | 待开发 |
| T-081 | 搜索视图 | search action (全文搜索) | apps/notes/views.py | P0 | 待开发 |
| T-082 | 最近笔记视图 | recent action | apps/notes/views.py | P1 | 待开发 |
| T-083 | 按分类筛选 | 过滤指定分类的笔记 | apps/notes/views.py | P1 | 待开发 |
| T-084 | 按标签筛选 | 过滤指定标签的笔记 | apps/notes/views.py | P1 | 待开发 |

#### 2.5.4 URL 路由

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-085 | 笔记模块路由 | 配置 /api/notes/ 路由 | apps/notes/urls.py | P0 | 待开发 |

#### 2.5.5 信号处理

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-086 | 自动生成 slug | 使用 title 生成唯一 slug | apps/notes/signals.py | P0 | 待开发 |

#### 2.5.6 管理后台

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-087 | 笔记管理注册 | 注册笔记模型到 Admin | apps/notes/admin.py | P1 | 待开发 |

---

### 2.6 知识图谱模块 (graph)

#### 2.6.1 数据模型

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-090 | 创建图谱节点模型 | GraphNode 模型 | apps/graph/models.py | P1 | 待开发 |
| T-091 | 创建图谱链接模型 | GraphLink 模型 | apps/graph/models.py | P1 | 待开发 |

#### 2.6.2 序列化器

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-092 | 图谱数据序列化器 | GraphDataSerializer | apps/graph/serializers.py | P1 | 待开发 |
| T-093 | 节点序列化器 | GraphNodeSerializer | apps/graph/serializers.py | P1 | 待开发 |
| T-094 | 链接序列化器 | GraphLinkSerializer | apps/graph/serializers.py | P1 | 待开发 |

#### 2.6.3 视图集

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-095 | 图谱数据视图 | 获取完整图谱数据 | apps/graph/views.py | P1 | 待开发 |
| T-096 | 相关节点视图 | 获取指定节点的相关节点 | apps/graph/views.py | P1 | 待开发 |
| T-097 | 链接管理视图 | 创建/删除图谱链接 | apps/graph/views.py | P2 | 待开发 |
| T-098 | 图谱生成服务 | 生成图谱数据的 service | apps/graph/services.py | P1 | 待开发 |

#### 2.6.4 URL 路由

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-099 | 图谱模块路由 | 配置 /api/graph/ 路由 | apps/graph/urls.py | P1 | 待开发 |

---

### 2.7 内容收藏模块 (collections)

#### 2.7.1 数据模型

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-100 | 创建收藏模型 | Collection 模型 | apps/collections/models.py | P1 | 待开发 |
| T-101 | 状态字段 | is_processed 处理状态 | apps/collections/models.py | P1 | 待开发 |

#### 2.7.2 序列化器

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-102 | 收藏序列化器 | CollectionSerializer | apps/collections/serializers.py | P1 | 待开发 |
| T-103 | 收藏创建序列化器 | CollectionCreateSerializer | apps/collections/serializers.py | P1 | 待开发 |

#### 2.7.3 视图集

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-104 | 收藏 CRUD 视图 | CollectionViewSet | apps/collections/views.py | P1 | 待开发 |
| T-105 | URL 抓取服务 | 抓取网页内容的 service | apps/collections/services.py | P1 | 待开发 |
| T-106 | 内容提取服务 | 使用 BeautifulSoup 提取正文 | apps/collections/services.py | P1 | 待开发 |

#### 2.7.4 URL 路由

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-107 | 收藏模块路由 | 配置 /api/collections/ 路由 | apps/collections/urls.py | P1 | 待开发 |

---

### 2.8 附件管理模块 (attachments)

#### 2.8.1 数据模型

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-110 | 创建附件模型 | Attachment 模型 | apps/attachments/models.py | P1 | 待开发 |
| T-111 | 文件类型验证 | 限制上传文件类型 | apps/attachments/models.py | P1 | 待开发 |
| T-112 | 文件大小限制 | 限制最大文件大小 | apps/attachments/models.py | P1 | 待开发 |

#### 2.8.2 视图集

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-113 | 附件上传视图 | 上传文件到云存储或本地 | apps/attachments/views.py | P1 | 待开发 |
| T-114 | 附件管理视图 | 附件 CRUD 操作 | apps/attachments/views.py | P1 | 待开发 |

#### 2.8.3 URL 路由

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-115 | 附件模块路由 | 配置 /api/attachments/ 路由 | apps/attachments/urls.py | P1 | 待开发 |

---

## 三、前端开发任务

### 3.1 基础架构

#### 3.1.1 类型定义

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-200 | 用户类型定义 | User 接口定义 | src/types/user.ts | P0 | 待开发 |
| T-201 | 笔记类型定义 | Note 接口定义 | src/types/note.ts | P0 | 待开发 |
| T-202 | 分类类型定义 | Category 接口定义 | src/types/category.ts | P0 | 待开发 |
| T-203 | 标签类型定义 | Tag 接口定义 | src/types/tag.ts | P0 | 待开发 |
| T-204 | 图谱类型定义 | GraphData 接口定义 | src/types/graph.ts | P1 | 待开发 |
| T-205 | 收藏类型定义 | Collection 接口定义 | src/types/collection.ts | P1 | 待开发 |
| T-206 | API 响应类型 | ApiResponse 接口定义 | src/types/api.ts | P0 | 待开发 |

#### 3.1.2 API 层

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-210 | Axios 实例配置 | api/index.ts (拦截器、baseURL) | src/api/index.ts | P0 | 待开发 |
| T-211 | 认证 API | auth.ts (login, register, logout) | src/api/auth.ts | P0 | 待开发 |
| T-212 | 笔记 API | notes.ts (CRUD, search) | src/api/notes.ts | P0 | 待开发 |
| T-213 | 分类 API | categories.ts | src/api/categories.ts | P0 | 待开发 |
| T-214 | 标签 API | tags.ts | src/api/tags.ts | P0 | 待开发 |
| T-215 | 图谱 API | graph.ts | src/api/graph.ts | P1 | 待开发 |
| T-216 | 收藏 API | collections.ts | src/api/collections.ts | P1 | 待开发 |

#### 3.1.3 路由配置

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-220 | 路由配置 | router/index.ts | src/router/index.ts | P0 | 待开发 |
| T-221 | 路由守卫 | 实现登录验证 | src/router/index.ts | P0 | 待开发 |

---

### 3.2 状态管理 (Pinia Stores)

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-230 | 认证状态 | auth.ts (login, logout, user) | src/stores/auth.ts | P0 | 待开发 |
| T-231 | 笔记状态 | notes.ts (notes 列表、操作) | src/stores/notes.ts | P0 | 待开发 |
| T-232 | 分类状态 | categories.ts | src/stores/categories.ts | P0 | 待开发 |
| T-233 | 标签状态 | tags.ts | src/stores/tags.ts | P0 | 待开发 |
| T-234 | 图谱状态 | graph.ts | src/stores/graph.ts | P1 | 待开发 |
| T-235 | 布局状态 | layout.ts (侧边栏折叠、主题) | src/stores/layout.ts | P1 | 待开发 |

---

### 3.3 通用组件

#### 3.3.1 基础组件

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-240 | 按钮组件 | Button.vue | src/components/common/Button.vue | P0 | 待开发 |
| T-241 | 输入框组件 | Input.vue | src/components/common/Input.vue | P0 | 待开发 |
| T-242 | 选择框组件 | Select.vue | src/components/common/Select.vue | P1 | 待开发 |
| T-243 | 模态框组件 | Modal.vue | src/components/common/Modal.vue | P1 | 待开发 |
| T-244 | 空状态组件 | Empty.vue | src/components/common/Empty.vue | P2 | 待开发 |
| T-245 | 加载组件 | Loading.vue | src/components/common/Loading.vue | P1 | 待开发 |
| T-246 | 消息提示 | Toast.vue | src/components/common/Toast.vue | P1 | 待开发 |
| T-247 | 分页组件 | Pagination.vue | src/components/common/Pagination.vue | P1 | 待开发 |

#### 3.3.2 布局组件

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-250 | 主布局 | MainLayout.vue (侧边栏 + 内容区) | src/layouts/MainLayout.vue | P0 | 待开发 |
| T-251 | 侧边栏 | Sidebar.vue | src/components/layout/Sidebar.vue | P0 | 待开发 |
| T-252 | 顶部栏 | Header.vue | src/components/layout/Header.vue | P0 | 待开发 |
| T-253 | 面包屑 | Breadcrumb.vue | src/components/layout/Breadcrumb.vue | P1 | 待开发 |
| T-254 | 标签页导航 | TabNav.vue | src/components/layout/TabNav.vue | P2 | 待开发 |

---

### 3.4 业务组件

#### 3.4.1 编辑器组件

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-260 | TipTap 编辑器 | Tiptap.vue | src/components/editor/Tiptap.vue | P0 | 待开发 |
| T-261 | 浮动菜单 | BubbleMenu.vue | src/components/editor/BubbleMenu.vue | P1 | 待开发 |
| T-262 | 固定菜单 | FloatingMenu.vue | src/components/editor/FloatingMenu.vue | P1 | 待开发 |
| T-263 | 图片上传 | ImageUploader.vue | src/components/editor/ImageUploader.vue | P1 | 待开发 |

#### 3.4.2 分类组件

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-270 | 分类树 | CategoryTree.vue (树形展示) | src/components/categories/CategoryTree.vue | P0 | 待开发 |
| T-271 | 分类选择器 | CategorySelect.vue (下拉选择) | src/components/categories/CategorySelect.vue | P1 | 待开发 |
| T-272 | 分类编辑弹窗 | CategoryModal.vue | src/components/categories/CategoryModal.vue | P1 | 待开发 |

#### 3.4.3 标签组件

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-280 | 标签展示 | Tag.vue | src/components/tags/Tag.vue | P0 | 待开发 |
| T-281 | 标签选择器 | TagSelect.vue (多选) | src/components/tags/TagSelect.vue | P0 | 待开发 |
| T-282 | 标签输入 | TagInput.vue (创建新标签) | src/components/tags/TagInput.vue | P1 | 待开发 |

#### 3.4.4 图谱组件

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-290 | 图谱画布 | GraphCanvas.vue (D3.js) | src/components/graph/GraphCanvas.vue | P1 | 待开发 |
| T-291 | 图谱节点 | GraphNode.vue | src/components/graph/GraphNode.vue | P1 | 待开发 |
| T-292 | 图谱控制 | GraphControls.vue | src/components/graph/GraphControls.vue | P2 | 待开发 |
| T-293 | 图谱图例 | GraphLegend.vue | src/components/graph/GraphLegend.vue | P2 | 待开发 |

#### 3.4.5 笔记组件

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-300 | 笔记卡片 | NoteCard.vue | src/components/notes/NoteCard.vue | P0 | 待开发 |
| T-301 | 笔记列表 | NoteList.vue | src/components/notes/NoteList.vue | P0 | 待开发 |
| T-302 | 笔记网格 | NoteGrid.vue | src/components/notes/NoteGrid.vue | P1 | 待开发 |
| T-303 | 搜索栏 | NoteSearch.vue | src/components/notes/NoteSearch.vue | P1 | 待开发 |

---

### 3.5 页面组件

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-310 | 登录页面 | Login.vue | src/pages/Login.vue | P0 | 待开发 |
| T-311 | 注册页面 | Register.vue | src/pages/Register.vue | P0 | 待开发 |
| T-312 | 首页/仪表盘 | Home.vue | src/pages/Home.vue | P0 | 待开发 |
| T-313 | 笔记列表页 | NoteList.vue | src/pages/notes/NoteList.vue | P0 | 待开发 |
| T-314 | 笔记详情页 | NoteDetail.vue | src/pages/notes/NoteDetail.vue | P0 | 待开发 |
| T-315 | 笔记编辑页 | NoteEditor.vue | src/pages/notes/NoteEditor.vue | P0 | 待开发 |
| T-316 | 分类管理页 | CategoryList.vue | src/pages/categories/CategoryList.vue | P0 | 待开发 |
| T-317 | 标签管理页 | TagList.vue | src/pages/tags/TagList.vue | P0 | 待开发 |
| T-318 | 知识图谱页 | GraphView.vue | src/pages/graph/GraphView.vue | P1 | 待开发 |
| T-319 | 收藏列表页 | CollectionList.vue | src/pages/collections/CollectionList.vue | P1 | 待开发 |
| T-320 | 收藏详情页 | CollectionDetail.vue | src/pages/collections/CollectionDetail.vue | P1 | 待开发 |
| T-321 | 添加收藏页 | CollectionAdd.vue | src/pages/collections/CollectionAdd.vue | P1 | 待开发 |
| T-322 | 设置页面 | Settings.vue | src/pages/settings/Settings.vue | P2 | 待开发 |

---

### 3.6 组合式函数 (Composables)

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-330 | 认证逻辑 | useAuth.ts | src/composables/useAuth.ts | P0 | 待开发 |
| T-331 | 笔记操作 | useNotes.ts | src/composables/useNotes.ts | P0 | 待开发 |
| T-332 | 分类操作 | useCategories.ts | src/composables/useCategories.ts | P0 | 待开发 |
| T-333 | 标签操作 | useTags.ts | src/composables/useTags.ts | P0 | 待开发 |
| T-334 | 图谱操作 | useGraph.ts | src/composables/useGraph.ts | P1 | 待开发 |
| T-335 | 模态框控制 | useModal.ts | src/composables/useModal.ts | P1 | 待开发 |
| T-336 | 本地存储 | useStorage.ts | src/composables/useStorage.ts | P1 | 待开发 |

---

## 四、样式与主题

### 4.1 全局样式

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-400 | 全局 CSS 变量 | variables.scss (颜色、间距) | src/styles/variables.scss | P0 | 待开发 |
| T-401 | 全局重置样式 | reset.scss | src/styles/reset.scss | P0 | 待开发 |
| T-402 | 工具类 | utility.scss | src/styles/utility.scss | P1 | 待开发 |
| T-403 | 动画样式 | animations.scss | src/styles/animations.scss | P2 | 待开发 |

### 4.2 主题支持

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-410 | 亮色主题 | light theme | src/styles/themes/light.scss | P1 | 待开发 |
| T-411 | 暗色主题 | dark theme | src/styles/themes/dark.scss | P1 | 待开发 |
| T-412 | 主题切换 | 主题切换逻辑 | src/composables/useTheme.ts | P1 | 待开发 |

---

## 五、测试任务

### 5.1 后端测试

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-500 | 用户模块测试 | test_users.py | tests/test_users.py | P1 | 待开发 |
| T-501 | 分类模块测试 | test_categories.py | tests/test_categories.py | P1 | 待开发 |
| T-502 | 标签模块测试 | test_tags.py | tests/test_tags.py | P1 | 待开发 |
| T-503 | 笔记模块测试 | test_notes.py | tests/test_notes.py | P1 | 待开发 |
| T-504 | API 集成测试 | test_api.py | tests/test_api.py | P1 | 待开发 |

### 5.2 前端测试

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-510 | Store 单元测试 | stores 测试 | tests/unit/stores.spec.ts | P2 | 待开发 |
| T-511 | 组件单元测试 | 基础组件测试 | tests/unit/components.spec.ts | P2 | 待开发 |
| T-512 | E2E 测试 | Cypress 配置 | tests/e2e/ | P2 | 待开发 |

---

## 六、部署任务

### 6.1 Docker 部署

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-600 | 后端 Dockerfile | Dockerfile.backend | Dockerfile.backend | P1 | 待开发 |
| T-601 | 前端 Dockerfile | Dockerfile.frontend | Dockerfile.frontend | P1 | 待开发 |
| T-602 | Docker Compose | docker-compose.yml | docker-compose.yml | P1 | 待开发 |
| T-603 | Nginx 配置 | nginx.conf | nginx.conf | P1 | 待开发 |

### 6.2 CI/CD

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-610 | GitHub Actions | CI 配置文件 | .github/workflows/ci.yml | P2 | 待开发 |
| T-611 | 部署脚本 | deploy.sh | scripts/deploy.sh | P2 | 待开发 |

---

## 七、文档任务

| 任务ID | 任务名称 | 描述 | 文件路径 | 优先级 | 状态 |
|--------|----------|------|----------|--------|------|
| T-700 | API 文档 | OpenAPI/Swagger | docs/api.md | P1 | 待开发 |
| T-701 | 部署文档 | 部署指南 | docs/deployment.md | P1 | 待开发 |
| T-702 | 数据库设计 | 数据库 ER 图 | docs/database.md | P1 | 待开发 |

---

## 任务统计

| 阶段 | 任务数量 | P0 优先级 | P1 优先级 | P2 优先级 |
|------|----------|-----------|-----------|-----------|
| 项目初始化 | 14 | 9 | 5 | 0 |
| 后端开发 | 98 | 36 | 52 | 10 |
| 前端开发 | 133 | 43 | 72 | 18 |
| 样式与主题 | 13 | 2 | 8 | 3 |
| 测试 | 13 | 0 | 10 | 3 |
| 部署 | 8 | 0 | 6 | 2 |
| 文档 | 3 | 0 | 3 | 0 |
| **总计** | **282** | **90** | **156** | **36** |

---

## 开发顺序建议

### Phase 1: 基础设施 (2-3天)

1. 项目初始化
2. 后端公共模块
3. 前端基础架构
4. 用户认证模块

### Phase 2: 核心功能 (1周)

1. 分类管理
2. 标签管理
3. 笔记 CRUD
4. 笔记编辑器

### Phase 3: 扩展功能 (5天)

1. 知识图谱
2. 内容收藏
3. 附件管理

### Phase 4: 前端完善 (1周)

1. 页面开发
2. 组件封装
3. 状态管理

### Phase 5: 测试与部署 (3天)

1. 单元测试
2. Docker 部署
3. 文档编写

---

## 优先级说明

| 优先级 | 说明 |
|--------|------|
| P0 | 核心功能，必须完成 |
| P1 | 重要功能，建议完成 |
| P2 | 可选功能，可以延后 |

---

## 状态说明

| 状态 | 说明 |
|------|------|
| 待开发 | 尚未开始 |
| 进行中 | 正在开发 |
| 待Review | 待代码审查 |
| 已完成 | 已完成开发 |

---

## 任务完成标准

### P0 任务
- 代码完整无语法错误
- 单元测试覆盖率 >= 80%
- 代码审查通过

### P1 任务
- 代码完整无语法错误
- 基础功能测试通过

### P2 任务
- 代码完整
- 可手动测试通过
