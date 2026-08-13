#!/bin/bash
# 日式RPG遊戲安裝程式 (Linux/Mac)

echo "=========================================="
echo "   日式RPG冒險 - 安裝程式"
echo "=========================================="
echo ""

# 檢查Python
if ! command -v python3 &> /dev/null; then
    echo "錯誤：未找到 Python3，請先安裝 Python3"
    exit 1
fi

echo "✓ 檢測到 Python: $(python3 --version)"

# 安裝依賴
echo ""
echo "正在安裝遊戲依賴..."
pip3 install pygame numpy --quiet

if [ $? -eq 0 ]; then
    echo "✓ 依賴安裝完成"
else
    echo "✗ 依賴安裝失敗"
    exit 1
fi

# 創建啟動腳本
echo ""
echo "正在創建啟動腳本..."

cat > play_jrpg.sh << 'INNER_EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 src/main.py
INNER_EOF

chmod +x play_jrpg.sh
echo "✓ 啟動腳本已創建"

# 創建桌面捷徑（如果可能）
if [ -d "$HOME/Desktop" ]; then
    cat > "$HOME/Desktop/JRPG_Adventure.desktop" << DESKTOP_EOF
[Desktop Entry]
Name=日式RPG冒險
Exec=$(pwd)/play_jrpg.sh
Icon=
Type=Application
Categories=Game;
DESKTOP_EOF
    chmod +x "$HOME/Desktop/JRPG_Adventure.desktop"
    echo "✓ 桌面捷徑已創建"
fi

echo ""
echo "=========================================="
echo "   安裝完成！"
echo "=========================================="
echo ""
echo "啟動方式："
echo "  1. 雙擊 play_jrpg.sh"
echo "  2. 或在終端運行：./play_jrpg.sh"
echo ""
echo "遊戲控制："
echo "  - 方向鍵/WASD: 移動"
echo "  - Z/Space: 確認/互動"
echo "  - ESC: 返回標題"
echo ""
