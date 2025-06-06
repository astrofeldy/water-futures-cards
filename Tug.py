import streamlit as st
from PIL import Image
import random
import os

# -------------------- PAGE SETUP --------------------
st.set_page_config(page_title="Tug of Futures", layout="centered")

st.title("🌏 Tug of Futures: Utopia vs. Dystopia")

st.markdown("""
### 📝 Instructions

This warm-up invites you to explore imagined futures:

1. Click **"Reveal Utopia"** to flip one hopeful card.
2. Click **"Reveal Dystopia"** to flip one challenging or cautionary card.
3. Reflect: What tensions emerge between them? How might both influence the future of water?
4. Click **"Reset the Deck"** to start over with fresh cards.

---
""")

# -------------------- IMAGE SETUP --------------------
# Load the back-of-card image
back_image = Image.open("back.jpg")

# Get list of available card images
card_folder = "cards"
card_files = [f for f in os.listdir(card_folder) if f.endswith((".jpg", ".jpeg", ".png"))]

# Check for enough cards to draw from
if len(card_files) < 4:
    st.error("Not enough cards in the deck (need at least 4).")
    st.stop()

# -------------------- SESSION STATE --------------------
# Setup session state for independent draws
if "available_cards" not in st.session_state:
    st.session_state.available_cards = random.sample(card_files, len(card_files))
    st.session_state.utopia_used = []
    st.session_state.dystopia_used = []


# -------------------- DRAW FUNCTIONS --------------------
def draw_card(target):
    if not st.session_state.available_cards:
        # Reshuffle if deck is exhausted
        all_used = st.session_state.utopia_used + st.session_state.dystopia_used
        st.session_state.available_cards = random.sample(all_used, len(all_used))
        st.session_state.utopia_used = []
        st.session_state.dystopia_used = []

    card = st.session_state.available_cards.pop()
    
    if target == "utopia":
        st.session_state.utopia_used.append(card)
    elif target == "dystopia":
        st.session_state.dystopia_used.append(card)


# -------------------- CARD DISPLAY --------------------
# Layout: Back → Face → Face → Back
cols = st.columns(4)

# UTOPIA: back of next card
with cols[0]:
    st.image(back_image, use_container_width=True)
    st.markdown("<div style='text-align: center; font-weight: bold;'>Utopia (Next)</div>", unsafe_allow_html=True)
    if st.button("🌿 Reveal UTOPIAN card", key="reveal_utopia"):
        draw_card("utopia")

# UTOPIA: revealed card (most recent only)
with cols[1]:
    if st.session_state.utopia_used:
        last_utopia = st.session_state.utopia_used[-1]
        st.image(Image.open(os.path.join(card_folder, last_utopia)), use_container_width=True)
    else:
        st.empty()
    st.markdown("<div style='text-align: center; font-weight: bold;'>Utopia (Revealed)</div>", unsafe_allow_html=True)

# DYSTOPIA: revealed card (most recent only)
with cols[2]:
    if st.session_state.dystopia_used:
        last_dystopia = st.session_state.dystopia_used[-1]
        st.image(Image.open(os.path.join(card_folder, last_dystopia)), use_container_width=True)
    else:
        st.empty()
    st.markdown("<div style='text-align: center; font-weight: bold;'>Dystopia (Revealed)</div>", unsafe_allow_html=True)

# DYSTOPIA: back of next card
with cols[3]:
    st.image(back_image, use_container_width=True)
    st.markdown("<div style='text-align: center; font-weight: bold;'>Dystopia (Next)</div>", unsafe_allow_html=True)
    if st.button("🔥 Reveal DYSTOPIAN card", key="reveal_dystopia"):
        draw_card("dystopia")

# -------------------- RESET --------------------
if st.button("🔁 Reset the Deck"):
    st.session_state.available_cards = random.sample(card_files, len(card_files))
    st.session_state.utopia_used = []
    st.session_state.dystopia_used = []
    st.session_state.shuffled_deck = shuffled
    st.session_state.utopia_index = 0
    st.session_state.dystopia_index = 0
