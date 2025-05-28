import streamlit as st
from PIL import Image
import random
import os

# Page setup
st.set_page_config(page_title="Draw Three Cards", layout="centered")

# Title & instructions
st.title("🎴 Imagining your water future")
st.markdown("""
### 📝 Instructions

1. Click the button below each card to reveal it.
2. Discuss what each card means on its own, then as a representation of the past, the present, or the future.
3. Click **"Draw Again"** to shuffle and try a new set.

---
""")

# Load images
back_image = Image.open("back.jpg")
card_folder = "cards"
card_files = [f for f in os.listdir(card_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Check if enough cards exist
if len(card_files) < 3:
    st.error("Not enough cards in the deck (need at least 3).")
    st.stop()

# Session state setup
if 'drawn_cards' not in st.session_state:
    st.session_state.drawn_cards = random.sample(card_files, 3)
    st.session_state.flipped_cards = [False, False, False]

# Card titles
positions = ["PAST", "PRESENT", "FUTURE"]
cols = st.columns(3)

# Display cards + reveal buttons
for i in range(3):
    with cols[i]:
        if st.session_state.flipped_cards[i]:
            card_path = os.path.join(card_folder, st.session_state.drawn_cards[i])
            card_image = Image.open(card_path)
            st.image(card_image, use_container_width=True)
        else:
            st.image(back_image, use_container_width=True)
            # Use a form to wrap the button and center it
