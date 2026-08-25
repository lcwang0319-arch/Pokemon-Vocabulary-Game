import streamlit as st
import random
import os

# ==================== 1. 遊戲核心基礎資料設定 ====================
# 13 關強大的聯盟 NPC 訓練家故事關卡
MAIN_STAGES = [
    {"name": "小隊長大岩蛇", "level": 12, "hp": 80, "move": "落石", "exp_reward": 20},     
    {"name": "小隊長寶石海星", "level": 18, "hp": 95, "move": "水炮", "exp_reward": 40},   
    {"name": "小隊長雷丘", "level": 22, "hp": 110, "move": "十萬伏特", "exp_reward": 70},  
    {"name": "小隊長霸王花", "level": 26, "hp": 125, "move": "日光束", "exp_reward": 110}, 
    {"name": "小隊長末入蛾", "level": 32, "hp": 140, "move": "蟲鳴", "exp_reward": 160},   
    {"name": "小隊長胡地", "level": 38, "hp": 155, "move": "精神強念", "exp_reward": 240}, 
    {"name": "小隊長鴨嘴火獸", "level": 42, "hp": 170, "move": "大字爆炎", "exp_reward": 360},
    {"name": "小隊長鑽角犀獸", "level": 45, "hp": 185, "move": "地震", "exp_reward": 500},  
    {"name": "四大天王乘龍", "level": 52, "hp": 210, "move": "絕對零度", "exp_reward": 760}, 
    {"name": "四大天王怪力", "level": 54, "hp": 230, "move": "爆裂拳", "exp_reward": 1040},  
    {"name": "四大天王耿鬼", "level": 56, "hp": 250, "move": "暗影球", "exp_reward": 1400},  
    {"name": "四大天王快龍", "level": 60, "hp": 280, "move": "破壞光線", "exp_reward": 1900}, 
    {"name": "火箭隊總帥超夢", "level": 70, "hp": 350, "move": "精神擊破", "exp_reward": 3000}  
]

# 野生特訓區 5 大草叢（共 50 隻可捕捉野生寶可夢池）
WILD_POOL = {
    "1-10": [{"name": "綠毛蟲", "move": "撞擊"}, {"name": "小拉達", "move": "電光一閃"}, {"name": "獨角蟲", "move": "毒針"}, {"name": "波波", "move": "起風"}, {"name": "阿柏蛇", "move": "緊束"}, {"name": "皮卡丘", "move": "電擊"}, {"name": "穿山鼠", "move": "抓"}, {"name": "尼多蘭", "move": "二連踢"}, {"name": "胖丁", "move": "連環巴掌"}, {"name": "地鼠", "move": "潑沙"}],
    "11-20": [{"name": "比比鳥", "move": "烈暴風"}, {"name": "阿柏怪", "move": "溶解液"}, {"name": "巴大蝶", "move": "念力"}, {"name": "大嘴蝠", "move": "翅膀攻擊"}, {"name": "臭臭花", "move": "超級吸取"}, {"name": "派拉斯", "move": "吸血"}, {"name": "喵喵", "move": "聚寶功"}, {"name": "可達鴨", "move": "水槍"}, {"name": "蚊香蝌蚪", "move": "泡沫"}, {"name": "凱西", "move": "折彎湯匙"}],
    "21-30": [{"name": "三地鼠", "move": "泥巴炸彈"}, {"name": "風速狗", "move": "火焰輪"}, {"name": "蚊香君", "move": "連環巴掌"}, {"name": "勇基拉", "move": "幻象光線"}, {"name": "豪力", "move": "空手劈"}, {"name": "隆隆石", "move": "滾石"}, {"name": "小火馬", "move": "火焰漩渦"}, {"name": "呆呆獸", "move": "水之波動"}, {"name": "大磁怪", "move": "電擊波"}, {"name": "大舌貝", "move": "冰凍之風"}],
    "31-40": [{"name": "大鬼斯通", "move": "暗影拳"}, {"name": "火爆獸", "move": "噴射火焰"}, {"name": "水箭龜", "move": "水炮"}, {"name": "妙蛙花", "move": "藤鞭"}, {"name": "噴火龍", "move": "噴射火焰"}, {"name": "飛腿郎", "move": "飛膝踢"}, {"name": "快拳郎", "move": "音速拳"}, {"name": "雙彈瓦斯", "move": "污泥炸彈"}, {"name": "巨鉗蟹", "move": "蟹鉗錘"}, {"name": "椰蛋樹", "move": "種子炸彈"}],
    "41-50": [{"name": "化石翼龍", "move": "原始力量"}, {"name": "卡比獸", "move": "終極衝擊"}, {"name": "急凍鳥", "move": "冰凍光束"}, {"name": "閃電鳥", "move": "打雷"}, {"name": "火焰鳥", "move": "熱風"}, {"name": "九尾", "move": "大字爆炎"}, {"name": "刺甲貝", "move": "冰錐"}, {"name": "鐮刀盔", "move": "水流裂破"}, {"name": "多邊獸", "move": "三角攻擊"}, {"name": "哈克龍", "move": "龍之波動"}]
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
                st.session_state.pokeballs = int(lines[4]) if len(lines) >= 5 else 5
                st.session_state.caught_pokemon = lines[5].split(",") if len(lines) >= 6 and lines[5] else []
                st.session_state.active_partner = lines[6] if len(lines) >= 7 else "無"
        except:
            pass
            
    if "player_level" not in st.session_state:
        st.session_state.player_level = 5
        st.session_state.player_current_exp = 0
        st.session_state.current_stage = 0
        st.session_state.selected_week = "第 13 週"
        st.session_state.pokeballs = 5
        st.session_state.caught_pokemon = []
        st.session_state.active_partner = "無"
        
    st.session_state.player_max_hp = calculate_max_hp(st.session_state.player_level)
    st.session_state.player_hp = st.session_state.player_max_hp
    st.session_state.is_wild_mode = False
    st.session_state.current_enemy = MAIN_STAGES[st.session_state.current_stage].copy()
    st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
    st.session_state.battle_log = "進入戰鬥！請看中文提示，並在下方拼出正確的『英文單字』！"
    st.session_state.skills_generated = False
    st.session_state.evo_message = ""

def save_game_st():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        f.write(f"{st.session_state.player_level}\n")
        f.write(f"{st.session_state.player_current_exp}\n")
        f.write(f"{st.session_state.current_stage}\n")
        f.write(f"{st.session_state.selected_week}\n")
        f.write(f"{st.session_state.pokeballs}\n")
        f.write(f"{','.join(st.session_state.caught_pokemon)}\n")
        f.write(f"{st.session_state.active_partner}\n")

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
        st.session_state.pokeballs += 2 
        
        st.session_state.evo_message = ""
        evo_rules = {
            "綠毛蟲": (10, "鐵甲蛹"),
            "鐵甲蛹": (15, "巴大蝶"),
            "小拉達": (20, "拉達"),
            "波波": (18, "比比鳥"),
            "皮卡丘": (30, "雷丘"),
            "哈克龍": (55, "快龍")
        }
        
        for idx, p_name in enumerate(st.session_state.caught_pokemon):
            if p_name in evo_rules:
                req_lvl, target_name = evo_rules[p_name]
                if st.session_state.player_level >= req_lvl:
                    st.session_state.caught_pokemon[idx] = target_name
                    st.session_state.evo_message = f"✨ **奇蹟發生了！** 背包裡的【{p_name}】在達到對應修煉等級後，成功進化成了【**{target_name}**】！"
                    if st.session_state.active_partner == p_name:
                        st.session_state.active_partner = target_name
                    break 
                    
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
st.title("🔥 蒼炎刃鬼 - 寶可夢單字故事聯盟挑戰 🔥")

col1, col2 = st.columns(2)

with col1: 
    if not st.session_state.is_wild_mode:
        st.subheader(f"🏆 【故事關卡挑戰 NPC】第 {st.session_state.current_stage + 1} / 13 關")
    else:
        st.subheader("🌲 【野生寶可夢捕捉區】草叢深處")
        
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        st.error(f"😈 對手: {st.session_state.current_enemy['name']} (Lv.{st.session_state.current_enemy['level']})")
        st.progress(max(0.0, min(1.0, st.session_state.enemy_hp / st.session_state.current_enemy['hp'])))
        st.write(f"血量: **{st.session_state.enemy_hp}** / {st.session_state.current_enemy['hp']}")
    with b_col2:
        st.success(f"⚔️ 我方: 蒼炎刃鬼 (Lv.{st.session_state.player_level})")
        st.progress(max(0.0, min(1.0, st.session_state.player_hp / st.session_state.player_max_hp)))
        partner_tag = f" ➕ 夥伴【{st.session_state.active_partner}】" if st.session_state.active_partner != "無" else ""
        st.write(f"血量: **{st.session_state.player_hp}** / {st.session_state.player_max_hp}{partner_tag}")

    st.info(f"📢 戰鬥日誌: {st.session_state.battle_log}")

    st.write("### ⚔️ 可發動技能與綁定單字提示")
    if not st.session_state.current_round_answers:
        st.warning(f"⚠️ {st.session_state.selected_week} 尚未錄入真實單字！請從右側切換至第 13 週。")
    else:
        for s_name, (word, ans, dmg) in st.session_state.current_round_answers.items():
            st.markdown(f"**{s_name}** (威力: {dmg}) ➔ 中文意思: <span style='color:#e65100; font-size:18px; font-weight:bold;'>【 {ans} 】</span>", unsafe_allow_html=True)

    st.write("---")
    user_input = st.text_input("請輸入招式對應的正確『英文單字』並按下發動:", key="battle_input").strip().lower()
    
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        if st.button("💥 發動招式攻擊", use_container_width=True):
            if not st.session_state.current_round_answers:
                st.stop()
                
            matched_skill = None
            damage_dealt = 0
            
            for s_name, (word, ans, dmg) in st.session_state.current_round_answers.items():
                if user_input == word.lower():
                    matched_skill = s_name
                    damage_dealt = dmg
                    break
                    
            boss = st.session_state.current_enemy
            
            # === 1. 建立戰鬥回合結果彈出式視窗 ===
            @st.dialog("⚔️ 戰鬥回合結果")
            def show_battle_dialog(is_success, skill, dmg, b_name, b_move):
                if is_success:
                    st.success(f"✨ **拼字完全正確！**")
                    if st.session_state.active_partner != "無":
                        st.markdown(f"### 蒼炎刃鬼使出【**{skill}**】，首發夥伴【**{st.session_state.active_partner}**】也發動了支援協擊！")
                        st.markdown(f"🎯 聯合合擊成功對 **{b_name}** 造成了 `{dmg + 15}` 點巨額聯擊傷害！*(內含夥伴 +15 加成)*")
                    else:
                        st.markdown(f"### 蒼炎刃鬼使出了【**{skill}**】！")
                        st.markdown(f"🎯 成功對 **{b_name}** 造成了 `{dmg}` 點重創傷害！")
                else:
                    st.error(f"❌ **拼字錯誤或未命中...**")
                    st.markdown(f"### **{b_name}** 乘虛而入使用了【**{b_move}**】！")
                    st.markdown(f"💥 蒼炎刃鬼受到了 `{dmg}` 點大招傷害！")
                if st.button("確定 (Next Turn)", use_container_width=True):
                    st.rerun()

            if matched_skill:
                final_damage = damage_dealt
                if st.session_state.active_partner != "無":
                    final_damage += 15
                st.session_state.enemy_hp -= final_damage
                st.session_state.battle_log = f"✨ 答對了！蒼炎刃鬼使出【{matched_skill}】！對 {boss['name']} 造成 {final_damage} 點傷害！"
                show_battle_dialog(True, matched_skill, damage_dealt, boss['name'], boss['move'])
            else:
                if not st.session_state.is_wild_mode:
                    boss_damage = int(boss["level"] * 2.5) + 40 + random.randint(-4, 4)
                else:
                    boss_damage = int(boss["level"] * 1.8) + 20 + random.randint(-2, 2)
                st.session_state.player_hp -= boss_damage
                st.session_state.battle_log = f"❌ 拼字錯誤！Lv.{boss['level']} 的 {boss['name']} 使用了【{boss['move']}】！蒼炎刃鬼受到 {boss_damage} 點傷害！"
                show_battle_dialog(False, "", boss_damage, boss['name'], boss['move'])

            # === 2. 勝負與經驗值結算判定 ===
            if st.session_state.enemy_hp <= 0:
                exp = boss["exp_reward"]
                is_up, gap = check_level_up_st(exp)
                
                next_stage_calculated = st.session_state.current_stage
                if not st.session_state.is_wild_mode:
                    next_stage_calculated += 1
                    if next_stage_calculated >= len(MAIN_STAGES):
                        next_stage_calculated = 0

                @st.dialog("🎉 戰鬥大勝利！")
                def show_win_dialog(b_name, xp, up, lvl, next_stg):
                    st.balloons()
                    st.success(f"🏆 **太厲害了！你成功擊敗了 {b_name}！**")
                    st.markdown(f"### 📈 獲得了 `{xp}` 點修行經驗值！")
                    if up:
                        st.warning(f"🔥 **等級突破！** 蒼炎刃鬼提升了 {lvl} 級！目前等級變為：Lv.{st.session_state.player_level}")
                    if st.session_state.evo_message:
                        st.info(st.session_state.evo_message)
                        
                    if st.button("🏆 主動迎接下一關 / 下一隻怪", use_container_width=True):
                        if not st.session_state.is_wild_mode:
                            st.session_state.current_stage = next_stg
                            st.session_state.current_enemy = MAIN_STAGES[st.session_state.current_stage].copy()
                            st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
                        else:
                            st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
                        save_game_st()
                        generate_round_skills()
                        st.rerun()

                save_game_st()
                show_win_dialog(boss['name'], exp, is_up, gap, next_stage_calculated)
                
            elif st.session_state.player_hp <= 0:
                @st.dialog("💀 挑戰失敗")
                def show_lose_dialog():
                    st.error("蒼炎刃鬼失去戰鬥能力... 自動送回喬伊小姐的醫療中心補滿血。")
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

    with action_col2:
        if st.button("🔴 投擲精靈球捕捉", use_container_width=True):
            if not st.session_state.is_wild_mode:
                st.warning("⚠️ 只能在野生寶可夢捕捉區進行捕捉，故事關卡的 NPC 頭目是不能被收服的！")
            elif st.session_state.pokeballs <= 0:
                st.error("❌ 你的精靈球已經用完了！去野生區擊敗怪物或升級可以獲得精靈球。")
            else:
                boss = st.session_state.current_enemy
                hp_ratio = st.session_state.enemy_hp / boss["hp"]
                catch_rate = 0.85 if hp_ratio <= 0.3 else (0.45 if hp_ratio <= 0.7 else 0.15)
                
                weekly_words = WORD_WEEKLY_BANK.get(st.session_state.selected_week, [])
                if weekly_words:
                    catch_q_word, catch_q_ans = random.choice(weekly_words)
                    
                    @st.dialog("🔴 精靈球投擲中...")
                    def show_catch_dialog(word, ans, rate, b_name):
                        st.write(f"你對 **{b_name}** 投擲了精靈球！確認代號中...")
                        st.markdown(f"### 🎯 請拼寫考核單字：【 **{ans}** 】")
                        catch_input = st.text_input("請輸入正確英文單字:", key="catch_word_input").strip().lower()
                        
                        if st.button("確定封印收服", use_container_width=True):
                            st.session_state.pokeballs -= 1
                            if catch_input == word.lower():
                                if random.random() <= rate:
                                    st.balloons()
                                    st.success(f"✨ 嗶、嗶、嗶...登登！成功收服 **{b_name}**！已放入隊伍背包。")
                                    if b_name not in st.session_state.caught_pokemon:
                                        st.session_state.caught_pokemon.append(b_name)
                                    st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
                                else:
                                    st.error(f"💨 哎呀！{b_name} 從精靈球裡掙脫逃跑了！(捕捉機率：{int(rate*100)}%)")
                            else:
                                st.error(f"❌ 拼字錯誤！收服失敗。正確答案是【{word}】")
                            save_game_st()
                            generate_round_skills()
                            if st.button("繼續特訓 (Next)", use_container_width=True):
                                st.rerun()
                    show_catch_dialog(catch_q_word, catch_q_ans, catch_rate, boss["name"])

with col2: # ==================== 右側控制面板 ====================
    st.header("🗺️ 進度與野外特訓區")
    
    st.markdown(f"🎒 **玩家背包狀態**")
    st.markdown(f"🔴 剩餘精靈球數量： `{st.session_state.pokeballs}` 顆 | 🎖️ 當前首發隊友： **{st.session_state.active_partner}**")
    
    with st.expander(f"📜 已收服的寶可夢圖鑑管理選單"):
        if st.session_state.caught_pokemon:
            st.write("點選下方你想派上場的夥伴寶可夢：")
            
            if st.button("❌ 召回夥伴 (單獨作戰)", key="remove_partner_btn"):
                st.session_state.active_partner = "無"
                save_game_st()
                st.rerun()
                
            for idx, p_name in enumerate(st.session_state.caught_pokemon):
                if st.button(f"🎖️ 派遣【{p_name}】出場戰鬥", key=f"partner_{idx}"):
                    st.session_state.active_partner = p_name
                    save_game_st()
                    st.rerun()
        else:
                                    st.success(f"✨ 嗶、嗶、嗶...登登！成功收服 **{b_name}**！已放入隊伍背包。")
                                    if b_name not in st.session_state.caught_pokemon:
                                        st.session_state.caught_pokemon.append(b_name)
                                    st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
                                else:
                                    st.error(f"💨 哎呀！{b_name} 從精靈球裡掙脫逃跑了！(捕捉機率：{int(rate*100)}%)")
                            else:
                                st.error(f"❌ 拼字錯誤！收服失敗。正確答案是【{word}】")
                            save_game_st()
                            generate_round_skills()
                            if st.button("繼續特訓 (Next)", use_container_width=True):
                                st.rerun()
                    show_catch_dialog(catch_q_word, catch_q_ans, catch_rate, boss["name"])

with col2: # ==================== 右側控制面板 ====================
    st.header("🗺️ 進度與野外特訓區")
    
    st.markdown(f"🎒 **玩家背包狀態**")
    st.markdown(f"🔴 剩餘精靈球數量： `{st.session_state.pokeballs}` 顆 | 🎖️ 當前首發隊友： **{st.session_state.active_partner}**")
    
    with st.expander(f"📜 已收服的寶可夢圖鑑管理選單"):
        if st.session_state.caught_pokemon:
            st.write("點選下方你想派上場的夥伴寶可夢：")
            
            if st.button("❌ 召回夥伴 (單獨作戰)", key="remove_partner_btn"):
                st.session_state.active_partner = "無"
                save_game_st()
                st.rerun()
                
            for idx, p_name in enumerate(st.session_state.caught_pokemon):
                if st.button(f"🎖️ 派遣【{p_name}】出場戰鬥", key=f"partner_{idx}"):
                    st.session_state.active_partner = p_name
                    save_game_st()
                    st.rerun()
        else:
            st.write("目前背包空空如也，快去野生區抓一隻吧！")
    
    st.write("---")
    week_list = [f"第 {w} 週" for w in range(1, 41)]
    idx_saved = week_list.index(st.session_state.selected_week) if st.session_state.selected_week in week_list else 12
    chosen_week = st.selectbox("📚 選擇本週背誦進度", week_list, index=idx_saved)
    
    if chosen_week != st.session_state.selected_week:
        st.session_state.selected_week = chosen_week
        save_game_st()
        generate_round_skills()
        st.rerun()
        
    st.write("---")
    st.write("🌲 **點擊進入野生寶可夢捕捉區：**")
    
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
    if st.button("🏆 回到故事挑戰 (與 NPC 對戰)", use_container_width=True):
        st.session_state.is_wild_mode = False
        st.session_state.current_enemy = MAIN_STAGES[st.session_state.current_stage].copy()
        st.session_state.enemy_hp = st.session_state.current_enemy["hp"]
        generate_round_skills()
        st.rerun()
