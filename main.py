import streamlit as st
import time
import random

st.set_page_config(page_title="🕹️ Game Mini Flappy Bird", layout="wide")
st.title("🕹️ Game Mini Flappy Bird (Giả lập)")

# ======= CSS Styling ========
st.markdown(
    """
    <style>
    .game-container {
        border: 3px dashed #FF5733;
        padding: 20px;
        border-radius: 10px;
        background-color: #fff7e6;
        font-size: 20px;
        line-height: 1.4;
    }
    .stButton>button {
        background-color: #FF5733;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        height: 40px;
        width: 100%;
    }
    .stMetric {
        font-size: 24px !important;
        color: #0099cc !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
                row += "▫️"
        st.write(row)

def flap():
    st.session_state.bird_y -= 2
    if st.session_state.bird_y < 0:
        st.session_state.bird_y = 0

# ========== Logic ==========
if st.session_state.running:
    left, center, right = st.columns([1, 6, 1])

    with right:
        if st.button("⬆️", key="flap_button"):
            flap()

    with center:
        st.markdown('<div class="game-container">', unsafe_allow_html=True)
        draw_game()
        st.markdown('</div>', unsafe_allow_html=True)
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
    if st.button("🔁 Chơi lại", use_container_width=True):
        st.session_state.bird_y = 5
        st.session_state.pipe_x = 10
        st.session_state.gap_y = random.randint(2, 7)
        st.session_state.score = 0
        st.session_state.running = True
        st.rerun()
