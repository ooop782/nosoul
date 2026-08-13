#!/usr/bin/env python3
"""
日式 RPG 遊戲 - 可執行啟動器
此腳本可以打包成 .exe 文件
"""

import sys
import os

# 添加 src 目錄到路徑
src_dir = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_dir)

# 導入並運行遊戲
from main import main

if __name__ == "__main__":
    main()
