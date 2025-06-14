import streamlit as st
import random

st.set_page_config(page_title="🔫 Game Bắn Súng", layout="centered")
st.title("🔫 Game Bắn Súng Đơn Giản")

# ========== Khởi tạo trạng thái ==========
if 'target' not in st.session_state:
    st.session_state.score = 0
    st.session_state.bullets = 5
    st.session_state.target = random.randint(1, 9)

# ========== Hàm hỗ trợ ==========
def draw_targets():
    st.subheader("🎯 Chọn mục tiêu để bắn")
    cols = st.columns(3)
    for i in range(3):
        for j in range(3):
            idx = i * 3 + j + 1
            if cols[j].button(f"{idx}", key=f"target-{idx}"):
                shoot(idx)

def shoot(choice):
    if st.session_state.bullets <= 0:
        return
    if choice == st.session_state.target:
        st.success(f"🎉 Trúng mục tiêu số {choice}! +1 điểm")
        st.session_state.score += 1
        st.session_state.target = random.randint(1, 9)
    else:
        st.warning(f"💨 Trượt rồi! Mục tiêu không phải số {choice}.")
    st.session_state.bullets -= 1

# ========== Hiển thị thông tin ==========
st.metric("💥 Đạn còn", st.session_state.bullets)
st.metric("🏆 Điểm số", st.session_state.score)

if st.session_state.bullets > 0:
    draw_targets()
else:
    st.error("Hết đạn rồi! 😢")
    if st.button("🔁 Chơi lại"):
        st.session_state.score = 0
        st.session_state.bullets = 5
        st.session_state.target = random.randint(1, 9)
        st.rerun()
