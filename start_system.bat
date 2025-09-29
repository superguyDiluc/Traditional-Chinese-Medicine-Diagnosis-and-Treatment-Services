@echo off
echo 启动中医 AI 系统...
echo.

echo 安装 Python 依赖包...
pip install flask flask-cors dashscope

echo.
echo 启动后端服务 (端口 5000)...
start "TCM AI Backend" cmd /k "python ai_backend.py"

echo.
echo 等待后端服务启动...
timeout /t 3 /nobreak >nul

echo.
echo 启动前端服务 (端口 8000)...
start "TCM Frontend" cmd /k "python -m http.server 8000"

echo.
echo 系统启动完成！
echo.
echo 后端 API: http://localhost:5000
echo 前端界面: http://localhost:8000
echo.
echo 按任意键关闭此窗口...
pause >nul