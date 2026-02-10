# API 文档

## 基础信息
- Base URL: `/api`
- 响应格式: `{ code, message, data }`
- 认证方式: `Authorization: Bearer <access_token>`

## 认证模块
- `POST /api/auth/register/` 用户注册
- `POST /api/auth/login/` 用户登录
- `POST /api/auth/logout/` 用户登出
- `POST /api/auth/refresh/` 刷新 token
- `GET /api/auth/profile/` 获取当前用户
- `PUT /api/auth/profile/` 更新当前用户
- `POST /api/auth/password/change/` 修改密码

## 笔记模块
- `GET /api/notes/` 笔记列表
- `POST /api/notes/` 创建笔记
- `GET /api/notes/{id}/` 笔记详情
- `PUT /api/notes/{id}/` 更新笔记
- `DELETE /api/notes/{id}/` 删除笔记
- `POST /api/notes/{id}/archive/` 归档
- `POST /api/notes/{id}/unarchive/` 取消归档
- `GET /api/notes/search/` 搜索
- `GET /api/notes/recent/` 最近笔记

## 分类模块
- `GET /api/categories/` 分类列表
- `POST /api/categories/` 创建分类
- `GET /api/categories/{id}/` 分类详情
- `PUT /api/categories/{id}/` 更新分类
- `DELETE /api/categories/{id}/` 删除分类
- `GET /api/categories/tree/` 分类树

## 标签模块
- `GET /api/tags/` 标签列表
- `POST /api/tags/` 创建标签
- `PUT /api/tags/{id}/` 更新标签
- `DELETE /api/tags/{id}/` 删除标签

## 图谱模块
- `GET /api/graph/graph/` 图谱数据
- `GET /api/graph/related/{id}/` 相关节点
- `POST /api/graph/links/` 创建链接
- `DELETE /api/graph/links/{id}/` 删除链接

## 收藏模块
- `GET /api/collections/` 收藏列表
- `POST /api/collections/` 创建收藏
- `GET /api/collections/{id}/` 收藏详情
- `PUT /api/collections/{id}/` 更新收藏
- `DELETE /api/collections/{id}/` 删除收藏

## 附件模块
- `GET /api/attachments/` 附件列表
- `POST /api/attachments/` 上传附件
- `DELETE /api/attachments/{id}/` 删除附件
