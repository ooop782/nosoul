# 日式 RPG 冒險遊戲

一款使用 Python 和 Pygame 開發的日式角色扮演遊戲，所有遊戲資源均為程式生成或使用無版權素材。

## 遊戲特色

- 🎮 經典日式 RPG 玩法
- 🗺️ 程序生成的開放世界地圖
- ⚔️ 回合制戰鬥系統
- 📈 角色升級與成長系統
- 🎨 所有圖形均為程式生成（無版權問題）
- 🎵 合成音效（無版權問題）

## 系統需求

- Python 3.8 或更高版本
- Windows / macOS / Linux
- 至少 50MB 可用空間

## 快速安裝

### Windows 用戶

**方法一：使用安裝腳本（推薦）**

1. **雙擊運行** `install.bat` 進行自動安裝
2. 安裝完成後，**雙擊** `run_game.bat` 啟動遊戲

**方法二：手動安裝**

```bash
pip install -r requirements.txt
python src\main.py
```

**方法三：打包成 EXE 可執行文件**

如需創建獨立的 .exe 文件（無需安裝 Python）：

1. 運行 `build_exe.bat`
2. 在 `dist` 目錄中找到 `JRPG_Adventure.exe`
3. 雙擊即可運行遊戲

### Linux / Mac 用戶

```bash
chmod +x install.sh run_game.sh
./install.sh
./run_game.sh
```

或手動安裝：
```bash
pip3 install -r requirements.txt
python3 src/main.py
```

**打包成可執行文件：**
```bash
chmod +x build_exe.sh
./build_exe.sh
# 可執行文件位於 dist/JRPG_Adventure
```

## 遊戲操作

| 按鍵 | 功能 |
|------|------|
| ↑ ↓ ← → 或 W A S D | 移動角色 |
| Z 或 Space | 確認/互動/開始遊戲 |
| ESC | 返回標題畫面 |

### 戰鬥操作

- 進入戰鬥後按 **Z** 或 **Space** 選擇攻擊
- 再次按 **Z** 或 **Space** 選擇目標並執行攻擊
- 擊敗敵人獲得經驗值升級

## 遊戲說明

1. **標題畫面**: 按 Z 或 Space 開始新遊戲
2. **探索**: 使用方向鍵在地圖上移動
3. **遇敵**: 移動時有機率隨機遭遇敵人
4. **戰鬥**: 回合制戰鬥，選擇攻擊擊敗敵人
5. **升級**: 獲得足夠經驗值後自動升級，提升屬性
6. **遊戲結束**: HP 歸零時遊戲結束，可返回標題重新開始

## 技術特點

- **純程式生成資源**: 所有圖形、音效均由程式碼實時生成，無需外部素材文件
- **跨平台**: 支援 Windows、macOS、Linux
- **輕量級**: 安裝簡單，依賴少
- **開源友好**: 使用標準 Pygame 庫

## 檔案結構

```
jrpg-game/
├── src/
│   └── main.py          # 遊戲主程式
├── assets/              # 資源目錄（本遊戲使用程式生成，此目錄為空）
│   ├── music/
│   ├── images/
│   └── fonts/
├── install.bat          # Windows 安裝腳本
├── install.sh           # Linux/Mac 安裝腳本
├── run_game.bat         # Windows 運行腳本
├── run_game.sh          # Linux/Mac 運行腳本
├── install.py           # Python 安裝程式
├── requirements.txt     # Python 依賴列表
└── README.md            # 本文件
```

## 依賴套件

- **pygame** >= 2.5.0 - 遊戲引擎
- **numpy** >= 1.24.0 - 數值計算（用於音效生成）

## 常見問題

### Q: 遊戲無法啟動？
A: 請確認已正確安裝 Python 和所有依賴套件。運行 `install.bat` (Windows) 或 `install.sh` (Linux/Mac) 進行安裝。

### Q: 沒有聲音？
A: 遊戲使用程式生成的合成音效，某些系統可能需要額外配置音頻驅動。

### Q: 如何退出遊戲？
A: 按 ESC 返回標題畫面，然後關閉視窗即可。

## 授權說明

本遊戲所有資源均為：
- 程式代碼生成的圖形和音效
- 或使用無版權（Royalty-Free）素材
- 可自由修改和分發

遊戲代碼採用 MIT 授權條款。

## 開發者註記

這是一個示範性質的日式 RPG 遊戲框架，展示了如何使用 Pygame 創建基本的 RPG 元素，包括：
- 地圖系統
- 角色移動
- 碰撞檢測
- 戰鬥系統
- 經驗值和升級機制

歡迎在此基礎上擴展更多功能！

---

**享受你的冒險旅程！** 🗡️🛡️✨
