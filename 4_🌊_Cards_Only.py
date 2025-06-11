import streamlit as st
from PIL import Image
import random
import os

# Page setup
st.set_page_config(page_title="Water Futures Cards Activity", layout="centered")


# Load images
back_image = Image.open("backnew.png")
card_folder = "cardsreal"
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
        # Center-align the button using nested columns
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            if st.button(f"Draw card {positions[i]}", key=f"flip_button_{i}"):
                st.session_state.flipped_cards[i] = True

        # Show either the card or the back
        if st.session_state.flipped_cards[i]:
            card_path = os.path.join(card_folder, st.session_state.drawn_cards[i])
            card_image = Image.open(card_path)
            st.image(card_image, use_container_width=True)
        else:
            st.image(back_image, use_container_width=True)

        # Show the label under each card (always centered)
        st.markdown(
            f"<div style='text-align: center; font-size: 18px; font-weight: bold; margin-top: 6px;'>{positions[i]}</div>",
            unsafe_allow_html=True
        )


# Draw again button at the bottom
if st.button("🔁 Draw Again"):
    st.session_state.drawn_cards = random.sample(card_files, 3)
    st.session_state.flipped_cards = [False, False, False]

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
