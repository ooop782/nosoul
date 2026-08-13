# 日式 RPG 冒險 - 安裝說明

## 遊戲特色
- ✅ 完全使用無版權資源（所有圖標、音樂均為程式生成）
- ✅ 經典日式 RPG 玩法
- ✅ 隨機生成的地圖
- ✅ 戰鬥系統
- ✅ NPC 對話系統
- ✅ 升級系統

## 快速安裝

### Windows 用戶
1. **方法一：使用安裝程式（推薦）**
   - 雙擊 `installer.bat`
   - 按照提示完成安裝
   - 安裝完成後，桌面會出現捷徑，或執行 `play_jrpg.bat`

2. **方法二：直接執行已編譯的 EXE**
   - 進入 `dist` 資料夾
   - 雙擊 `JRPG_Adventure.exe`（需要從 Linux 重新編譯為 Windows 版本）

3. **方法三：手動安裝**
   ```cmd
   pip install pygame numpy
   python src/main.py
   ```

### Linux/Mac 用戶
1. **使用安裝腳本（推薦）**
   ```bash
   chmod +x installer.sh
   ./installer.sh
   ```
   安裝完成後執行：
   ```bash
   ./play_jrpg.sh
   ```

2. **手動安裝**
   ```bash
   pip install pygame numpy pillow
   python src/main.py
   ```

## 遊戲控制
- **方向鍵** 或 **WASD**: 移動角色
- **Z 鍵** 或 **空白鍵**: 確認/互動/開始遊戲
- **ESC**: 返回標題畫面

## 檔案結構
```
jrpg-game/
├── src/                # 遊戲原始碼
│   └── main.py        # 主遊戲程式
├── assets/            # 遊戲資源
│   ├── icon.png       # 遊戲圖標（程式生成）
│   ├── tileset.png    # 地圖圖塊（程式生成）
│   ├── images/        # 圖片資源
│   └── music/         # 音樂資源（程式生成）
│       ├── bgm_title.wav      # 背景音樂
│       ├── sfx_attack.wav     # 攻擊音效
│       ├── sfx_hit.wav        # 受擊音效
│       └── sfx_levelup.wav    # 升級音效
├── dist/              # 編譯後的執行檔
│   └── JRPG_Adventure # Linux 可執行檔
├── installer.bat      # Windows 安裝程式
├── installer.sh       # Linux/Mac 安裝程式
├── generate_assets.py # 資源生成器
└── README_安裝說明.md  # 本文件
```

## 注意事項
1. 所有遊戲資源（圖片、音樂）都是使用程式自動生成的，完全無版權問題，可以自由使用和修改。
2. 如果需要 Windows 的 .exe 執行檔，需要在 Windows 系統上使用 PyInstaller 重新編譯：
   ```cmd
   pip install pyinstaller pygame numpy
   pyinstaller --onefile --windowed --name="JRPG_Adventure" src/main.py
   ```
3. 遊戲需要 Python 3.x 和 Pygame 庫才能運行。

## 授權聲明
本遊戲所有資源均為程式生成，屬於公共領域（Public Domain），無版權限制，可自由使用、修改和分發。

祝您遊戲愉快！
