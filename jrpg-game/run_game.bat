@echo off
echo 正在啟動日式 RPG 遊戲...
python src\main.py
if %errorlevel% neq 0 (
    echo.
    echo [錯誤] 遊戲運行失敗
    echo 請確認已正確安裝所有依賴套件
    echo 運行 install.bat 進行安裝
    pause
)
