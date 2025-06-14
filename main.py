import streamlit as st
import time
import random

st.set_page_config(page_title="🕹️ Game Mini Flappy Bird", layout="wide")
st.markdown("""
    <style>
    body {
        background: linear-gradient(to bottom, #fbc2eb 0%, #a6c1ee 100%);
    }
    .game-container {
        border: 4px solid #ff4b1f;
        padding: 25px;
        border-radius: 15px;
        background-color: #ffffffcc;
        font-size: 22px;
        line-height: 1.6;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
        cursor: pointer;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        color: white;
        border-radius: 12px;
        font-weight: bold;
        font-size: 16px;
        height: 45px;
        width: 100%;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    .stMetric {
        font-size: 28px !important;
        color: #2b5876 !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""<h1 style='text-align: center; color: #ff416c;'>🐤 Game Mini Flappy Bird</h1>""", unsafe_allow_html=True)

# ========== Khởi tạo trạng thái ==========
if 'bird_y' not in st.session_state:
    st.session_state.bird_y = 5
    st.session_state.gravity = 1
    st.session_state.pipe_x = 10
    st.session_state.gap_y = random.randint(2, 7)
    st.session_state.score = 0
    st.session_state.running = True
    st.session_state.jump_request = False

# ========== Hàm vẽ ==========
def draw_game():
    for y in range(10):
        row = ""
        for x in range(10):
            if x == 2 and y == st.session_state.bird_y:
                row += "🐤"
            elif x == st.session_state.pipe_x and not (st.session_state.gap_y <= y <= st.session_state.gap_y+2):
                row += "🌵"
            else:
                row += "⬜"
        st.write(row)

def flap():
    st.session_state.bird_y -= 2
    if st.session_state.bird_y < 0:
        st.session_state.bird_y = 0

# ========== Logic ==========
if st.session_state.running:
    # Click bất kỳ đâu trên khung game để gà nhảy
    container = st.empty()
    if container.button("", key="flap_click", help="Nhấp để con gà nhảy", use_container_width=True):
        st.session_state.jump_request = True

    left, center, right = st.columns([1, 6, 1])

    with center:
        st.markdown('<div class="game-container">', unsafe_allow_html=True)
        draw_game()
        st.markdown('</div>', unsafe_allow_html=True)
        time.sleep(0.2)

    # Xử lý nhảy trước gravity
    if st.session_state.jump_request:
        flap()
        st.session_state.jump_request = False

    # Cập nhật trạng thái game
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
