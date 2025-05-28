import streamlit as st
from PIL import Image
import random
import os

# Page setup
st.set_page_config(page_title="Draw Three Cards", layout="centered")

# Optional styling to hide the form submit button borders
st.markdown("""
    <style>
    button[kind="formSubmit"] {
        border: none;
        background-color: transparent;
        height: 0px;
        padding: 0;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title & instructions
st.title("🎴 Imagining your water future")
st.markdown("""
### 📝 Instructions

1. Click on each card to flip and reveal your draw.
2. Discuss what each card means on its own, then what it means as a placeholder for the past, the present, or the future.
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

# Session state for drawn cards and flip status
if 'drawn_cards' not in st.session_state:
    st.session_state.drawn_cards = random.sample(card_files, 3)
    st.session_state.flipped_cards = [False, False, False]

# Display cards
st.subheader("Click a card to reveal it 🔮")
cols = st.columns(3)
positions = ["Past", "Present", "Future"]

for i in range(3):
    with cols[i]:
        if st.session_state.flipped_cards[i]:
            card_path = os.path.join(card_folder, st.session_state.drawn_cards[i])
            card_image = Image.open(card_path)
            st.image(card_image, use_container_width=True)
        else:
            with st.form(key=f"form_{i}"):
                st.image(back_image, use_container_width=True)
                flipped = st.form_submit_button("")
                if flipped:
                    st.session_state.flipped_cards[i] = True

        # Always show label underneath
        label = positions[i]
        st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: bold; margin-top: 8px;'>{label}</div>", unsafe_allow_html=True)

# Draw again button
if st.button("🔁 Draw Again"):
    st.session_state.drawn_cards = random.sample(card_files, 3)
    st.session_state.flipped_cards = [False, False, False]
