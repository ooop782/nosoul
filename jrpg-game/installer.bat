@echo off
chcp 65001 > nul
echo ==========================================
echo    日式 RPG 冒險 - Windows 安裝程式
echo ==========================================
echo.

:: 檢查 Python
python --version > nul 2>&1
if errorlevel 1 (
    echo 錯誤：未找到 Python，請先安裝 Python 3.x
    echo 請前往 https://www.python.org/downloads/ 下載
    pause
    exit /b 1
)

echo ✓ 檢測到 Python: 
python --version

:: 安裝依賴
echo.
echo 正在安裝遊戲依賴...
pip install pygame numpy --quiet

if errorlevel 1 (
    echo ✗ 依賴安裝失敗
    pause
    exit /b 1
)

echo ✓ 依賴安裝完成

:: 創建啟動腳本
echo.
echo 正在創建啟動腳本...

(
echo @echo off
echo chcp 65001 ^> nul
echo cd /d "%%~dp0"
echo python src/main.py
echo pause
) > play_jrpg.bat

echo ✓ 啟動腳本已創建

:: 創建桌面捷徑
echo.
echo 正在創建桌面捷徑...

set SCRIPT_PATH=%cd%\play_jrpg.bat
set DESKTOP=%USERPROFILE%\Desktop

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\JRPG_Adventure.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%SCRIPT_PATH%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%cd%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "日式RPG冒險" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

cscript //nologo "%TEMP%\CreateShortcut.vbs"
del "%TEMP%\CreateShortcut.vbs"

echo ✓ 桌面捷徑已創建

echo.
echo ==========================================
echo    安裝完成！
echo ==========================================
echo.
echo 啟動方式：
echo   1. 雙擊 play_jrpg.bat
echo   2. 或點擊桌面上的 JRPG_Adventure 捷徑
echo.
echo 遊戲控制：
echo   - 方向鍵/WASD: 移動
echo   - Z/Space: 確認/互動
echo   - ESC: 返回標題
echo.
pause
