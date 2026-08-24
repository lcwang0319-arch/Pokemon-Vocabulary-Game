import streamlit as st
import random
import os

# ==================== 1. 遊戲資料設定 ====================
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
    "41-50": [{"name": "化石翼龍", "move": "原始力量"}, {"name": "卡比獸", "move": "終極衝擊"}, {"name": "急凍鳥", "move": "冰凍光束"}, {"name": "閃電鳥", "move": "打雷"}, {"name": "火焰鳥", "move": "熱風"}, {"name": "九尾", "move": "大字爆炎"}, {"name": "刺甲貝", "move": "冰錐"}, {"name": "鐮刀盔", "move": "水流裂破"}, {"name": "多邊獸", "move": "三角攻擊"}, {"name": "哈克龍", "move": "龍之波動"} ]
}

BASE_SKILLS = {"🔥 悔念劍": 40, "👻 暗影衝擊": 30, "⚡ 蓄能焰襲": 20, "🔮 精神利刃": 25}

WORD_WEEKLY_BANK = {}
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

for week in range(1, 41):
    WORD_WEEKLY_BANK[f"第 {week} 週"] = []
WORD_WEEKLY_BANK["第 13 週"] = [(item["en"], item["zh"]) for item in WEEK_13_INPUT]

# ==================== 2. 存檔與狀態管理 ====================
SAVE_FILE = "pokemon_save.txt"

def calculate_max_hp(lvl):
    if lvl >= 100: return 410
    return 50 + (lvl - 5) * 4

# 初始化狀態
if "player_level" not in st.session_state:
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                st.session_state.player_level = int(lines[0])
                st.session_state.player_current_exp = int(lines[1])
                st.session_state.current_stage = int(lines[2])
                st.session_state.selected_week = lines[3]
        except:
            pass
            
    if "player_level" not in st.session_state:
        st.session_state.player_level = 5
        st.session_state.player_current_exp = 0
        st.session_state.current_stage = 0
        st.session_state.selected_week = "第 13 週"
        
    st.session_state.player_max_hp = calculate_max_hp(st.session_state.player_level)
    st.session_state.player_hp = st.session_state.player_max_hp
    st.session_state.is_wild_mode = False
    st.session_state.current_enemy = MAIN_STAGES[st.session_state.current_stage].copy()
    st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
    st.session_state.battle_log = "進入戰鬥！請看中文，並在下方輸入正確的『英文單字』！"
    st.session_state.skills_generated = False

def save_game_st():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        f.write(f"{st.session_state.player_level}\n")
        f.write(f"{st.session_state.player_current_exp}\n")
        f.write(f"{st.session_state.current_stage}\n")
        f.write(f"{st.session_state.selected_week}\n")

def check_level_up_st(added_exp):
    st.session_state.player_current_exp += added_exp
    old_lvl = st.session_state.player_level
    while st.session_state.player_level < 100:
        next_req = ((st.session_state.player_level + 1) - 4) ** 2 * 50
        if st.session_state.player_current_exp >= next_req:
            st.session_state.player_level += 1
        else:
            break
    if st.session_state.player_level > old_lvl:
        st.session_state.player_max_hp = calculate_max_hp(st.session_state.player_level)
        st.session_state.player_hp = st.session_state.player_max_hp
        return True, st.session_state.player_level - old_lvl
    st.session_state.player_hp = st.session_state.player_max_hp
    return False, 0

def generate_round_skills():
    weekly_words = WORD_WEEKLY_BANK.get(st.session_state.selected_week, [])
    if len(weekly_words) < 4:
        st.session_state.current_round_answers = {}
        return
    pool_copy = weekly_words.copy()
    random.shuffle(pool_copy)
    
    st.session_state.current_round_answers = {}
    for i, (skill_name, base_dmg) in enumerate(BASE_SKILLS.items()):
        word, ans = pool_copy[i]
        bonus = int((st.session_state.player_level - 5) * 0.5)
        st.session_state.current_round_answers[skill_name] = (word, ans, base_dmg + bonus)
    st.session_state.skills_generated = True

if not st.session_state.skills_generated or "current_round_answers" not in st.session_state:
    generate_round_skills()

# ==================== 3. Streamlit 網頁佈局 ====================
st.set_page_config(page_title="蒼炎刃鬼 - 單字聯盟挑戰", layout="wide")
st.title("🔥 蒼炎刃鬼 - 寶可夢單字聯盟大挑戰 🔥")

col1, col2 = st.columns(2)

with col1: # 左側戰鬥面板
    if not st.session_state.is_wild_mode:
        st.subheader(f"🏆 【主線故事】第 {st.session_state.current_stage + 1} / 13 關")
    else:
        st.subheader("🌲 【野生特訓區】草叢深處")
        
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        st.error(f"😈 敵方: {st.session_state.current_enemy['name']} (Lv.{st.session_state.current_enemy['level']})")
        st.progress(max(0.0, min(1.0, st.session_state.enemy_hp / st.session_state.current_enemy['hp'])))
        st.write(f"血量: **{st.session_state.enemy_hp}** / {st.session_state.current_enemy['hp']}")
    with b_col2:
        st.success(f"⚔️ 我方: 蒼炎刃鬼 (Lv.{st.session_state.player_level})")
        st.progress(max(0.0, min(1.0, st.session_state.player_hp / st.session_state.player_max_hp)))
        st.write(f"血量: **{st.session_state.player_hp}** / {st.session_state.player_max_hp} | 累積 EXP: **{st.session_state.player_current_exp}**")

    st.info(f"📢 戰鬥日誌: {st.session_state.battle_log}")

    st.write("### ⚔️ 可發動技能與綁定單字提示")
    if not st.session_state.current_round_answers:
        st.warning(f"⚠️ {st.session_state.selected_week} 尚未錄入真實單字！請從右側切換至第 13 週。")
    else:
        for s_name, (word, ans, dmg) in st.session_state.current_round_answers.items():
            st.markdown(f"**{s_name}** (威力: {dmg}) ➔ 中文意思: <span style='color:#e65100; font-size:18px; font-weight:bold;'>【 {ans} 】</span>", unsafe_allow_html=True)

    st.write("---")
    user_input = st.text_input("請輸入招式對應的正確『英文單字』並按下發動:", key="battle_input").strip().lower()
    
    if st.button("💥 發動招式攻擊", use_container_width=True):
        if not st.session_state.current_round_answers:
            st.stop()
            
        matched_skill = None
        damage_dealt = 0
        
        # === 1. 建立網頁版強制彈出式視窗的對話框函式 ===
        @st.dialog("⚔️ 戰鬥回合結果")
        def show_battle_dialog(is_success, skill, dmg, b_name, b_move):
            if is_success:
                st.success(f"✨ **拼字完全正確！**")
                st.markdown(f"### 蒼炎刃鬼使出了【**{skill}**】！")
                st.markdown(f"🎯 成功對野生 **{b_name}** 造成了 `{dmg}` 點重創傷害！")
            else:
                st.error(f"❌ **拼字錯誤或未命中...**")
                st.markdown(f"### 野生 **{b_name}** 乘虛而入使用了【**{b_move}**】！")
                st.markdown(f"💥 蒼炎刃鬼受到了 `{dmg}` 點巨額傷害！")
            if st.button("確定 (Next Turn)", use_container_width=True):
                st.rerun()

        # === 2. 檢查玩家輸入的英文單字 ===
        for s_name, (word, ans, dmg) in st.session_state.current_round_answers.items():
            if user_input == word.lower():
                matched_skill = s_name
                damage_dealt = dmg
                break
                
        boss = st.session_state.current_enemy
        
        # === 3. 根據是否答對，計算扣血、更新日誌並觸發彈出視窗 ===
        if matched_skill:
            st.session_state.enemy_hp -= damage_dealt
            st.session_state.battle_log = f"✨ 答對了！蒼炎刃鬼使出【{matched_skill}】！對 {boss['name']} 造成 {damage_dealt} 點傷害！"
            show_battle_dialog(True, matched_skill, damage_dealt, boss['name'], boss['move'])
        else:
            if not st.session_state.is_wild_mode:
                boss_damage = int(boss["level"] * 2.5) + 40 + random.randint(-4, 4)
            else:
                boss_damage = int(boss["level"] * 1.8) + 20 + random.randint(-2, 2)
            st.session_state.player_hp -= boss_damage
            st.session_state.battle_log = f"❌ 拼字錯誤！Lv.{boss['level']} 的 {boss['name']} 使用了【{boss['move']}】！蒼炎刃鬼受到 {boss_damage} 點傷害！"
            show_battle_dialog(False, "", boss_damage, boss['name'], boss['move'])

        # === 4. 勝負與經驗值結算判定 ===
        if st.session_state.enemy_hp <= 0:
            exp = boss["exp_reward"]
            is_up, gap = check_level_up_st(exp)
            
            @st.dialog("🎉 戰鬥大勝利！")
            def show_win_dialog(b_name, xp, up, lvl):
                st.balloons()
                st.success(f"🏆 成功擊敗了野生 {b_name}！")
                st.write(f"📈 獲得了 `{xp}` 點經驗值！")
                if up:
                    st.warning(f"🔥 **等級突破！** 蒼炎刃鬼提升了 {lvl} 級！目前等級：Lv.{st.session_state.player_level}")
                if st.button("前前下一關 (Confirm)", use_container_width=True):
                    st.rerun()

            if not st.session_state.is_wild_mode:
                st.session_state.current_stage += 1
                if st.session_state.current_stage >= len(MAIN_STAGES):
                    st.session_state.current_stage = 0
                    st.session_state.player_level = 5
                    st.session_state.player_current_exp = 0
            
            save_game_st()
            show_win_dialog(boss['name'], exp, is_up, gap)
            
            if not st.session_state.is_wild_mode:
                st.session_state.current_enemy = MAIN_STAGES[st.session_state.current_stage].copy()
            st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
            generate_round_skills()
            
        elif st.session_state.player_hp <= 0:
            @st.dialog("💀 挑戰失敗")
            def show_lose_dialog():
                st.error("蒼炎刃鬼失去戰鬥能力... 自動送回喬意小姐的醫療中心補滿血。")
                if st.button("重新整備出發", use_container_width=True):
                    st.rerun()

            st.session_state.player_hp = st.session_state.player_max_hp
            if not st.session_state.is_wild_mode:
                st.session_state.current_stage = max(0, st.session_state.current_stage - 1)
                st.session_state.current_enemy = MAIN_STAGES[st.session_state.current_stage].copy()
            st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
            save_game_st()
            generate_round_skills()
            show_lose_dialog()
        else:
            generate_round_skills()

with col2: # ==================== 右側控制面板 ====================
    st.header("🗺️ 進度與野外特訓區")
    
    week_list = [f"第 {w} 週" for w in range(1, 41)]
    idx_saved = week_list.index(st.session_state.selected_week) if st.session_state.selected_week in week_list else 12
    chosen_week = st.selectbox("📚 選擇本週背誦進度", week_list, index=idx_saved)
    
    if chosen_week != st.session_state.selected_week:
        st.session_state.selected_week = chosen_week
        save_game_st()
        generate_round_skills()
        st.rerun()
        
    st.write("---")
    st.write("🌲 點擊進入野生草叢練功")
    
    if st.button("🌿 1~10級 草叢特訓"):
        st.session_state.is_wild_mode = True
        lvl = random.randint(1, 10)
        t = random.choice(WILD_POOL["1-10"])
        st.session_state.current_enemy = {"name": t["name"], "level": lvl, "hp": 35 + lvl * 3, "move": t["move"], "exp_reward": lvl * 3}
        st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
        generate_round_skills()
        st.rerun()
        
    if st.button("🌿 11~20級 森林特訓"):
        st.session_state.is_wild_mode = True
        lvl = random.randint(11, 20)
        t = random.choice(WILD_POOL["11-20"])
        st.session_state.current_enemy = {"name": t["name"], "level": lvl, "hp": 35 + lvl * 3, "move": t["move"], "exp_reward": lvl * 3}
        st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
        generate_round_skills()
        st.rerun()
        
    if st.button("🌿 21~30級 洞穴特訓"):
        st.session_state.is_wild_mode = True
        lvl = random.randint(21, 30)
        t = random.choice(WILD_POOL["21-30"])
        st.session_state.current_enemy = {"name": t["name"], "level": lvl, "hp": 35 + lvl * 3, "move": t["move"], "exp_reward": lvl * 3}
        st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
        generate_round_skills()
        st.rerun()
        
    if st.button("🌿 31~40級 火山特訓"):
        st.session_state.is_wild_mode = True
        lvl = random.randint(31, 40)
        t = random.choice(WILD_POOL["31-40"])
        st.session_state.current_enemy = {"name": t["name"], "level": lvl, "hp": 35 + lvl * 3, "move": t["move"], "exp_reward": lvl * 3}
        st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
        generate_round_skills()
        st.rerun()
        
    if st.button("🌿 41~50級 遺蹟特訓"):
        st.session_state.is_wild_mode = True
        lvl = random.randint(41, 50)
        t = random.choice(WILD_POOL["41-50"])
        st.session_state.current_enemy = {"name": t["name"], "level": lvl, "hp": 35 + lvl * 3, "move": t["move"], "exp_reward": lvl * 3}
        st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
        generate_round_skills()
        st.rerun()

    st.write("---")
    if st.button("🏆 回到主線 13 關挑戰", use_container_width=True):
        st.session_state.is_wild_mode = False
        st.session_state.current_enemy = MAIN_STAGES[st.session_state.current_stage].copy()
        st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
        generate_round_skills()
        st.rerun()
