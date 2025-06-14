import streamlit as st
import random

# ======================= HỖ TRỢ =======================
def create_deck():
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']
    deck = [rank + suit for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

def calculate_score(hand):
    score = 0
    aces = 0
    for card in hand:
        rank = card[:-1]
        if rank in ['J', 'Q', 'K']:
            score += 10
        elif rank == 'A':
            aces += 1
            score += 11
        else:
            score += int(rank)
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

def show_hand(title, hand, score, is_dealer=False, reveal=False):
    col = "#FEEBCB" if is_dealer else "#CBF5F2"
    with st.container():
        st.markdown(f"""
            <div style="background-color:{col}; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                <h5>{title}</h5>
                <p style="font-size: 24px;">{" | ".join(hand) if reveal or not is_dealer else "🂠 | " + hand[1]}</p>
                <strong>Điểm: {score if reveal or not is_dealer else '??'} </strong>
            </div>
        """, unsafe_allow_html=True)

# ======================= GIAO DIỆN =======================

st.set_page_config(page_title="🃏 Xì Dách - Blackjack", layout="centered")
st.markdown("<h1 style='text-align: center; color: #FFC107;'>🃏 Xì Dách (Blackjack)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Hãy cố gắng đạt càng gần 21 điểm càng tốt. Nhưng đừng quá 21 nhé!</p>", unsafe_allow_html=True)

# ==== INIT SESSION ====
if "deck" not in st.session_state:
    st.session_state.deck = create_deck()
    st.session_state.player_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.dealer_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.game_over = False
    st.session_state.message = ""

# ==== DISPLAY HAND ====
player_score = calculate_score(st.session_state.player_hand)
dealer_score = calculate_score(st.session_state.dealer_hand)

show_hand("🧑 Bạn", st.session_state.player_hand, player_score, is_dealer=False)
show_hand("🤖 Nhà cái", st.session_state.dealer_hand, dealer_score, is_dealer=True, reveal=st.session_state.game_over)

# ==== NÚT CHƠI ====
if not st.session_state.game_over:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🃏 Rút thêm bài", use_container_width=True):
            st.session_state.player_hand.append(st.session_state.deck.pop())
            player_score = calculate_score(st.session_state.player_hand)
            if player_score > 21:
                st.session_state.message = f"💥 Bạn bị quắc ({player_score} điểm)! Bạn thua!"
                st.session_state.game_over = True
    with col2:
        if st.button("✋ Dằn bài", use_container_width=True):
            # Dealer chơi
            while dealer_score < 17:
                st.session_state.dealer_hand.append(st.session_state.deck.pop())
                dealer_score = calculate_score(st.session_state.dealer_hand)

            player_score = calculate_score(st.session_state.player_hand)
            if dealer_score > 21 or player_score > dealer_score:
                st.session_state.message = f"🎉 Bạn thắng! ({player_score} vs {dealer_score})"
            elif dealer_score > player_score:
                st.session_state.message = f"😢 Bạn thua... ({player_score} vs {dealer_score})"
            else:
                st.session_state.message = f"🤝 Hòa nhau ({player_score} điểm)"
            st.session_state.game_over = True

# ==== THÔNG BÁO KẾT QUẢ ====
if st.session_state.message:
    st.markdown("---")
    st.markdown(f"<div style='text-align:center; font-size: 24px; font-weight: bold; color: green;'>{st.session_state.message}</div>", unsafe_allow_html=True)
    # ==== CHƠI LẠI ====
st.markdown("---")
if st.button("🔁 Chơi lại", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# ==== HIỂN THỊ BỘ BÀI CÒN LẠI ====
with st.expander("🗃️ Xem bộ bài còn lại"):
    remaining = st.session_state.deck
    st.markdown(f"Số lá còn lại: **{len(remaining)}**")
    if len(remaining) > 0:
        formatted = " | ".join(remaining)
        st.markdown(f"""
        <div style='background-color:#f5f5f5; padding:10px; border-radius:5px;'>
            {formatted}
        </div>
        """, unsafe_allow_html=True)


# ==== CHƠI LẠI ====
st.markdown("---")
if st.button("Ván bài mới ", use_container_width=True):
    st.session_state.clear()
    st.rerun()
