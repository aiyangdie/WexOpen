@echo off
chcp 65001 >nul
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
    echo 未找到 Python，请先安装 Python 3.10+
    echo 下载：https://www.python.org/downloads/
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo 首次运行，正在安装依赖…
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt -q
) else (
    call .venv\Scripts\activate.bat
)

python main.py
