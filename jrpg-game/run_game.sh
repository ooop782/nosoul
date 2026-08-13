#!/bin/bash

echo "正在啟動日式 RPG 遊戲..."
python3 src/main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[錯誤] 遊戲運行失敗"
    echo "請確認已正確安裝所有依賴套件"
    echo "運行 ./install.sh 進行安裝"
fi
