import streamlit as st
from PIL import Image
import random
import os

# -------------------- PAGE SETUP --------------------
st.set_page_config(page_title="Welcome to the Water Futures Card Deck", layout="centered")
st.title("Here is where you'll find playable activities to use the 'Water Futures Cards' developed by the team at The Institute for Water Futures at The Australian National University")

st.markdown("""
## Build the story, one flip at a time!
---
""")

# -------------------- LOAD CARD FILES --------------------
card_folder = "cardsreal"
card_files = [f for f in os.listdir(card_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

if len(card_files) < 4:
    st.error("Not enough cards in the deck (need at least 4).")
    st.stop()

back_image = Image.open("backnew.png")

# -------------------- UI LAYOUT --------------------
cols = st.columns(2)

# ----- COL 0: Display card back -----
with cols[0]:
    st.image(back_image, use_container_width=True)
    st.markdown("<div style='text-align: center; font-weight: bold;'>Remaining deck</div>", unsafe_allow_html=True)


# ----- COL 2: Display one face card -----
with cols[1]:
if not card_files:
    st.error("No card images found in the folder!")
else:
    # Choose a random image on page load
    random_card = random.choice(card_files)
    card_path = os.path.join(card_folder, random_card)

    # Display the image
    st.image(Image.open(card_path), caption="Randomly drawn card", use_container_width=True)


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
