@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo  ╔══════════════════════════════════════╗
echo  ║     WexOpen  构建脚本                ║
echo  ╚══════════════════════════════════════╝
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python
    pause & exit /b 1
)

echo [1/4] 安装构建依赖…
pip install -r requirements-build.txt -q

echo [2/4] 生成应用图标…
python scripts\generate_icon.py
if errorlevel 1 pause & exit /b 1

echo [3/4] PyInstaller 打包…
pyinstaller WexOpen.spec --noconfirm
if errorlevel 1 (
    echo [错误] PyInstaller 打包失败
    pause & exit /b 1
)

echo       免安装版: dist\WexOpen-Portable.exe

echo [4/4] 构建安装程序…
set "ISCC="
for %%P in (
    "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    "C:\Program Files\Inno Setup 6\ISCC.exe"
) do if exist %%P set "ISCC=%%~P"

if defined ISCC (
    "!ISCC!" installer\WexOpen.iss
    if errorlevel 1 (
        echo [警告] 安装程序构建失败
    ) else (
        echo       安装版:   dist\installer\WexOpen-Setup.exe
    )
) else (
  echo [跳过] 未安装 Inno Setup，仅生成免安装版
    echo        安装 Inno Setup 6 后重新运行 build.bat 即可生成安装包
)

echo.
echo  ══════════════════════════════════════
echo   构建完成！输出目录: dist\
echo  ══════════════════════════════════════
echo.
pause
