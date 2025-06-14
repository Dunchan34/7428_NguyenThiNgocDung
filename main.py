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
    .stButton.jump-btn>button {
        background: white;
        color: #ff4b2b;
        border-radius: 12px;
        font-weight: bold;
        font-size: 16px;
        height: 45px;
        width: 120px;
        transition: all 0.2s ease-in-out;
        border: 2px solid #ff4b2b;
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
    }
    .stButton.jump-btn>button:hover {
        transform: scale(1.05);
        background-color: #ffe3dc;
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
    st.session_state.difficulty = 1

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
                row += "⬛"
        st.write(row)

def flap():
    st.session_state.bird_y -= 2
    if st.session_state.bird_y < 0:
        st.session_state.bird_y = 0

# ========== Logic ==========
if st.session_state.running:
    # Giao diện click toàn khu vực + nút riêng
    with st.container():
        left, center, right = st.columns([1, 6, 1])
        with center:
            st.markdown('<div class="game-container">', unsafe_allow_html=True)
            draw_game()
            st.markdown('</div>', unsafe_allow_html=True)
            time.sleep(0.2)

    # Nút nhảy cố định góc dưới phải
    with st.container():
        with st.container():
            if st.button("⬆️ Nhảy lên", key="flap_click", help="Nhấn để gà nhảy", type="secondary"):
                st.session_state.jump_request = True

    # Xử lý nhảy trước gravity
    if st.session_state.jump_request:
        flap()
        st.session_state.jump_request = False

    # Tăng độ khó: sau mỗi 5 điểm tăng tốc độ (giảm delay)
    if st.session_state.score != 0 and st.session_state.score % 5 == 0:
        st.session_state.difficulty += 1

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
    time.sleep(0.2 / st.session_state.difficulty)
    st.rerun()
else:
    st.error("💥 Game Over! Bạn đạt được {} điểm.".format(st.session_state.score))
    if st.button("🔁 Chơi lại", use_container_width=True):
        st.session_state.bird_y = 5
        st.session_state.pipe_x = 10
        st.session_state.gap_y = random.randint(2, 7)
        st.session_state.score = 0
        st.session_state.running = True
        st.session_state.difficulty = 1
        st.rerun()
