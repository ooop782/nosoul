"""
日式RPG遊戲安裝程式
此腳本將協助您安裝並運行遊戲
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
import shutil

class Installer:
    def __init__(self):
        self.game_dir = os.path.dirname(os.path.abspath(__file__))
        self.requirements_file = os.path.join(self.game_dir, "requirements.txt")
        
    def check_python(self):
        """檢查Python是否已安裝"""
        try:
            result = subprocess.run([sys.executable, "--version"], 
                                  capture_output=True, text=True)
            return True, result.stdout.strip()
        except Exception as e:
            return False, str(e)
    
    def install_dependencies(self):
        """安裝必要的依賴套件"""
        print("正在安裝依賴套件...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", 
                                 self.requirements_file])
            print("依賴套件安裝成功！")
            return True
        except subprocess.CalledProcessError as e:
            print(f"安裝失敗：{e}")
            return False
        except Exception as e:
            print(f"發生錯誤：{e}")
            return False
    
    def verify_installation(self):
        """驗證安裝是否成功"""
        try:
            import pygame
            print(f"Pygame 版本：{pygame.__version__}")
            return True
        except ImportError as e:
            print(f"無法導入 pygame：{e}")
            return False
    
    def create_shortcut(self):
        """創建桌面捷徑（Windows）"""
        if sys.platform == 'win32':
            try:
                import pyshortcuts
                # 這需要額外安裝 pyshortcuts
                print("注意：如需創建桌面捷徑，請安裝 pyshortcuts 套件")
            except ImportError:
                print("提示：安裝 pyshortcuts 可創建桌面捷徑")
    
    def run_game(self):
        """運行遊戲"""
        main_script = os.path.join(self.game_dir, "src", "main.py")
        if os.path.exists(main_script):
            try:
                subprocess.run([sys.executable, main_script])
            except Exception as e:
                print(f"運行遊戲時出錯：{e}")
        else:
            print(f"找不到遊戲主程式：{main_script}")

def main():
    installer = Installer()
    
    print("=" * 50)
    print("日式RPG遊戲安裝程式")
    print("=" * 50)
    
    # 檢查 Python
    python_ok, python_info = installer.check_python()
    if not python_ok:
        messagebox.showerror("錯誤", f"未找到 Python 環境：{python_info}")
        return
    
    print(f"✓ Python 環境：{python_info}")
    
    # 安裝依賴
    if not installer.verify_installation():
        choice = messagebox.askyesno("安裝依賴", 
                                    "需要安裝 pygame 套件，是否繼續？")
        if choice:
            if not installer.install_dependencies():
                messagebox.showerror("錯誤", "依賴套件安裝失敗")
                return
        else:
            messagebox.showwarning("警告", "遊戲可能無法運行")
    
    # 驗證安裝
    if installer.verify_installation():
        print("✓ 所有依賴已正確安裝")
        messagebox.showinfo("成功", "安裝完成！\n現在可以運行遊戲了。")
        
        # 詢問是否立即運行
        run_choice = messagebox.askyesno("運行遊戲", "是否立即運行遊戲？")
        if run_choice:
            installer.run_game()
    else:
        messagebox.showerror("錯誤", "安裝驗證失敗，請手動安裝 requirements.txt 中的套件")

if __name__ == "__main__":
    main()
