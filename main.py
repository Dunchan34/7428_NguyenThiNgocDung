import streamlit as st
import random

# ======================= HỖ TRỢ =======================

def create_deck():
    """Tạo bộ bài gồm 52 lá"""
    suits = ['♠', '♥', '♦', '♣']
    ranks = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']
    deck = [rank + suit for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

def calculate_score(hand):
    """Tính điểm của tay bài"""
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
    # Nếu bị "quắc" và có A, đổi A thành 1
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

def show_hand(title, hand):
    st.markdown(f"**{title}**: {' | '.join(hand)} ({calculate_score(hand)} điểm)")

# ======================= UI STREAMLIT =======================

st.set_page_config(page_title="🃏 Xì Dách - Blackjack", layout="centered")
st.title("🃏 Xì Dách (Blackjack) với Máy")

# Khởi tạo trò chơi
if "deck" not in st.session_state:
    st.session_state.deck = create_deck()
    st.session_state.player_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.dealer_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.game_over = False
    st.session_state.message = ""

# Hiển thị tay bài
show_hand("Bạn", st.session_state.player_hand)
if st.session_state.game_over:
    show_hand("Nhà cái", st.session_state.dealer_hand)
else:
    st.markdown("**Nhà cái**: 🂠 | " + st.session_state.dealer_hand[1])

# Nút điều khiển
col1, col2 = st.columns(2)
with col1:
    if st.button("Rút thêm bài 🃏") and not st.session_state.game_over:
        st.session_state.player_hand.append(st.session_state.deck.pop())
        player_score = calculate_score(st.session_state.player_hand)
        if player_score > 21:
            st.session_state.message = f"💥 Bạn bị quắc ({player_score} điểm)! Bạn thua!"
            st.session_state.game_over = True

with col2:
    if st.button("Dằn bài ✋") and not st.session_state.game_over:
        # Dealer chơi
        dealer_score = calculate_score(st.session_state.dealer_hand)
        while dealer_score < 17:
            st.session_state.dealer_hand.append(st.session_state.deck.pop())
            dealer_score = calculate_score(st.session_state.dealer_hand)

        # So điểm
        player_score = calculate_score(st.session_state.player_hand)
        if dealer_score > 21 or player_score > dealer_score:
            st.session_state.message = f"🎉 Bạn thắng! ({player_score} vs {dealer_score})"
        elif dealer_score > player_score:
            st.session_state.message = f"😢 Bạn thua... ({player_score} vs {dealer_score})"
        else:
            st.session_state.message = f"🤝 Hòa nhau ({player_score} điểm)"
        st.session_state.game_over = True

# Kết quả
if st.session_state.message:
    st.markdown("---")
    st.markdown(f"### {st.session_state.message}")

# Nút chơi lại
if st.button("🔁 Chơi lại"):
    st.session_state.clear()
    st.experimental_rerun()
