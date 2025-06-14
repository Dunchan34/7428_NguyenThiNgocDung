import streamlit as st
import random

st.set_page_config(page_title="🧩 Game Xếp Số 8 (8-Puzzle)", layout="centered")
st.title("🧩 Game Xếp Số 8")

# ========== Khởi tạo trạng thái ==========
if 'tiles' not in st.session_state:
    nums = list(range(1, 9)) + [0]  # 0 là ô trống
    random.shuffle(nums)
    st.session_state.tiles = nums

# ========== Hàm hỗ trợ ==========
def draw_board(tiles):
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            val = tiles[i * 3 + j]
            if val == 0:
                cols[j].button("", key=f"empty-{i}-{j}", disabled=True)
            else:
                if cols[j].button(str(val), key=f"btn-{i}-{j}"):
                    try_move(i, j)

def try_move(i, j):
    idx = i * 3 + j
    empty_idx = st.session_state.tiles.index(0)
    ei, ej = divmod(empty_idx, 3)
    if abs(i - ei) + abs(j - ej) == 1:
        st.session_state.tiles[empty_idx], st.session_state.tiles[idx] = (
            st.session_state.tiles[idx],
            st.session_state.tiles[empty_idx]
        )

def is_solved(tiles):
    return tiles[:-1] == list(range(1, 9))

# ========== Giao diện ==========
st.write("Click vào số bên cạnh ô trống để di chuyển.")
draw_board(st.session_state.tiles)

if is_solved(st.session_state.tiles):
    st.success("🎉 Chúc mừng! Bạn đã hoàn thành trò chơi!")

if st.button("🔁 Xáo trộn lại"):
    nums = list(range(1, 9)) + [0]
    random.shuffle(nums)
    st.session_state.tiles = nums
    st.rerun()
