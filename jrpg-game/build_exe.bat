@echo off
echo ========================================
echo 日式 RPG 遊戲 - 打包成 EXE
echo ========================================
echo.

REM 檢查 PyInstaller 是否已安裝
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [正在安裝] PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo [錯誤] PyInstaller 安裝失敗
        pause
        exit /b 1
    )
)

echo [✓] PyInstaller 已安裝
echo.

REM 清理舊的打包文件
if exist build (
    echo [清理] 刪除舊的構建文件...
    rmdir /s /q build
)
if exist dist (
    rmdir /s /q dist
)

echo [打包中] 正在創建可執行文件，請稍候...
echo.

REM 使用 PyInstaller 打包
pyinstaller --onefile ^
            --windowed ^
            --name "JRPG_Adventure" ^
            --add-data "src;src" ^
            --hidden-import pygame ^
            --hidden-import numpy ^
            --hidden-import pygame.sndarray ^
            run.py

if %errorlevel% neq 0 (
    echo.
    echo [錯誤] 打包失敗
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 可執行文件位於：dist\JRPG_Adventure.exe
echo.
echo 注意：由於遊戲包含中文字符，在某些系統上可能需要額外配置
echo 建議在目標系統上先測試運行
echo.
pause
