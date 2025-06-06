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
if len(card_files) < 2:
    st.error("Not enough cards in the deck (need at least 2).")
    st.stop()

# -------------------- SESSION STATE --------------------
# Track current revealed cards and progress
if "utopia_index" not in st.session_state:
    st.session_state.utopia_index = 0
    st.session_state.dystopia_index = 0
    st.session_state.utopia_cards = random.sample(card_files, 2)
    st.session_state.dystopia_cards = random.sample([c for c in card_files if c not in st.session_state.utopia_cards], 2)

# -------------------- CARD DISPLAY --------------------
# Layout: Back → Face → Face → Back
cols = st.columns(4)

# UTOPIA: back of next card
with cols[0]:
    st.image(back_image, use_container_width=True)
    st.markdown("<div style='text-align: center; font-weight: bold;'>Utopia (Next)</div>", unsafe_allow_html=True)

# UTOPIA: revealed card (if any)
with cols[1]:
    if st.session_state.utopia_index > 0:
        card_path = os.path.join(card_folder, st.session_state.utopia_cards[st.session_state.utopia_index - 1])
        card_image = Image.open(card_path)
        st.image(card_image, use_container_width=True)
    else:
        st.empty()
    st.markdown("<div style='text-align: center; font-weight: bold;'>Utopia (Revealed)</div>", unsafe_allow_html=True)

# DYSTOPIA: revealed card (if any)
with cols[2]:
    if st.session_state.dystopia_index > 0:
        card_path = os.path.join(card_folder, st.session_state.dystopia_cards[st.session_state.dystopia_index - 1])
        card_image = Image.open(card_path)
        st.image(card_image, use_container_width=True)
    else:
        st.empty()
    st.markdown("<div style='text-align: center; font-weight: bold;'>Dystopia (Revealed)</div>", unsafe_allow_html=True)

# DYSTOPIA: back of next card
with cols[3]:
    st.image(back_image, use_container_width=True)
    st.markdown("<div style='text-align: center; font-weight: bold;'>Dystopia (Next)</div>", unsafe_allow_html=True)

# -------------------- INTERACTION BUTTONS --------------------
# Buttons appear under layout
utopia_reveal = st.button("🌿 Reveal UTOPIAN card", key="reveal_utopia")
dystopia_reveal = st.button("🔥 Reveal DYSTOPIAN card", key="reveal_dystopia")

# Reveal logic
if utopia_reveal and st.session_state.utopia_index < 2:
    st.session_state.utopia_index += 1

if dystopia_reveal and st.session_state.dystopia_index < 2:
    st.session_state.dystopia_index += 1

# -------------------- RESET --------------------
if st.button("🔁 Reset the Deck"):
    st.session_state.utopia_index = 0
    st.session_state.dystopia_index = 0
    st.session_state.utopia_cards = random.sample(card_files, 2)
    st.session_state.dystopia_cards = random.sample([c for c in card_files if c not in st.session_state.utopia_cards], 2)
