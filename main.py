import streamlit as st
import random
import os
from PIL import Image

# ================== CẤU HÌNH ==================
st.set_page_config(page_title="Game Tiến Lên Đơn Giản", layout="wide")

suits = ['S', 'H', 'D', 'C']  # ♠ ♥ ♦ ♣
values = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']

# ================== HỖ TRỢ ==================
def init_deck():
    return [v + s for v in values for s in suits]

def card_image(card):
    path = f"cards/{card}.png"
    if os.path.exists(path):
        return Image.open(path)
    return None

def sort_hand(hand):
    order = {v: i for i, v in enumerate(values)}
    return sorted(hand, key=lambda c: order[c[:-1]])

# ================== KHỞI TẠO ==================
if 'deck' not in st.session_state:
    st.session_state.deck = init_deck()
    random.shuffle(st.session_state.deck)
    st.session_state.player = []
    st.session_state.bot = []
    st.session_state.turn = 'player'
    st.session_state.board = []
    st.session_state.pass_bot = False
    st.session_state.pass_player = False
    for _ in range(13):
        st.session_state.player.append(st.session_state.deck.pop())
        st.session_state.bot.append(st.session_state.deck.pop())
    st.session_state.player = sort_hand(st.session_state.player)
    st.session_state.bot = sort_hand(st.session_state.bot)

# ================== GIAO DIỆN ==================
st.title("🃏 Game Tiến Lên Đơn Giản")

col1, col2 = st.columns(2)
with col1:
    st.subheader("👤 Bài của bạn")
    selected_cards = st.multiselect("Chọn bài để đánh:", st.session_state.player)
    images = [card_image(c) for c in st.session_state.player]
    st.image(images, width=60)

with col2:
    st.subheader("🤖 Bài của máy (ẩn)")
    st.write(f"Còn lại: {len(st.session_state.bot)} lá")

st.markdown("---")
st.subheader("🪙 Bài đang trên bàn:")
if st.session_state.board:
    st.image([card_image(c) for c in st.session_state.board], width=60)
else:
    st.write("Chưa có bài nào được đánh.")

# ================== NÚT ĐÁNH ==================
col3, col4, col5 = st.columns(3)
with col3:
    if st.button("🔼 Đánh"):
        if selected_cards:
            for c in selected_cards:
                st.session_state.player.remove(c)
            st.session_state.board = selected_cards.copy()
            st.session_state.turn = 'bot'
            st.session_state.pass_bot = False
            st.rerun()

with col4:
    if st.button("❌ Bỏ lượt"):
        st.session_state.pass_player = True
        st.session_state.turn = 'bot'
        st.rerun()

with col5:
    if st.button("🔁 Chơi lại"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ================== LƯỢT CỦA MÁY ==================
if st.session_state.turn == 'bot':
    # Bot sẽ đánh 1 lá nhỏ hơn bài đang trên bàn nếu có
    played = False
    for card in st.session_state.bot:
        if not st.session_state.board or values.index(card[:-1]) > values.index(st.session_state.board[-1][:-1]):
            st.session_state.bot.remove(card)
            st.session_state.board = [card]
            st.session_state.turn = 'player'
            played = True
            st.session_state.pass_player = False
            break
    if not played:
        st.session_state.pass_bot = True
        st.session_state.turn = 'player'
    st.rerun()

# ================== THẮNG ==================
if len(st.session_state.player) == 0:
    st.success("🎉 Bạn đã thắng!")
elif len(st.session_state.bot) == 0:
    st.error("💀 Bot đã thắng!")
