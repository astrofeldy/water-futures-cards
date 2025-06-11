import streamlit as st
from PIL import Image
import random
import os

# -------------------- PAGE SETUP --------------------
st.set_page_config(page_title="Exquisite Warm Up", layout="centered")
st.title("☕ Warm Up: Exquisite Corpse, Water Futures Edition")

st.markdown("""
## Build the story, one flip at a time!

Before you start: one person in the breakout room should share their screen, so that you're all looking at the same revealed cards.

### 📝 Instructions

This warm-up invites you to build a story together, using a revealed card as a prompt:

1. Click **"flip a card"** to reveal one water future card. Player 1 begins a new story by using the card to set the scene, then passes to the next player.
2. Click **"flip a card"** again to show another card, and Player 2 continues building on the story made by Player 1.
3. Continue flipping cards and telling your back-and-forth story, until the team becomes repetitive or stuck. Then start again and have another go by **double clicking** "Reset the deck".

### Reflection: 
- What was easy or difficult about this exercise?
- Were there common themes that emerged? 
---
""")

# -------------------- LOAD CARD FILES --------------------
card_folder = "cardsreal"
card_files = [f for f in os.listdir(card_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

if len(card_files) < 4:
    st.error("Not enough cards in the deck (need at least 4).")
    st.stop()

back_image = Image.open("backnew.png")

# -------------------- SETUP SESSION STATE --------------------
if "unused_cards" not in st.session_state:
    st.session_state.unused_cards = random.sample(card_files, len(card_files))  # random shuffle
    st.session_state.used_cards = []  # store all previously drawn cards
    st.session_state.utopia_card = None  # track current utopia image
    st.session_state.dystopia_card = None  # track current dystopia image
    

# -------------------- FUNCTION TO DRAW A CARD --------------------
def draw_card(for_side):
    """
    Draw one card randomly from unused_cards and assign it to the requested side.
    Side must be "utopia" or "dystopia".
    """
    if not st.session_state.unused_cards:
        # If all cards have been used, reshuffle the deck
        st.session_state.unused_cards = random.sample(st.session_state.used_cards, len(st.session_state.used_cards))
        st.session_state.used_cards = []

    # Draw one new card
    new_card = st.session_state.unused_cards.pop()
    st.session_state.used_cards.append(new_card)

    # Assign the drawn card to the correct side
    if for_side == "utopia":
        st.session_state.utopia_card = new_card
    elif for_side == "dystopia":
        st.session_state.dystopia_card = new_card

    #insert: if utopia = dystopia state, draw again

# -------------------- UI LAYOUT --------------------
cols = st.columns(2)

# ----- COL 0: UTOPIA DRAW BUTTON -----
with cols[0]:
    st.image(back_image, use_container_width=True)
    st.markdown("<div style='text-align: center; font-weight: bold;'>Remaining deck</div>", unsafe_allow_html=True)
    if st.button("🌿 CLICK: flip a card", key="reveal_utopia"):
        draw_card("utopia")

# ----- COL 1: UTOPIA CARD DISPLAY -----
with cols[1]:
    if st.session_state.utopia_card:
        card_path = os.path.join(card_folder, st.session_state.utopia_card)
        st.image(Image.open(card_path), use_container_width=True)
    else:
        st.empty()
    st.markdown("<div style='text-align: center; font-weight: bold;'>Revealed card (most recent)</div>", unsafe_allow_html=True)

# -------------------- RESET BUTTON --------------------
if st.button("🔁 Reset the Deck"):
    st.session_state.unused_cards = random.sample(card_files, len(card_files))
    st.session_state.used_cards = []
    st.session_state.utopia_card = None
    st.session_state.dystopia_card = None


#-------------------- COPYRIGHT STATEMENT ------------
st.markdown("""

<hr style="margin-top: 2em; margin-bottom: 1em;">

<div style='text-align: center; color: grey; font-size: 8px; line-height: 1;'>

<strong>© 2025 Australian National University. All rights reserved.</strong><br>
This app is intended for <em>educational use only</em> and may <strong>not</strong> be reproduced, modified, or distributed without prior written permission.<br><br>
All images are owned by the <strong>Australian National University</strong> and were created by <strong>Benjamin Coultas-Roberts</strong>.<br>
All other intellectual property, including the design of the exercise and how this app is used, is owned by the <strong>Institute for Water Futures</strong> at the Australian National University.

</div>
""", unsafe_allow_html=True)
