import streamlit as st
import time
import random

st.set_page_config(page_title="🕹️ Game Mini Flappy Bird", layout="centered")
st.title("🕹️ Game Mini Flappy Bird (Giả lập)")

# ========== Khởi tạo trạng thái ==========
if 'bird_y' not in st.session_state:
    st.session_state.bird_y = 5
    st.session_state.gravity = 1
    st.session_state.pipe_x = 10
    st.session_state.gap_y = random.randint(2, 7)
    st.session_state.score = 0
    st.session_state.running = True

# ========== Hàm vẽ ==========
def draw_game():
    for y in range(10):
        row = ""
        for x in range(10):
            if x == 2 and y == st.session_state.bird_y:
                row += "🐤"
            elif x == st.session_state.pipe_x and not (st.session_state.gap_y <= y <= st.session_state.gap_y+2):
                row += "🟩"
            else:
                row += "▫️"  # thay vì ⬛
        st.write(row)

def flap():
    st.session_state.bird_y -= 2
    if st.session_state.bird_y < 0:
        st.session_state.bird_y = 0

# ========== Logic ==========
if st.session_state.running:
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("⬆️ Bay lên"):
            flap()

    with col2:
        draw_game()
        time.sleep(0.2)

    # Update game state
    st.session_state.bird_y += st.session_state.gravity
    st.session_state.pipe_x -= 1

    if st.session_state.pipe_x < 0:
        st.session_state.pipe_x = 10
        st.session_state.gap_y = random.randint(2, 7)
        st.session_state.score += 1

    # Kiểm tra va chạm
    if (st.session_state.pipe_x == 2 and
        not (st.session_state.gap_y <= st.session_state.bird_y <= st.session_state.gap_y + 2)) \
        or st.session_state.bird_y >= 10:
        st.session_state.running = False

    st.metric("🏆 Điểm", st.session_state.score)
    st.rerun()
else:
    st.error("💥 Game Over! Bạn đạt được {} điểm.".format(st.session_state.score))
    if st.button("🔁 Chơi lại"):
        st.session_state.bird_y = 5
        st.session_state.pipe_x = 10
        st.session_state.gap_y = random.randint(2, 7)
        st.session_state.score = 0
        st.session_state.running = True
        st.rerun()
