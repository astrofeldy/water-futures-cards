import streamlit as st
from PIL import Image
import random
import os

st.set_page_config(page_title="Draw Three Cards", layout="centered")

st.title("🎴 Draw Three Cards")

# Load card back image
back_image = Image.open("back.jpg")

# Load card front images from folder
card_folder = "cards"
card_files = [f for f in os.listdir(card_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Initialize session state to track flips
if 'flipped' not in st.session_state:
    st.session_state.flipped = False
if 'drawn_cards' not in st.session_state:
    st.session_state.drawn_cards = []

# Require at least 3 cards
if len(card_files) < 3:
    st.error("Not enough cards in the deck (need at least 3).")
else:
    # If not flipped yet, show backs
    if not st.session_state.flipped:
        st.subheader("Click to flip your cards:")
        cols = st.column(3)
        for col in cols:
            col.image(back_image, use_container_width=True)

        if st.button("🔮 Flip Cards"):
            st.session_state.flipped = True
            st.session_state.drawn_cards = random.sample(card_files, 3)

    else:
        st.subheader("Your Cards:")
        cols = st.column(3)
        for i, col in enumerate(cols):
            card_path = os.path.join(card_folder, st.session_state.drawn_cards[i])
            card_image = Image.open(card_path)
            col.image(card_image, caption=st.session_state.drawn_cards[i], use_container_width=True)

        if st.button("🔁 Draw Again"):
            st.session_state.flipped = False
