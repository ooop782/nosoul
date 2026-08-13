#!/bin/bash

echo "========================================"
echo "日式 RPG 遊戲快速安裝程式 (Linux/Mac)"
echo "========================================"
echo ""

# 檢查 Python 是否已安裝
if ! command -v python3 &> /dev/null; then
    echo "[錯誤] 未找到 Python3，請先安裝 Python 3.8 或以上版本"
    exit 1
fi

echo "[✓] Python 已安裝"
python3 --version
echo ""

# 安裝依賴套件
echo "[正在安裝] 遊戲依賴套件..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[錯誤] 依賴套件安裝失敗"
    exit 1
fi

echo ""
echo "[✓] 所有套件安裝成功！"
echo ""
echo "========================================"
echo "安裝完成！"
echo "========================================"
echo ""
echo "要運行遊戲，請執行："
echo "  python3 src/main.py"
echo ""
echo "或運行 ./run_game.sh"
echo ""
