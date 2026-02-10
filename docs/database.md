# 数据库设计文档

## 概览
数据库使用 PostgreSQL 17，核心业务围绕用户、笔记、分类、标签、图谱、收藏与附件。

## 主要实体

### users_user
- 用户基础信息
- 关键字段: `id`, `username`, `email`, `password`, `avatar`, `bio`, `created_at`

### notes_note
- 笔记主体
- 关键字段: `id`, `title`, `slug`, `content`, `plain_text`, `owner_id`, `category_id`, `is_pinned`, `is_archived`, `view_count`, `created_at`, `updated_at`
- 索引: `(owner, created_at)`, `(owner, is_archived)`, `(owner, is_pinned)`

### categories_category
- 分类树结构
- 关键字段: `id`, `name`, `slug`, `owner_id`, `parent_id`, `color`

### tags_tag
- 标签
- 关键字段: `id`, `name`, `slug`, `owner_id`, `color`

### graph_graphnode
- 图谱节点
- 关键字段: `id`, `owner_id`, `node_type`, `title`, `label`, `data`, `created_at`

### graph_graphlink
- 图谱链接
- 关键字段: `id`, `owner_id`, `source_id`, `target_id`, `link_type`, `weight`, `created_at`

### collections_collection
- 收藏内容
- 关键字段: `id`, `owner_id`, `url`, `title`, `description`, `content`, `is_processed`, `created_at`

### attachments_attachment
- 附件信息
- 关键字段: `id`, `owner_id`, `file`, `file_type`, `file_size`, `created_at`

## 关系说明
- 一个用户拥有多个笔记、分类、标签、收藏、附件、图谱节点和图谱链接。
- 笔记与标签是多对多关系。
- 笔记与分类是多对一关系（可为空）。
- 图谱链接通过 `source_id` 和 `target_id` 连接图谱节点。

## 迁移与初始化

```bash
cd backend
uv run python manage.py migrate
```
