import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  
import random
import os

# ==================== 1. 完整 13 關主線與野外資料 ====================
MAIN_STAGES = [
    {"name": "大岩蛇", "level": 12, "hp": 80, "move": "落石", "exp_reward": 20},     
    {"name": "寶石海星", "level": 18, "hp": 95, "move": "水炮", "exp_reward": 40},   
    {"name": "雷丘", "level": 22, "hp": 110, "move": "十萬伏特", "exp_reward": 70},  
    {"name": "霸王花", "level": 26, "hp": 125, "move": "日光束", "exp_reward": 110}, 
    {"name": "末入蛾", "level": 32, "hp": 140, "move": "蟲鳴", "exp_reward": 160},   
    {"name": "胡地", "level": 38, "hp": 155, "move": "精神強念", "exp_reward": 240}, 
    {"name": "鴨嘴火獸", "level": 42, "hp": 170, "move": "大字爆炎", "exp_reward": 360},
    {"name": "鑽角犀獸", "level": 45, "hp": 185, "move": "地震", "exp_reward": 500},  
    {"name": "乘龍", "level": 52, "hp": 210, "move": "絕對零度", "exp_reward": 760}, 
    {"name": "怪力", "level": 54, "hp": 230, "move": "爆裂拳", "exp_reward": 1040},  
    {"name": "耿鬼", "level": 56, "hp": 250, "move": "暗影球", "exp_reward": 1400},  
    {"name": "快龍", "level": 60, "hp": 280, "move": "破壞光線", "exp_reward": 1900}, 
    {"name": "超夢", "level": 70, "hp": 350, "move": "精神擊破", "exp_reward": 3000}  
]

WILD_POOL = {
    "1-10": [{"name": "綠毛蟲", "move": "撞擊"}, {"name": "小拉達", "move": "電光一閃"}, {"name": "獨角蟲", "move": "毒針"}, {"name": "波波", "move": "起風"}, {"name": "阿柏蛇", "move": "緊束"}, {"name": "皮卡丘", "move": "電擊"}, {"name": "穿山鼠", "move": "抓"}, {"name": "尼多蘭", "move": "二連踢"}, {"name": "胖丁", "move": "連環巴掌"}, {"name": "地鼠", "move": "潑沙"}],
    "11-20": [{"name": "比比鳥", "move": "烈暴風"}, {"name": "阿柏怪", "move": "溶解液"}, {"name": "巴大蝶", "move": "念力"}, {"name": "大嘴蝠", "move": "翅膀攻擊"}, {"name": "臭臭花", "move": "超級吸取"}, {"name": "派拉斯", "move": "吸血"}, {"name": "喵喵", "move": "聚寶功"}, {"name": "可達鴨", "move": "水槍"}, {"name": "蚊香蝌蚪", "move": "泡沫"}, {"name": "凱西", "move": "折彎湯匙"}],
    "21-30": [{"name": "三地鼠", "move": "泥巴炸彈"}, {"name": "風速狗", "move": "火焰輪"}, {"name": "蚊香君", "move": "連環巴掌"}, {"name": "勇基拉", "move": "幻象光線"}, {"name": "豪力", "move": "空手劈"}, {"name": "隆隆石", "move": "滾石"}, {"name": "小火馬", "move": "火焰漩渦"}, {"name": "呆呆獸", "move": "水之波動"}, {"name": "大磁怪", "move": "電擊波"}, {"name": "大舌貝", "move": "冰凍之風"}],
    "31-40": [{"name": "大鬼斯通", "move": "暗影拳"}, {"name": "火爆獸", "move": "噴射火焰"}, {"name": "水箭龜", "move": "水炮"}, {"name": "妙蛙花", "move": "藤鞭"}, {"name": "噴火龍", "move": "噴射火焰"}, {"name": "飛腿郎", "move": "飛膝踢"}, {"name": "快拳郎", "move": "音速拳"}, {"name": "雙彈瓦斯", "move": "污泥炸彈"}, {"name": "巨鉗蟹", "move": "蟹鉗錘"}, {"name": "椰蛋樹", "move": "種子炸彈"}],
    "41-50": [{"name": "化石翼龍", "move": "原始力量"}, {"name": "卡比獸", "move": "終極衝擊"}, {"name": "急凍鳥", "move": "冰凍光束"}, {"name": "閃電鳥", "move": "打雷"}, {"name": "火焰鳥", "move": "熱風"}, {"name": "九尾", "move": "大字爆炎"}, {"name": "刺甲貝", "move": "冰錐"}, {"name": "鐮刀盔", "move": "水流裂破"}, {"name": "多邊獸", "move": "三角攻擊"}, {"name": "哈克龍", "move": "龍之波動"}]
}

BASE_SKILLS = {"🔥 悔念劍": 40, "👻 暗影衝擊": 30, "⚡ 蓄能焰襲": 20, "🔮 精神利刃": 25}

# ==================== 2. 真實每週單字資料庫配置區 ====================
WORD_WEEKLY_BANK = {}

# 【第 13 週】真實 50 單字清單
WEEK_13_INPUT = [
    {"en": "extra", "zh": "額外的"}, {"en": "eye", "zh": "眼"}, {"en": "face", "zh": "臉"}, 
    {"en": "fact", "zh": "事實"}, {"en": "factory", "zh": "工廠"}, {"en": "fail", "zh": "失敗"},
    {"en": "fair", "zh": "公平"}, {"en": "fall", "zh": "秋天"}, {"en": "false", "zh": "假的"}, 
    {"en": "family", "zh": "家庭"}, {"en": "famous", "zh": "出名"}, {"en": "fan", "zh": "電扇"},
    {"en": "fancy", "zh": "華麗"}, {"en": "fantastic", "zh": "好極了"}, {"en": "far", "zh": "遠的"}, 
    {"en": "farm", "zh": "農場"}, {"en": "farmer", "zh": "農夫"}, {"en": "fashionable", "zh": "流行的"}, 
    {"en": "fast", "zh": "很快地"}, {"en": "fat", "zh": "胖的"}, {"en": "father", "zh": "爸爸"}, 
    {"en": "faucet", "zh": "水龍頭"}, {"en": "fault", "zh": "錯誤"}, {"en": "favorite", "zh": "最喜愛的"}, 
    {"en": "fear", "zh": "恐懼"}, {"en": "february", "zh": "二月"}, {"en": "fee", "zh": "費用"}, 
    {"en": "feed", "zh": "餵食"}, {"en": "feel", "zh": "感覺到..."}, {"en": "feeling", "zh": "感受"}, 
    {"en": "female", "zh": "女性"}, {"en": "fence", "zh": "籬笆"}, {"en": "festival", "zh": "節慶"}, 
    {"en": "fever", "zh": "發燒"}, {"en": "few", "zh": "些許"}, {"en": "fifteen", "zh": "十五"}, 
    {"en": "fifty", "zh": "五十"}, {"en": "fight", "zh": "打鬥"}, {"en": "fill", "zh": "充滿"}, 
    {"en": "film", "zh": "底片"}, {"en": "final", "zh": "最後的"}, {"en": "finally", "zh": "終於"}, 
    {"en": "find", "zh": "找尋"}, {"en": "fine", "zh": "美好的"}, {"en": "finger", "zh": "手指"}, 
    {"en": "finish", "zh": "完成"}, {"en": "fire", "zh": "火"}, {"en": "first", "zh": "第一"}, 
    {"en": "fish", "zh": "魚"}, {"en": "fisherman", "zh": "漁夫"}
]

# 初始化 1-40 週的空清單結構 (已移除通用庫)
for week in range(1, 41):
    WORD_WEEKLY_BANK[f"第 {week} 週"] = []

# 將第 13 週單字精準寫入
WORD_WEEKLY_BANK["第 13 週"] = [(item["en"], item["zh"]) for item in WEEK_13_INPUT]

# ==================== 3. 遊戲狀態變數與儲存功能 ====================
SAVE_FILE = "pokemon_save.txt"

player_level = 5
player_current_exp = 0
player_max_hp = 50
player_hp = 50
current_stage = 0      
selected_week = "第 13 週"  

is_wild_mode = False   
current_enemy = {}     
current_answers = {}

def save_game():
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            f.write(f"{player_level}\n")
            f.write(f"{player_current_exp}\n")
            f.write(f"{current_stage}\n")
            f.write(f"{selected_week}\n")
        log_label.config(text="💾 遊戲進度已自動儲存！", fg="blue")
    except Exception as e:
        print("存檔失敗:", e)

def load_game():
    global player_level, player_current_exp, current_stage, selected_week, player_max_hp, player_hp
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                if len(lines) >= 4:
                    player_level = int(lines[0])
                    player_current_exp = int(lines[1])
                    current_stage = int(lines[2])
                    selected_week = lines[3]
                    
                    player_max_hp = calculate_max_hp(player_level)
                    player_hp = player_max_hp
                    print("讀檔成功！載入歷史進度。")
        except Exception as e:
            print("讀檔故障，設定初始化:", e)

# ==================== 4. 核心邏輯函數 ====================
def calculate_max_hp(lvl):
    if lvl >= 100: return 410
    return 50 + (lvl - 5) * 4

def check_level_up(added_exp):
    global player_level, player_current_exp, player_max_hp, player_hp
    player_current_exp += added_exp
    old_level = player_level
    
    while player_level < 100:
        next_lvl_required = ((player_level + 1) - 4) ** 2 * 50
        if player_current_exp >= next_lvl_required:
            player_level += 1
        else:
            break
            
    if player_level > old_level:
        player_max_hp = calculate_max_hp(player_level)
        player_hp = player_max_hp
        return True, player_level - old_level
    player_hp = player_max_hp
    return False, 0

def load_battle():
    global current_enemy, enemy_hp
    
    if not is_wild_mode:
        if current_stage >= len(MAIN_STAGES):
            messagebox.showinfo("終極勝利", "🎉 恭喜你！蒼炎刃鬼成功擊敗超夢，稱霸寶可夢聯盟！")
            root.destroy()
            return
        current_enemy = MAIN_STAGES[current_stage].copy()
        stage_label.config(text=f"【主線故事】第 {current_stage + 1} / {len(MAIN_STAGES)} 關")
    
    enemy_hp = current_enemy["hp"]
    enemy_name_label.config(text=f"{current_enemy['name']} (Lv.{current_enemy['level']})")
    enemy_hp_bar.config(text=f"HP: {enemy_hp}/{current_enemy['hp']}")
    
    player_name.config(text=f"我方 蒼炎刃鬼 Lv.{player_level} (EXP: {player_current_exp})")
    player_hp_bar.config(text=f"HP: {player_hp}/{player_max_hp}")
    
    prefix = "野生 " if is_wild_mode else "聯盟頭目 "
    log_label.config(text=f"{prefix}{current_enemy['name']} 出現了！請輸入正確單字發動招式！", fg="black")
    refresh_skills()

def enter_wild_zone(zone_range):
    global is_wild_mode, current_enemy
    is_wild_mode = True
    stage_label.config(text=f"【野生訓練區】草叢深處 ({zone_range}級)")
    
    min_l, max_l = map(int, zone_range.split("-"))
    wild_lvl = random.randint(min_l, max_l)
    template = random.choice(WILD_POOL[zone_range])
    
    wild_hp = 35 + wild_lvl * 3
    wild_exp = wild_lvl * 3 
    
    current_enemy = {
        "name": template["name"],
        "level": wild_lvl,
        "hp": wild_hp,
        "move": template["move"],
        "exp_reward": wild_exp
    }
    load_battle()

def quit_wild_zone():
    global is_wild_mode
    is_wild_mode = False
    load_battle()

def on_week_change(event):
    global selected_week
    selected_week = week_combobox.get()
    save_game() 
    refresh_skills()

def refresh_skills():
    global current_answers
    current_answers.clear()
    
    weekly_words = WORD_WEEKLY_BANK.get(selected_week, [])
    
    if len(weekly_words) < 4:
        skill_display.config(text=f"【 招式表狀態 】\n\n⚠️ {selected_week} 尚未錄入真實單字！\n請至程式碼中填寫該週單字清單後再行挑戰。")
        attack_btn.config(state="disabled")
        return
        
    attack_btn.config(state="normal")
    pool_copy = weekly_words.copy()
    random.shuffle(pool_copy)
    
    skill_text = f"【 蒼炎刃鬼 招式表 - 當前進度：{selected_week} 】\n\n"
    for i, (skill_name, base_dmg) in enumerate(BASE_SKILLS.items()):
        word, ans = pool_copy[i]
        lvl_bonus = int((player_level - 5) * 0.5)
        final_dmg = base_dmg + lvl_bonus
        
        current_answers[skill_name] = (ans, final_dmg)
        skill_text += f"{skill_name} (威力 {final_dmg}) ➔ 單字: {word}\n"
    
    skill_display.config(text=skill_text)
    input_entry.delete(0, tk.END)

def cast_attack():
    global player_hp, enemy_hp, current_stage, player_level, player_max_hp
    user_input = input_entry.get().strip()
    if not current_answers: 
        return
        
    matched_skill = None
    damage_dealt = 0
    for skill_name, (ans, dmg) in current_answers.items():
        if user_input == ans:
            matched_skill = skill_name
            damage_dealt = dmg
            break
            
    boss = MAIN_STAGES[current_stage] if not is_wild_mode else current_enemy
            
    if matched_skill:
        enemy_hp -= damage_dealt
        log_label.config(text=f"✨ 答對了！蒼炎刃鬼使出【{matched_skill}】！\n對 {boss['name']} 造成 {damage_dealt} 點傷害！", fg="green")
    else:
        if not is_wild_mode:
            base_damage = int(boss["level"] * 2.5) + 40
            boss_damage = base_damage + random.randint(-4, 4)
        else:
            base_damage = int(boss["level"] * 1.8) + 20
            boss_damage = base_damage + random.randint(-2, 2)
            
        player_hp -= boss_damage
        log_label.config(text=f"❌ 答錯了！Lv.{boss['level']} 的 {boss['name']} 使用了【{boss['move']}】！\n蒼炎刃鬼受到了 {boss_damage} 點傷害！", fg="red")

    player_hp_bar.config(text=f"HP: {player_hp}/{player_max_hp}")
    enemy_hp_bar.config(text=f"HP: {enemy_hp}/{boss['hp']}")
    
    if enemy_hp <= 0:
        exp_gained = boss["exp_reward"]
        is_up, lvl_gap = check_level_up(exp_gained)
        
        msg = f"🎉 成功擊敗了 {boss['name']}！\n獲得了 {exp_gained} 點經驗值！"
        if is_up:
            msg += f"\n🔥 蒼炎刃鬼等級提升了 {lvl_gap} 級！目前等級為 Lv.{player_level}！"
            
        messagebox.showinfo("戰鬥勝利", msg)
        if not is_wild_mode:
            current_stage += 1  
            
        save_game() 
        load_battle()
            
    elif player_hp <= 0:
        messagebox.showinfo("戰敗", "💀 蒼炎刃鬼失去戰鬥能力... 自動回中心補滿血。")
        player_hp = player_max_hp
        if not is_wild_mode:
            current_stage = max(0, current_stage - 1) 
        save_game() 
        load_battle()
    else:
        root.after(1500, refresh_skills)
# ==================== 5. GUI 介面佈局 ====================
load_game()

root = tk.Tk()
root.title("蒼炎刃鬼 - 寶可夢單字聯盟大挑戰")
root.geometry("760x700")
root.config(bg="#f5f5f5")

# --- 左側：戰鬥對戰主面板 ---
left_frame = tk.Frame(root, bg="#f5f5f5")
left_frame.pack(side="left", padx=15, fill="y")

stage_label = tk.Label(left_frame, text="", font=("Arial", 12, "bold"), bg="#f5f5f5", fg="#333")
stage_label.pack(pady=5)

battle_frame = tk.Frame(left_frame, bg="white", bd=2, relief="sunken", width=460, height=220)
battle_frame.pack_propagate(False)
battle_frame.pack(pady=10)

# 敵方寶可夢 UI
enemy_name_label = tk.Label(battle_frame, text="", font=("Arial", 11, "bold"), bg="white")
enemy_name_label.place(x=220, y=20)
enemy_hp_bar = tk.Label(battle_frame, text="", font=("Arial", 11), bg="white", fg="darkred")
enemy_hp_bar.place(x=220, y=45)
enemy_pic = tk.Label(battle_frame, bg="#e0e0e0", text="[對手寶可夢]")
enemy_pic.place(x=30, y=10, width=120, height=120)

# 我方蒼炎刃鬼 UI
player_name = tk.Label(battle_frame, text="", font=("Arial", 11, "bold"), bg="white")
player_name.place(x=30, y=140)
player_hp_bar = tk.Label(battle_frame, text="", font=("Arial", 11), bg="white", fg="darkgreen")
player_hp_bar.place(x=30, y=165)
player_pic = tk.Label(battle_frame, bg="#e0e0e0", text="[蒼炎刃鬼]")
player_pic.place(x=300, y=90, width=120, height=120)

# 戰鬥對話 Log 與招式題目顯示
log_label = tk.Label(left_frame, text="進入戰鬥...", font=("Arial", 11), wraplength=440, bg="#f5f5f5", height=2)
log_label.pack(pady=5)

skill_display = tk.Label(left_frame, text="", font=("Arial", 11), bg="white", fg="black", bd=1, relief="solid", justify="left", width=45, height=7)
skill_display.pack(pady=10)

# 輸入單字發動招式區
input_frame = tk.Frame(left_frame, bg="#f5f5f5")
input_frame.pack(pady=5)
tk.Label(input_frame, text="請輸入招式中文:", font=("Arial", 11), bg="#f5f5f5").grid(row=0, column=0, padx=5)
input_entry = tk.Entry(input_frame, font=("Arial", 12), width=12)
input_entry.grid(row=0, column=1, padx=5)
input_entry.bind("<Return>", lambda event: cast_attack())

attack_btn = tk.Button(left_frame, text="💥 發動招式", font=("Arial", 12, "bold"), bg="#ff4d4d", fg="white", width=18, command=cast_attack)
attack_btn.pack(pady=5)


# --- 右側：世界地圖與 40 週控制面板 ---
right_frame = tk.LabelFrame(root, text=" 🗺️ 控制面板與特訓區 ", font=("Arial", 11, "bold"), bg="#fff3e0", fg="#e65100", bd=2, relief="groove")
right_frame.pack(side="right", padx=15, pady=20, fill="both", expand=True)

# 下拉選單：切換 40 週進度
tk.Label(right_frame, text="📚 選擇本週背誦進度 (40週/2000字)", font=("Arial", 10, "bold"), bg="#fff3e0", fg="#333").pack(pady=10)

week_options = [f"第 {w} 週" for w in range(1, 41)]
week_combobox = ttk.Combobox(right_frame, values=week_options, state="readonly", width=15, font=("Arial", 11))
week_combobox.set(selected_week) 
week_combobox.pack(pady=5)
week_combobox.bind("<<ComboboxSelected>>", on_week_change)

tk.Label(right_frame, text="-----------------------------------", bg="#fff3e0", fg="#ccc").pack(pady=10)
tk.Label(right_frame, text="🌲 野生高壓特訓草叢", font=("Arial", 10, "bold"), bg="#fff3e0", fg="#333").pack(pady=5)

# 野生特訓區 5 大草叢按鈕
zones = [("🔥 1~10級 草叢特訓", "1-10"), 
         ("🔥 11~20級 森林特訓", "11-20"), 
         ("🔥 21~30級 洞穴特訓", "21-30"), 
         ("🔥 31~40級 火山特訓", "31-40"), 
         ("🔥 41~50級 遺蹟特訓", "41-50")]

for text, z_range in zones:
    btn = tk.Button(right_frame, text=text, font=("Arial", 10), bg="white", width=20, pady=4,
                    command=lambda r=z_range: enter_wild_zone(r))
    btn.pack(pady=6)

# 切換回主線的按鈕
return_btn = tk.Button(right_frame, text="🏆 回到主線 13 關故事挑戰", font=("Arial", 11, "bold"), bg="#1976d2", fg="white", width=20, pady=8, command=quit_wild_zone)
return_btn.pack(pady=20)


# --- 啟動遊戲主迴圈 ---
load_battle()
root.mainloop()
