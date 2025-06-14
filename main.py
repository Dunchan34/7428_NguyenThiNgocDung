
import streamlit as st
import random

# Title and instructions
st.set_page_config(page_title="Trò chơi Đoán số Vui nhộn 🎮")
st.title("🎲 Trò chơi Đoán số Vui nhộn")
st.markdown("Hãy thử đoán số bí mật trong khoảng từ **1 đến 100**. Bạn có bao nhiêu lần thử để chiến thắng?")

# Initialize secret number and attempt count using session_state
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False

# User input
guess = st.number_input("Nhập số bạn đoán:", min_value=1, max_value=100, step=1, format="%d")

# Guess button
if st.button("Đoán! 🎯") and not st.session_state.game_over:
    st.session_state.attempts += 1
    if guess < st.session_state.secret_number:
        st.warning("Số bạn đoán **nhỏ hơn** số bí mật.")
    elif guess > st.session_state.secret_number:
        st.warning("Số bạn đoán **lớn hơn** số bí mật.")
    else:
        st.success(f"🎉 Chính xác rồi! Số bí mật là {st.session_state.secret_number}.")
        st.balloons()
        st.session_state.game_over = True
        st.markdown(f"🔁 Bạn đã đoán đúng sau **{st.session_state.attempts} lần**.")

# Restart button
if st.button("Chơi lại 🔁"):
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.experimental_rerun()
