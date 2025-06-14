import streamlit as st
import random

st.set_page_config(page_title="Game Đánh Bài Đơn Giản", layout="wide")

# ================== INIT ==================
suits = ['♠', '♥', '♦', '♣']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Khởi tạo bộ bài
@st.cache_data(show_spinner=False)
def init_deck():
    return [v + s for v in values for s in suits]

# Tính điểm đơn giản (Xì dách logic cơ bản)
def calculate_score(hand):
    score = 0
    aces = 0
    for card in hand:
        v = card[:-1]
        if v in ['J', 'Q', 'K']:
            score += 10
        elif v == 'A':
            aces += 1
        else:
            score += int(v)

    for _ in range(aces):
        score += 11 if score + 11 <= 21 else 1

    return score

# ================== SESSION ==================
if 'deck' not in st.session_state:
    st.session_state.deck = init_deck()
    random.shuffle(st.session_state.deck)
    st.session_state.player = []
    st.session_state.dealer = []
    st.session_state.game_over = False
    st.session_state.message = ""

# ================== GAME LOGIC ==================
def deal_card(to_whom):
    if st.session_state.deck:
        card = st.session_state.deck.pop()
        to_whom.append(card)

def reset_game():
    st.session_state.deck = init_deck()
    random.shuffle(st.session_state.deck)
    st.session_state.player = []
    st.session_state.dealer = []
    st.session_state.game_over = False
    st.session_state.message = ""

def check_winner():
    p_score = calculate_score(st.session_state.player)
    d_score = calculate_score(st.session_state.dealer)

    if p_score > 21:
        return "❌ Bạn quá 21 điểm! Dealer thắng."
    elif d_score > 21:
        return "✅ Dealer quá 21 điểm! Bạn thắng."
    elif st.session_state.game_over:
        if p_score > d_score:
            return "🏆 Bạn thắng với {} điểm!".format(p_score)
        elif p_score < d_score:
            return "😥 Bạn thua! Dealer {} điểm.".format(d_score)
        else:
            return "🤝 Hòa điểm!"
    return ""

# ================== UI ==================
st.title("🃏 Game Xì Dách Đơn Giản")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🧍 Bài của bạn")
    st.markdown(" ".join(st.session_state.player))
    st.write("Điểm: ", calculate_score(st.session_state.player))

with col2:
    st.subheader("🧠 Dealer")
    if st.session_state.game_over:
        st.markdown(" ".join(st.session_state.dealer))
        st.write("Điểm: ", calculate_score(st.session_state.dealer))
    else:
        st.markdown(f"{st.session_state.dealer[0]} ❓")

st.markdown("---")

# ==== GAME BUTTONS ====
if not st.session_state.player:
    deal_card(st.session_state.player)
    deal_card(st.session_state.dealer)
    deal_card(st.session_state.player)
    deal_card(st.session_state.dealer)

# Hành động
btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1:
    if st.button("🃙 Rút bài"):
        deal_card(st.session_state.player)
        st.session_state.message = check_winner()

with btn_col2:
    if st.button("🛑 Dừng lại"):
        st.session_state.game_over = True
        while calculate_score(st.session_state.dealer) < 17:
            deal_card(st.session_state.dealer)
        st.session_state.message = check_winner()

with btn_col3:
    if st.button("🔁 Chơi lại"):
        reset_game()
        st.rerun()

# Thông báo kết quả
if st.session_state.message:
    st.markdown(f"<h3 style='color:green'>{st.session_state.message}</h3>", unsafe_allow_html=True)

# Bộ bài còn lại
with st.expander("📦 Bộ bài còn lại"):
    st.write("Số lá còn lại:", len(st.session_state.deck))
    st.markdown(" | ".join(st.session_state.deck))
