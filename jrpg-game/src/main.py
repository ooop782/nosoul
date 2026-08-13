"""
日式RPG遊戲 - 主要遊戲引擎
使用 Pygame 開發
所有資源均為無版權或程式生成
"""

import pygame
import sys
import random
import math
from enum import Enum

# 初始化 Pygame
pygame.init()

# 初始化音效（處理無音效設備的情況）
try:
    pygame.mixer.init()
    AUDIO_AVAILABLE = True
except pygame.error:
    AUDIO_AVAILABLE = False
    print("注意：音效設備不可用，遊戲將在無聲音模式下運行")

# 遊戲常數
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 32

# 顏色定義
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'purple': (128, 0, 128),
    'cyan': (0, 255, 255),
    'orange': (255, 165, 0),
    'brown': (139, 69, 19),
    'gray': (128, 128, 128),
    'dark_green': (0, 100, 0),
    'light_blue': (173, 216, 230),
    'sand': (244, 164, 96),
    'water': (30, 144, 255),
    'grass': (34, 139, 34),
    'gold': (255, 215, 0),
}

class GameState(Enum):
    TITLE = 1
    PLAYING = 2
    BATTLE = 3
    DIALOGUE = 4
    GAME_OVER = 5

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Character:
    def __init__(self, x, y, name, color, speed=3):
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.speed = speed
        self.direction = Direction.DOWN
        self.is_moving = False
        self.hp = 100
        self.max_hp = 100
        self.mp = 50
        self.max_mp = 50
        self.level = 1
        self.exp = 0
        self.attack = 10
        self.defense = 5
        
    def move(self, dx, dy, map_data):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # 檢查邊界
        if new_x < 0 or new_x >= SCREEN_WIDTH - TILE_SIZE:
            return False
        if new_y < 0 or new_y >= SCREEN_HEIGHT - TILE_SIZE:
            return False
            
        # 檢查地圖碰撞
        tile_x = new_x // TILE_SIZE
        tile_y = new_y // TILE_SIZE
        
        if tile_y < len(map_data) and tile_x < len(map_data[0]):
            tile = map_data[tile_y][tile_x]
            if tile in [1, 2, 3]:  # 樹木、水、山
                return False
        
        self.x = new_x
        self.y = new_y
        self.is_moving = True
        
        if dx > 0:
            self.direction = Direction.RIGHT
        elif dx < 0:
            self.direction = Direction.LEFT
        elif dy > 0:
            self.direction = Direction.DOWN
        elif dy < 0:
            self.direction = Direction.UP
            
        return True
    
    def draw(self, screen):
        # 繪製角色（簡單的像素風格）
        rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, self.color, rect)
        
        # 繪製眼睛表示方向
        eye_offset = 0
        if self.direction == Direction.RIGHT:
            eye_offset = 4
        elif self.direction == Direction.LEFT:
            eye_offset = -4
            
        eye_x = self.x + TILE_SIZE // 2 + eye_offset
        eye_y = self.y + 8
        
        pygame.draw.circle(screen, COLORS['white'], (eye_x - 3, eye_y), 3)
        pygame.draw.circle(screen, COLORS['white'], (eye_x + 3, eye_y), 3)
        pygame.draw.circle(screen, COLORS['black'], (eye_x - 3, eye_y), 1)
        pygame.draw.circle(screen, COLORS['black'], (eye_x + 3, eye_y), 1)
    
    def take_damage(self, damage):
        self.hp -= max(0, damage - self.defense)
        return max(0, damage - self.defense)
    
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
    
    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 100:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.exp = 0
        self.max_hp += 20
        self.hp = self.max_hp
        self.max_mp += 10
        self.mp = self.max_mp
        self.attack += 3
        self.defense += 2

class Enemy:
    def __init__(self, x, y, name, color, level=1):
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.level = level
        self.hp = level * 30
        self.max_hp = level * 30
        self.attack = level * 8
        self.defense = level * 3
        self.exp_reward = level * 20
        self.alive = True
        
    def draw(self, screen):
        if self.alive:
            rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, self.color, rect)
            
            # 繪製憤怒的眼睛
            eye_y = self.y + 10
            pygame.draw.circle(screen, COLORS['white'], (self.x + 8, eye_y), 4)
            pygame.draw.circle(screen, COLORS['white'], (self.x + 24, eye_y), 4)
            pygame.draw.circle(screen, COLORS['red'], (self.x + 8, eye_y), 2)
            pygame.draw.circle(screen, COLORS['red'], (self.x + 24, eye_y), 2)
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        if self.hp <= 0:
            self.alive = False
        return actual_damage

class TileMap:
    def __init__(self):
        # 0:草地, 1:樹木, 2:水, 3:山, 4:道路, 5:建築
        self.tile_size = TILE_SIZE
        self.map_width = SCREEN_WIDTH // self.tile_size
        self.map_height = SCREEN_HEIGHT // self.tile_size
        self.data = self.generate_map()
        
    def generate_map(self):
        map_data = []
        for y in range(self.map_height):
            row = []
            for x in range(self.map_width):
                # 生成自然地形
                rand = random.random()
                if rand < 0.7:
                    tile = 0  # 草地
                elif rand < 0.8:
                    tile = 1  # 樹木
                elif rand < 0.85:
                    tile = 2  # 水
                elif rand < 0.9:
                    tile = 3  # 山
                elif rand < 0.95:
                    tile = 4  # 道路
                else:
                    tile = 0  # 草地
            map_data.append(row)
        
        # 添加一些道路（確保不超出邊界）
        if self.map_height > 0:
            center_y = self.map_height // 2
            for x in range(self.map_width):
                map_data[center_y][x] = 4
        
        if self.map_width > 0:
            center_x = self.map_width // 2
            for y in range(self.map_height):
                map_data[y][center_x] = 4
            
        # 添加建築（村莊）- 確保不超出邊界
        for y in range(2, min(5, self.map_height)):
            for x in range(2, min(5, self.map_width)):
                map_data[y][x] = 5
                
        return map_data
    
    def draw(self, screen, camera_x=0, camera_y=0):
        for y in range(self.map_height):
            for x in range(self.map_width):
                tile = self.data[y][x]
                screen_x = x * self.tile_size - camera_x
                screen_y = y * self.tile_size - camera_y
                
                # 只繪製可見區域
                if screen_x < -self.tile_size or screen_x > SCREEN_WIDTH:
                    continue
                if screen_y < -self.tile_size or screen_y > SCREEN_HEIGHT:
                    continue
                
                rect = pygame.Rect(screen_x, screen_y, self.tile_size, self.tile_size)
                
                if tile == 0:  # 草地
                    pygame.draw.rect(screen, COLORS['grass'], rect)
                elif tile == 1:  # 樹木
                    pygame.draw.rect(screen, COLORS['dark_green'], rect)
                    # 繪製樹冠
                    pygame.draw.circle(screen, COLORS['green'], 
                                     (screen_x + self.tile_size//2, screen_y + self.tile_size//2), 
                                     self.tile_size//2 - 2)
                elif tile == 2:  # 水
                    pygame.draw.rect(screen, COLORS['water'], rect)
                elif tile == 3:  # 山
                    pygame.draw.rect(screen, COLORS['gray'], rect)
                    # 繪製山峰
                    points = [(screen_x + self.tile_size//2, screen_y + 2),
                             (screen_x + 2, screen_y + self.tile_size - 2),
                             (screen_x + self.tile_size - 2, screen_y + self.tile_size - 2)]
                    pygame.draw.polygon(screen, COLORS['brown'], points)
                elif tile == 4:  # 道路
                    pygame.draw.rect(screen, COLORS['sand'], rect)
                elif tile == 5:  # 建築
                    pygame.draw.rect(screen, COLORS['brown'], rect)
                    # 繪製屋頂
                    roof_points = [(screen_x + self.tile_size//2, screen_y + 2),
                                  (screen_x + 2, screen_y + self.tile_size//2),
                                  (screen_x + self.tile_size - 2, screen_y + self.tile_size//2)]
                    pygame.draw.polygon(screen, COLORS['red'], roof_points)

class BattleSystem:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.turn = 0
        self.battle_log = []
        self.action_selected = False
        self.target_selected = False
        self.selected_action = None
        self.selected_target = None
        self.animation_frame = 0
        self.battle_ended = False
        
    def draw(self, screen):
        # 繪製戰鬥背景
        screen.fill(COLORS['dark_green'])
        
        # 繪製敵人
        for i, enemy in enumerate(self.enemies):
            if enemy.alive:
                enemy.x = SCREEN_WIDTH // 2 + (i - len(self.enemies)//2) * 80
                enemy.y = 150
                enemy.draw(screen)
                # 繪製敵人HP條
                self.draw_health_bar(screen, enemy.x, enemy.y - 10, enemy.hp, enemy.max_hp, 30, 5)
        
        # 繪製玩家
        self.player.x = SCREEN_WIDTH // 2
        self.player.y = 450
        self.player.draw(screen)
        
        # 繪製玩家狀態
        self.draw_status_panel(screen)
        
        # 繪製戰鬥選單
        if not self.battle_ended:
            self.draw_battle_menu(screen)
        
        # 繪製戰鬥日誌
        self.draw_battle_log(screen)
        
        # 繪製動畫效果
        if self.animation_frame > 0:
            self.draw_attack_animation(screen)
    
    def draw_status_panel(self, screen):
        panel_rect = pygame.Rect(10, SCREEN_HEIGHT - 120, 250, 110)
        pygame.draw.rect(screen, COLORS['blue'], panel_rect)
        pygame.draw.rect(screen, COLORS['white'], panel_rect, 2)
        
        font = pygame.font.Font(None, 24)
        y_offset = 20
        
        texts = [
            f"{self.player.name} Lv.{self.player.level}",
            f"HP: {self.player.hp}/{self.player.max_hp}",
            f"MP: {self.player.mp}/{self.player.max_mp}",
            f"ATK: {self.player.attack} DEF: {self.player.defense}"
        ]
        
        for text in texts:
            text_surface = font.render(text, True, COLORS['white'])
            screen.blit(text_surface, (20, y_offset))
            y_offset += 22
    
    def draw_health_bar(self, screen, x, y, current, maximum, width, height):
        ratio = current / maximum if maximum > 0 else 0
        bar_rect = pygame.Rect(x, y, width, height)
        fill_rect = pygame.Rect(x, y, int(width * ratio), height)
        
        pygame.draw.rect(screen, COLORS['red'], bar_rect)
        pygame.draw.rect(screen, COLORS['green'], fill_rect)
        pygame.draw.rect(screen, COLORS['white'], bar_rect, 1)
    
    def draw_battle_menu(self, screen):
        menu_rect = pygame.Rect(SCREEN_WIDTH - 260, SCREEN_HEIGHT - 120, 250, 110)
        pygame.draw.rect(screen, COLORS['blue'], menu_rect)
        pygame.draw.rect(screen, COLORS['white'], menu_rect, 2)
        
        font = pygame.font.Font(None, 28)
        options = ["攻擊", "技能", "道具", "逃跑"]
        
        for i, option in enumerate(options):
            y = SCREEN_HEIGHT - 110 + i * 25
            color = COLORS['yellow'] if i == 0 and not self.action_selected else COLORS['white']
            text_surface = font.render(option, True, color)
            screen.blit(text_surface, (SCREEN_WIDTH - 250, y))
    
    def draw_battle_log(self, screen):
        log_rect = pygame.Rect(270, SCREEN_HEIGHT - 80, SCREEN_WIDTH - 280, 70)
        pygame.draw.rect(screen, (0, 0, 100), log_rect)
        pygame.draw.rect(screen, COLORS['white'], log_rect, 1)
        
        font = pygame.font.Font(None, 20)
        y_offset = SCREEN_HEIGHT - 75
        
        for log in self.battle_log[-2:]:
            text_surface = font.render(log, True, COLORS['white'])
            screen.blit(text_surface, (280, y_offset))
            y_offset += 20
    
    def draw_attack_animation(self, screen):
        if self.selected_target and self.selected_target.alive:
            # 簡單的攻擊動畫
            progress = self.animation_frame / 10
            start_x = self.player.x + TILE_SIZE // 2
            start_y = self.player.y + TILE_SIZE // 2
            end_x = self.selected_target.x + TILE_SIZE // 2
            end_y = self.selected_target.y + TILE_SIZE // 2
            
            current_x = start_x + (end_x - start_x) * progress
            current_y = start_y + (end_y - start_y) * progress
            
            pygame.draw.circle(screen, COLORS['yellow'], (int(current_x), int(current_y)), 5)
            self.animation_frame += 1
    
    def handle_input(self, event):
        if self.battle_ended:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True  # 結束戰鬥
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z or event.key == pygame.K_SPACE:
                if not self.action_selected:
                    self.action_selected = True
                    self.selected_action = "attack"
                    self.battle_log.append(f"{self.player.name} 準備攻擊！")
                elif not self.target_selected:
                    # 選擇第一個活著的敵人
                    for enemy in self.enemies:
                        if enemy.alive:
                            self.selected_target = enemy
                            self.target_selected = True
                            break
                else:
                    # 執行攻擊
                    if self.selected_target:
                        damage = self.selected_target.take_damage(self.player.attack)
                        self.battle_log.append(f"對 {self.selected_target.name} 造成 {damage} 點傷害！")
                        self.animation_frame = 1
                        
                        if not self.selected_target.alive:
                            self.battle_log.append(f"{self.selected_target.name} 被擊敗了！")
                            self.player.gain_exp(self.selected_target.exp_reward)
                        
                        # 檢查是否所有敵人都被擊敗
                        if all(not enemy.alive for enemy in self.enemies):
                            self.battle_ended = True
                            self.battle_log.append("戰鬥勝利！")
                        else:
                            # 敵人回合
                            self.enemy_turn()
                    
                    # 重置選擇
                    self.action_selected = False
                    self.target_selected = False
                    self.selected_action = None
                    self.selected_target = None
        
        return False
    
    def enemy_turn(self):
        for enemy in self.enemies:
            if enemy.alive:
                damage = self.player.take_damage(enemy.attack)
                self.battle_log.append(f"{enemy.name} 攻擊造成 {damage} 點傷害！")
                
                if self.player.hp <= 0:
                    self.battle_ended = True
                    self.battle_log.append("你被打敗了...")
                    break

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("日式RPG冒險 - 無版權資源版")
        self.clock = pygame.time.Clock()
        self.state = GameState.TITLE
        self.running = True
        
        # 生成遊戲圖標
        self.icon = self.create_game_icon()
        pygame.display.set_icon(self.icon)
        
        # 初始化遊戲對象
        self.player = None
        self.map = None
        self.camera_x = 0
        self.camera_y = 0
        self.dialogue_text = ""
        self.dialogue_timer = 0
        self.battle_system = None
        self.enemies = []
        
        # 嘗試生成簡單的BGM
        self.generate_bgm()
        
    def create_game_icon(self):
        """創建遊戲圖標（程式生成的像素藝術）"""
        icon_size = 32
        icon = pygame.Surface((icon_size, icon_size))
        icon.fill(COLORS['blue'])
        
        # 繪製一個簡單的劍與盾圖案
        pygame.draw.rect(icon, COLORS['yellow'], (8, 4, 16, 24))
        pygame.draw.rect(icon, COLORS['red'], (12, 8, 8, 16))
        pygame.draw.circle(icon, COLORS['white'], (16, 16), 6)
        
        return icon
    
    def generate_bgm(self):
        """生成簡單的背景音樂（合成音）"""
        if not AUDIO_AVAILABLE:
            self.bg_music = None
            return
            
        try:
            # 創建一個簡單的音效作為替代（立體聲）
            sample_rate = 44100
            duration = 2  # 秒
            frequency = 440  # Hz
            
            import numpy as np
            
            # 生成立體聲陣列 (samples, 2 channels)
            t_values = np.linspace(0, duration, int(sample_rate * duration))
            samples = (128 + 127 * np.sin(2 * np.pi * frequency * t_values)).astype(np.int16)
            
            # 轉換為立體聲（兩個聲道）
            stereo_samples = np.column_stack((samples, samples))
            
            self.bg_music = pygame.sndarray.make_sound(stereo_samples)
            self.bg_music.set_volume(0.3)
        except Exception as e:
            print(f"無法生成音樂：{e}")
            self.bg_music = None
    
    def new_game(self):
        """開始新遊戲"""
        self.map = TileMap()
        
        # 找到玩家的起始位置（村莊附近）
        start_x = 6 * TILE_SIZE
        start_y = 6 * TILE_SIZE
        
        self.player = Character(start_x, start_y, "勇者", COLORS['blue'])
        
        # 生成一些敵人
        self.enemies = [
            Enemy(0, 0, "史萊姆", COLORS['cyan'], 1),
            Enemy(0, 0, "哥布林", COLORS['green'], 2),
            Enemy(0, 0, "蝙蝠", COLORS['purple'], 1),
        ]
        
        self.dialogue_text = "歡迎來到這個世界！使用方向鍵移動，Z鍵互動。"
        self.dialogue_timer = 300  # 5秒鐘
        
        self.state = GameState.PLAYING
    
    def start_battle(self):
        """開始戰鬥"""
        # 隨機選擇1-2個敵人
        num_enemies = random.randint(1, 2)
        battle_enemies = random.sample(self.enemies, num_enemies)
        
        # 複製敵人用於戰鬥
        copied_enemies = []
        for enemy in battle_enemies:
            copied_enemies.append(Enemy(0, 0, enemy.name, enemy.color, enemy.level))
        
        self.battle_system = BattleSystem(self.player, copied_enemies)
        self.state = GameState.BATTLE
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.state == GameState.TITLE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z or event.key == pygame.K_SPACE:
                        self.new_game()
            
            elif self.state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.TITLE
                    
                    # 對話跳過
                    if self.dialogue_timer > 0 and (event.key == pygame.K_z or event.key == pygame.K_SPACE):
                        self.dialogue_timer = 0
                        continue
                    
                    # 隨機遇敵
                    if random.random() < 0.05:  # 5%機率遇敵
                        self.start_battle()
                
                # 移動控制
                if self.dialogue_timer <= 0:
                    keys = pygame.key.get_pressed()
                    dx, dy = 0, 0
                    if keys[pygame.K_UP] or keys[pygame.K_w]:
                        dy = -self.player.speed
                    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                        dy = self.player.speed
                    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        dx = -self.player.speed
                    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        dx = self.player.speed
                    
                    if dx != 0 or dy != 0:
                        # 歸一化對角線移動
                        if dx != 0 and dy != 0:
                            dx *= 0.707
                            dy *= 0.707
                        
                        self.player.move(dx, dy, self.map.data)
                    
                    # 更新相機
                    self.camera_x = max(0, min(self.player.x - SCREEN_WIDTH // 2, 
                                              self.map.map_width * TILE_SIZE - SCREEN_WIDTH))
                    self.camera_y = max(0, min(self.player.y - SCREEN_HEIGHT // 2,
                                              self.map.map_height * TILE_SIZE - SCREEN_HEIGHT))
            
            elif self.state == GameState.BATTLE:
                if self.battle_system.handle_input(event):
                    # 戰鬥結束
                    if self.player.hp > 0:
                        self.player.hp = max(1, self.player.hp)  # 至少保留1點HP
                        self.state = GameState.PLAYING
                        self.dialogue_text = "戰鬥勝利！獲得了經驗值。"
                        self.dialogue_timer = 180
                    else:
                        self.state = GameState.GAME_OVER
            
            elif self.state == GameState.GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z or event.key == pygame.K_SPACE:
                        self.state = GameState.TITLE
    
    def update(self):
        if self.dialogue_timer > 0:
            self.dialogue_timer -= 1
        
        if self.state == GameState.BATTLE and self.battle_system:
            pass  # 戰鬥邏輯在handle_input中處理
    
    def draw_title_screen(self):
        """繪製標題畫面"""
        self.screen.fill(COLORS['black'])
        
        # 繪製標題
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("日式RPG冒險", True, COLORS['gold'])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title_text, title_rect)
        
        subtitle_font = pygame.font.Font(None, 36)
        subtitle_text = subtitle_font.render("Press Z or SPACE to Start", True, COLORS['white'])
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # 繪製裝飾
        decor_font = pygame.font.Font(None, 24)
        info_text = decor_font.render("All assets are copyright-free", True, COLORS['gray'])
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(info_text, info_rect)
        
        # 閃爍的提示
        if pygame.time.get_ticks() % 1000 < 500:
            prompt_text = decor_font.render("> Press Z to Begin <", True, COLORS['yellow'])
            prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
            self.screen.blit(prompt_text, prompt_rect)
    
    def draw_game_screen(self):
        """繪製遊戲畫面"""
        self.screen.fill(COLORS['black'])
        
        # 繪製地圖
        if self.map:
            self.map.draw(self.screen, self.camera_x, self.camera_y)
        
        # 繪製玩家
        if self.player:
            self.player.draw(self.screen)
        
        # 繪製對話框
        if self.dialogue_timer > 0 and self.dialogue_text:
            dialogue_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 100, 80)
            pygame.draw.rect(self.screen, COLORS['blue'], dialogue_rect)
            pygame.draw.rect(self.screen, COLORS['white'], dialogue_rect, 2)
            
            font = pygame.font.Font(None, 28)
            text_surface = font.render(self.dialogue_text, True, COLORS['white'])
            self.screen.blit(text_surface, (60, SCREEN_HEIGHT - 90))
        
        # 繪製UI
        self.draw_ui()
    
    def draw_battle_screen(self):
        """繪製戰鬥畫面"""
        if self.battle_system:
            self.battle_system.draw(self.screen)
    
    def draw_game_over_screen(self):
        """繪製遊戲結束畫面"""
        self.screen.fill(COLORS['black'])
        
        font = pygame.font.Font(None, 72)
        text = font.render("GAME OVER", True, COLORS['red'])
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        small_font = pygame.font.Font(None, 36)
        prompt = small_font.render("Press Z to return to title", True, COLORS['white'])
        prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(prompt, prompt_rect)
    
    def draw_ui(self):
        """繪製用戶界面"""
        if self.player:
            # HP條
            hp_ratio = self.player.hp / self.player.max_hp if self.player.max_hp > 0 else 0
            hp_bar_rect = pygame.Rect(10, 10, 200, 20)
            pygame.draw.rect(self.screen, COLORS['red'], hp_bar_rect)
            pygame.draw.rect(self.screen, COLORS['green'], 
                           (10, 10, int(200 * hp_ratio), 20))
            pygame.draw.rect(self.screen, COLORS['white'], hp_bar_rect, 2)
            
            # MP條
            mp_ratio = self.player.mp / self.player.max_mp if self.player.max_mp > 0 else 0
            mp_bar_rect = pygame.Rect(10, 35, 150, 15)
            pygame.draw.rect(self.screen, COLORS['blue'], mp_bar_rect)
            pygame.draw.rect(self.screen, COLORS['cyan'],
                           (10, 35, int(150 * mp_ratio), 15))
            pygame.draw.rect(self.screen, COLORS['white'], mp_bar_rect, 2)
            
            # 等級顯示
            font = pygame.font.Font(None, 24)
            level_text = font.render(f"Lv.{self.player.level}", True, COLORS['white'])
            self.screen.blit(level_text, (10, 60))
    
    def draw(self):
        if self.state == GameState.TITLE:
            self.draw_title_screen()
        elif self.state == GameState.PLAYING:
            self.draw_game_screen()
        elif self.state == GameState.BATTLE:
            self.draw_battle_screen()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over_screen()
        
        pygame.display.flip()
    
    def run(self):
        """主遊戲循環"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """遊戲入口點"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
