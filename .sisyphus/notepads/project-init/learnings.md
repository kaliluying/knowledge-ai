# 项目初始化学习记录

## [2026-01-25] 项目开始

### 初始化策略
- 遵循 TASK.md 中的开发顺序建议
- 从 Phase 1 基础设施开始
- 先创建目录结构，再初始化 Git，最后配置环境

### 技术选型确认
- 后端: Django 5.2 + DRF + PostgreSQL 17 + uv
- 前端: Vue 3 + Vite + Pinia + TypeScript
- 编辑器: TipTap
- 可视化: D3.js
- 部署: Docker + Nginx

### Python 环境策略
- 使用 uv 作为包管理器（比 pip 快 10-100 倍）
- Windows 安装: `winget install astral-sh.uv`
- 创建独立虚拟环境

## [2026-01-25] Phase 2 完成

### 完成的任务
- Phase 1 基础设施 ✓
- Phase 2 后端公共模块:
  - T-020: utils/responses.py 统一响应格式 ✓
  - T-021: utils/permissions.py 自定义权限类 ✓
  - T-022: utils/pagination.py 分页器 ✓
  - T-023: utils/exceptions.py 异常处理器 ✓
  - T-024: utils/helpers.py 工具函数集 ✓
  - T-025: config/settings.py Django配置 ✓
  - T-026: config/urls.py 主路由配置 ✓
  - T-027: config/wsgi.py WSGI配置 ✓
  - T-028: config/rest_framework.py DRF配置 ✓
- Django check 通过 ✓
- User 模型创建 ✓

### 关键发现
- django-mptt 包名是 `mptt` 不是 `django_mptt`
- uv 和 pip 需要使用正确的 Python 路径
- Django 6.0.1 降级到 5.2.10 以兼容 requirements.txt
- 需要为每个 app 创建 urls.py 即使是空的
