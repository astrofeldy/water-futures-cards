import streamlit as st
from PIL import Image
import random
import os

# Page setup
st.set_page_config(page_title="Water Futures Cards Activity", layout="centered")

# Title & instructions
st.title("🎴 Imagining your water future")
st.markdown("""
### 📝 Instructions

1. **Double click** the "Reveal" button below each card to flip it over.
2. Discuss together what each card means to you, as a standalone image/word. 
3. As a group, discuss how this meaning could represent a water past, present, or future (depending on the card position).
4. What story could you tell about the timeline you've revealed here? How do the past and present cards interact with the future?
5. Share back with the group the story/scenario you come up with.
##
PS: Click **"Draw Again"** to shuffle and try a new set, if you want to.

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
            if st.button(f"Reveal: {positions[i]}", key=f"flip_button_{i}"):
                st.session_state.flipped_cards[i] = True

        # Show the label under each card (always)
        st.markdown(
            f"<div style='text-align: center; font-size: 18px; font-weight: bold; margin-top: 6px;'>{positions[i]}</div>",
            unsafe_allow_html=True
        )

# Draw again button at the bottom
st.markdown("---")
if st.button("🔁 Draw Again"):
    st.session_state.drawn_cards = random.sample(card_files, 3)
    st.session_state.flipped_cards = [False, False, False]
