import streamlit as st
from PIL import Image
import random
import os

st.set_page_config(page_title="Draw Three Cards", layout="centered")

st.title("🎴 Imagining your water future")

st.markdown("""
### 📝 Instructions

1. Click on each card to flip and reveal your draw.
2. Discuss what each card means on its own, then what it means as a placeholder for the past, the present, or the future.
3. Click **"Draw Again"** to shuffle and try a new set.

---
""")
# Load card back image
back_image = Image.open("back.jpg")

# Load card front images from folder
card_folder = "cards"
card_files = [f for f in os.listdir(card_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Initialize session state to track flips
if 'flipped_cards' not in st.session_state:
    st.session_state.drawn_cards = random.sample(card_files, 3)
    st.session_state.flipped_cards = [False, False, False]
if 'drawn_cards' not in st.session_state:
    st.session_state.drawn_cards = []

# Require at least 3 cards
if len(card_files) < 3:
    st.error("Not enough cards in the deck (need at least 3).")
else:
    # If not flipped yet, show backs
    if not st.session_state.flipped:
        st.subheader("Click a card to reveal it 🔮")
        cols = st.columns(3)
        ffor i in range(3):
    with cols[i]:
        if st.session_state.flipped_cards[i]:
            card_path = os.path.join(card_folder, st.session_state.drawn_cards[i])
            card_image = Image.open(card_path)
            st.image(card_image, use_container_width=True)
        else:
            if st.button(f"Flip Card {i+1}"):
                st.session_state.flipped_cards[i] = True
            st.image(back_image, use_container_width=True)

    else:
        st.subheader("Your Cards:")
        cols = st.columns(3)
        for i, col in enumerate(cols):
            card_path = os.path.join(card_folder, st.session_state.drawn_cards[i])
            card_image = Image.open(card_path)
            col.image(card_image, caption=st.session_state.drawn_cards[i], use_container_width=True)

        if st.button("🔁 Draw Again"):
            st.session_state.flipped = False
