# 项目初始化决策记录

## [2026-01-25] 架构决策

### 目录结构决策
- 采用 mono-repo 模式：backend/ 和 frontend/ 并列
- 后端使用标准 Django 结构
- 前端使用 Vite + Vue3 + TypeScript

### Git 分支策略
- main: 主分支，生产就绪
- develop: 开发分支
- feature/*: 功能分支
- release/*: 发布分支

### 开发环境配置
- Python 3.12+
- Node.js 20+
- PostgreSQL 17
