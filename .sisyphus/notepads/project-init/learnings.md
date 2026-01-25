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
