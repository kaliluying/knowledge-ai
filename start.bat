@echo off
chcp 65001 >nul
echo ========================================
echo Personal Knowledge Management System
echo ========================================
echo.

cd %~dp0

echo [1/3] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.12+
    pause
    exit /b 1
)

echo [2/3] 启动后端服务 (Django)...
cd backend
start "Django Server" cmd /c "python manage.py runserver"

echo.
echo [3/3] 启动前端服务 (Vue)...
cd ..\frontend
start "Vue Server" cmd /c "npm run dev"

echo.
echo ========================================
echo 服务启动中...
echo - 后端 API: http://localhost:8000
echo - 前端页面: http://localhost:5173
echo - API 文档: http://localhost:8000/api
echo ========================================
echo.
echo 按任意键停止所有服务...
pause >nul

taskkill /FI "WindowTitle eq Django Server" >nul 2>&1
taskkill /FI "WindowTitle eq Vue Server" >nul 2>&1

echo 服务已停止。
