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
back_image = Image.open("back.jpg")

card_folder = "cards"
card_files = [f for f in os.listdir(card_folder) if f.endswith((".jpg", ".jpeg", ".png"))]

if len(card_files) < 4:
    st.error("Not enough cards in the deck (need at least 4).")
    st.stop()

# -------------------- SESSION STATE SETUP --------------------
# Initialize deck, used cards set, and current revealed cards if not already in session state
if "deck" not in st.session_state:
    st.session_state.deck = card_files.copy()
    random.shuffle(st.session_state.deck)
    st.session_state.used_cards = set()
    st.session_state.utopia_current = None
    st.session_state.dystopia_current = None

# -------------------- DRAW FUNCTION --------------------
def draw_card(side):
    # Calculate which cards have not been used yet
    unused_cards = list(set(st.session_state.deck) - st.session_state.used_cards)

    # If all cards have been used, reset used_cards and reshuffle deck
    if not unused_cards:
        st.session_state.used_cards.clear()
        random.shuffle(st.session_state.deck)
        unused_cards = st.session_state.deck.copy()

    # Pick a random card from unused cards
    card = random.choice(unused_cards)

    # Mark the card as used
    st.session_state.used_cards.add(card)

    # Update the current revealed card for the respective side
    if side == "utopia":
        st.session_state.utopia_current = card
    elif side == "dystopia":
        st.session_state.dystopia_current = card

# -------------------- PAGE LAYOUT --------------------
cols = st.columns(4)

# --- UTOPIA SIDE ---
with cols[0]:
    st.image(back_image, use_container_width=True)
    st.markdown("<div style='text-align: center; font-weight: bold;'>Utopia (Next)</div>", unsafe_allow_html=True)
    if st.button("🌿 Reveal UTOPIAN card", key="reveal_utopia"):
        draw_card("utopia")

with cols[1]:
    if st.session_state.utopia_current:
        card_path = os.path.join(card_folder, st.session_state.utopia_current)
        st.image(Image.open(card_path), use_container_width=True)
    else:
        st.empty()
    st.markdown("<div style='text-align: center; font-weight: bold;'>Utopia (Revealed)</div>", unsafe_allow_html=True)

# --- DYSTOPIA SIDE ---
with cols[2]:
    if st.session_state.dystopia_current:
        card_path = os.path.join(card_folder, st.session_state.dystopia_current)
        st.image(Image.open(card_path), use_container_width=True)
    else:
        st.empty()
    st.markdown("<div style='text-align: center; font-weight: bold;'>Dystopia (Revealed)</div>", unsafe_allow_html=True)

with cols[3]:
    st.image(back_image, use_container_width=True)
    st.markdown("<div style='text-align: center; font-weight: bold;'>Dystopia (Next)</div>", unsafe_allow_html=True)
    if st.button("🔥 Reveal DYSTOPIAN card", key="reveal_dystopia"):
        draw_card("dystopia")

# -------------------- RESET --------------------
if st.button("🔁 Reset the Deck"):
    st.session_state.used_cards.clear()
    random.shuffle(st.session_state.deck)
    st.session_state.utopia_current = None
    st.session_state.dystopia_current = None
