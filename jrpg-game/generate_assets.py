"""
生成無版權遊戲資源
- 圖標 (PNG)
- 背景音樂 (WAV/OGG)
- 音效 (WAV)
所有資源均為程式生成，無版權問題
"""

import numpy as np
from PIL import Image, ImageDraw
import wave
import struct
import os

def create_game_icon(filename="assets/icon.png", size=64):
    """創建遊戲圖標 - 像素風格的劍與盾"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 背景圓形
    draw.ellipse([2, 2, size-2, size-2], fill=(30, 144, 255, 255))
    
    # 盾牌
    shield_points = [
        (size//2, size//4),
        (size*3//4, size//3),
        (size*3//4, size*2//3),
        (size//2, size*3//4),
        (size//4, size*2//3),
        (size//4, size//3)
    ]
    draw.polygon(shield_points, fill=(255, 215, 0, 255))
    draw.polygon(shield_points, outline=(139, 69, 19, 255), width=2)
    
    # 劍
    sword_blade = [
        (size//2 + 8, size//3),
        (size//2 + 4, size//2),
        (size//2 - 4, size//2),
        (size//2 - 8, size//3)
    ]
    draw.polygon(sword_blade, fill=(192, 192, 192, 255))
    
    # 劍柄
    draw.rectangle([size//2-2, size//2, size//2+2, size*2//3], fill=(139, 69, 19, 255))
    draw.rectangle([size//2-6, size//2, size//2+6, size//2+4], fill=(255, 215, 0, 255))
    
    img.save(filename, 'PNG')
    print(f"✓ 已創建圖標：{filename}")
    return filename

def create_tileset(filename="assets/tileset.png", tile_size=32):
    """創建地形圖塊集"""
    tiles_per_row = 6
    img = Image.new('RGB', (tile_size * tiles_per_row, tile_size * 3), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 0: 草地
    for y in range(tile_size):
        for x in range(tile_size):
            if (x + y) % 4 == 0:
                draw.point((x, y), (34, 139, 34))
            else:
                draw.point((x, y), (50, 160, 50))
    
    # 1: 樹木
    offset_x = tile_size
    draw.rectangle([offset_x, 0, offset_x+tile_size, tile_size], fill=(139, 69, 19))
    draw.ellipse([offset_x+4, 4, offset_x+tile_size-4, tile_size//2], fill=(34, 139, 34))
    draw.ellipse([offset_x+8, 8, offset_x+tile_size-8, tile_size//2-4], fill=(0, 100, 0))
    
    # 2: 水
    offset_x = tile_size * 2
    draw.rectangle([offset_x, 0, offset_x+tile_size, tile_size], fill=(30, 144, 255))
    for w in range(3):
        wy = 8 + w * 8
        draw.line([(offset_x+4, wy), (offset_x+tile_size-4, wy)], fill=(173, 216, 230), width=2)
    
    # 3: 山
    offset_x = tile_size * 3
    draw.rectangle([offset_x, 0, offset_x+tile_size, tile_size], fill=(128, 128, 128))
    draw.polygon([
        (offset_x + tile_size//2, 4),
        (offset_x + 4, tile_size - 4),
        (offset_x + tile_size - 4, tile_size - 4)
    ], fill=(160, 160, 160))
    draw.polygon([
        (offset_x + tile_size//2, 4),
        (offset_x + 8, tile_size//2),
        (offset_x + tile_size - 8, tile_size//2)
    ], fill=(255, 255, 255))
    
    # 4: 道路
    offset_x = tile_size * 4
    draw.rectangle([offset_x, 0, offset_x+tile_size, tile_size], fill=(244, 164, 96))
    for r in range(4):
        rx = 8 + r * 6
        draw.line([(rx, 4), (rx, tile_size-4)], fill=(210, 140, 70), width=1)
    
    # 5: 建築
    offset_x = tile_size * 5
    draw.rectangle([offset_x, tile_size//3, offset_x+tile_size, tile_size], fill=(139, 69, 19))
    draw.polygon([
        (offset_x + tile_size//2, 2),
        (offset_x + 2, tile_size//3),
        (offset_x + tile_size - 2, tile_size//3)
    ], fill=(220, 20, 60))
    draw.rectangle([offset_x+tile_size//2-4, tile_size//2, offset_x+tile_size//2+4, tile_size-4], fill=(100, 50, 10))
    
    img.save(filename, 'PNG')
    print(f"✓ 已創建圖塊集：{filename}")
    return filename

def generate_sound_wave(frequency, duration, sample_rate=44100, volume=0.5, wave_type='sine'):
    """生成音效波形"""
    samples = int(sample_rate * duration)
    t = np.linspace(0, duration, samples, False)
    
    if wave_type == 'sine':
        wave_data = np.sin(2 * np.pi * frequency * t)
    elif wave_type == 'square':
        wave_data = np.sign(np.sin(2 * np.pi * frequency * t))
    elif wave_type == 'triangle':
        wave_data = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
    elif wave_type == 'noise':
        wave_data = np.random.uniform(-1, 1, samples)
    else:
        wave_data = np.sin(2 * np.pi * frequency * t)
    
    # 添加淡入淡出
    fade_samples = int(sample_rate * 0.01)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    
    if len(wave_data) > fade_samples * 2:
        wave_data[:fade_samples] *= fade_in
        wave_data[-fade_samples:] *= fade_out
    
    wave_data = wave_data * volume * 32767
    return wave_data.astype(np.int16)

def create_bgm(filename="assets/music/bgm_title.wav", duration=30):
    """創建背景音樂 - 簡單的 RPG 風格旋律"""
    sample_rate = 44100
    
    # 簡單的 RPG 主題旋律（C大調）
    notes = {
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
        'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
        'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46,
        'G5': 783.99, 'A5': 880.00
    }
    
    # 簡單旋律序列
    melody = [
        ('C4', 0.5), ('E4', 0.5), ('G4', 0.5), ('C5', 0.5),
        ('G4', 0.5), ('E4', 0.5), ('C4', 0.5), ('D4', 0.5),
        ('E4', 0.5), ('F4', 0.5), ('G4', 0.5), ('A4', 0.5),
        ('G4', 0.5), ('F4', 0.5), ('E4', 0.5), ('D4', 0.5),
    ] * 4  # 重複以達到足夠長度
    
    all_samples = []
    current_time = 0
    
    for note, note_duration in melody:
        if current_time >= duration:
            break
        
        freq = notes.get(note, 440)
        
        # 主旋律
        main_wave = generate_sound_wave(freq, note_duration, sample_rate, 0.4, 'sine')
        
        # 和聲（低八度）
        if note in notes:
            harmony_freq = freq / 2
            harmony_wave = generate_sound_wave(harmony_freq, note_duration, sample_rate, 0.2, 'sine')
            
            # 混合
            if len(main_wave) == len(harmony_wave):
                mixed = (main_wave.astype(np.int32) + harmony_wave.astype(np.int32)) // 2
                mixed = np.clip(mixed, -32768, 32767).astype(np.int16)
            else:
                mixed = main_wave
        else:
            mixed = main_wave
        
        all_samples.extend(mixed.tolist())
        current_time += note_duration
    
    # 填充剩餘時間
    while current_time < duration:
        remaining = duration - current_time
        if remaining < 0.5:
            silence = np.zeros(int(sample_rate * remaining), dtype=np.int16)
        else:
            silence = np.zeros(int(sample_rate * 0.5), dtype=np.int16)
        all_samples.extend(silence.tolist())
        current_time += min(remaining, 0.5)
    
    # 轉換為立體聲
    audio_data = np.array(all_samples[:int(sample_rate * duration)])
    stereo_data = np.column_stack((audio_data, audio_data))
    
    # 保存 WAV 文件
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for sample in stereo_data:
            wav_file.writeframes(struct.pack('<hh', sample[0], sample[1]))
    
    print(f"✓ 已創建背景音樂：{filename}")
    return filename

def create_sfx_attack(filename="assets/music/sfx_attack.wav"):
    """創建攻擊音效"""
    sample_rate = 44100
    duration = 0.3
    
    # 混合多個波形創建打擊音效
    wave1 = generate_sound_wave(150, duration, sample_rate, 0.5, 'triangle')
    wave2 = generate_sound_wave(100, duration * 0.7, sample_rate, 0.4, 'square')
    noise = generate_sound_wave(0, duration * 0.2, sample_rate, 0.3, 'noise')
    
    # 確保長度一致
    min_len = min(len(wave1), len(wave2), len(noise))
    wave1 = wave1[:min_len]
    wave2 = wave2[:min_len]
    noise = noise[:min_len]
    
    # 混合
    mixed = (wave1.astype(np.int32) + wave2.astype(np.int32) + noise.astype(np.int32)) // 3
    mixed = np.clip(mixed, -32768, 32767).astype(np.int16)
    
    # 立體聲
    stereo_data = np.column_stack((mixed, mixed))
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for sample in stereo_data:
            wav_file.writeframes(struct.pack('<hh', sample[0], sample[1]))
    
    print(f"✓ 已創建攻擊音效：{filename}")
    return filename

def create_sfx_hit(filename="assets/music/sfx_hit.wav"):
    """創建受擊音效"""
    sample_rate = 44100
    duration = 0.2
    
    # 下降音調的受擊音效
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    freq = 200 * np.exp(-t * 10)
    wave_data = np.sin(2 * np.pi * freq * t) * np.exp(-t * 5)
    
    wave_data = wave_data * 0.5 * 32767
    wave_data = wave_data.astype(np.int16)
    
    stereo_data = np.column_stack((wave_data, wave_data))
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for sample in stereo_data:
            wav_file.writeframes(struct.pack('<hh', sample[0], sample[1]))
    
    print(f"✓ 已創建受擊音效：{filename}")
    return filename

def create_sfx_levelup(filename="assets/music/sfx_levelup.wav"):
    """創建升級音效"""
    sample_rate = 44100
    
    # 上升音階
    notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
    duration_per_note = 0.15
    
    all_samples = []
    for freq in notes:
        wave_data = generate_sound_wave(freq, duration_per_note, sample_rate, 0.4, 'sine')
        all_samples.extend(wave_data.tolist())
    
    audio_data = np.array(all_samples, dtype=np.int16)
    stereo_data = np.column_stack((audio_data, audio_data))
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for sample in stereo_data:
            wav_file.writeframes(struct.pack('<hh', sample[0], sample[1]))
    
    print(f"✓ 已創建升級音效：{filename}")
    return filename

if __name__ == "__main__":
    print("正在生成無版權遊戲資源...")
    print()
    
    # 確保目錄存在
    os.makedirs("assets/images", exist_ok=True)
    os.makedirs("assets/music", exist_ok=True)
    os.makedirs("assets/fonts", exist_ok=True)
    
    # 創建視覺資源
    create_game_icon()
    create_tileset()
    
    # 創建音頻資源
    create_bgm()
    create_sfx_attack()
    create_sfx_hit()
    create_sfx_levelup()
    
    print()
    print("所有資源生成完成！")
    print("這些資源都是程式生成的，無版權問題，可自由使用。")
