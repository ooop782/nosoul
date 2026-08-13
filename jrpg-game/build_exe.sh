#!/bin/bash

echo "========================================"
echo "日式 RPG 遊戲 - 打包成可執行文件"
echo "========================================"
echo ""

# 檢查 PyInstaller 是否已安裝
if ! python3 -m pip show pyinstaller &> /dev/null; then
    echo "[正在安裝] PyInstaller..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        echo "[錯誤] PyInstaller 安裝失敗"
        exit 1
    fi
fi

echo "[✓] PyInstaller 已安裝"
echo ""

# 清理舊的打包文件
if [ -d "build" ]; then
    echo "[清理] 刪除舊的構建文件..."
    rm -rf build
fi
if [ -d "dist" ]; then
    rm -rf dist
fi

echo "[打包中] 正在創建可執行文件，請稍候..."
echo ""

# 使用 PyInstaller 打包
pyinstaller --onefile \
            --windowed \
            --name "JRPG_Adventure" \
            --add-data "src:src" \
            --hidden-import pygame \
            --hidden-import numpy \
            --hidden-import pygame.sndarray \
            run.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[錯誤] 打包失敗"
    exit 1
fi

echo ""
echo "========================================"
echo "打包完成！"
echo "========================================"
echo ""
echo "可執行文件位於：dist/JRPG_Adventure"
echo ""
