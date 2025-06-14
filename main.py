import streamlit as st
import time
import random

st.set_page_config(page_title="⚽ Game Đánh Banh", layout="centered")
st.title("⚽ Game Đánh Banh Chạy Chạy")

# ========== Khởi tạo trạng thái ==========
if 'ball_position' not in st.session_state:
    st.session_state.score = 0
    st.session_state.ball_position = random.randint(0, 4)
    st.session_state.running = True

# ========== Hiển thị bảng ==========
def draw_field():
    cols = st.columns(5)
    for i in range(5):
        if i == st.session_state.ball_position:
            cols[i].button("⚽", key=f"ball-{i}", on_click=hit_ball, args=(i,))
        else:
            cols[i].button("", key=f"empty-{i}", disabled=True)

def hit_ball(pos):
    if pos == st.session_state.ball_position:
        st.session_state.score += 1
        st.session_state.ball_position = random.randint(0, 4)
    else:
        st.session_state.running = False

# ========== Vòng lặp ==========
if st.session_state.running:
    draw_field()
    st.metric("🏆 Điểm số", st.session_state.score)
else:
    st.error("💥 Trượt rồi! Kết thúc trò chơi.")
    st.metric("🏆 Tổng điểm", st.session_state.score)
    if st.button("🔁 Chơi lại"):
        st.session_state.score = 0
        st.session_state.ball_position = random.randint(0, 4)
        st.session_state.running = True
        st.rerun()
