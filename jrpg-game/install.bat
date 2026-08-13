@echo off
echo ========================================
echo 日式 RPG 遊戲快速安裝程式
echo ========================================
echo.

REM 檢查 Python 是否已安裝
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [錯誤] 未找到 Python，請先安裝 Python 3.8 或以上版本
    echo 下載網址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [✓] Python 已安裝
python --version
echo.

REM 安裝依賴套件
echo [正在安裝] 遊戲依賴套件...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [錯誤] 依賴套件安裝失敗
    pause
    exit /b 1
)

echo.
echo [✓] 所有套件安裝成功！
echo.
echo ========================================
echo 安裝完成！
echo ========================================
echo.
echo 要運行遊戲，請執行：
echo   python src\main.py
echo.
echo 或雙擊 run_game.bat
echo.
pause
