import streamlit as st
from PIL import Image
import random
import os

# Page setup
st.set_page_config(page_title="Water Futures Cards Activity", layout="centered")

# Title & instructions
st.title("🎴 Imagining a water justice future")
st.markdown(
    """
    **Before you start:** decide who is going to be the 'dealer' - one person in the breakout room needs to share their screen, and drive the below activity.  

    ### 📝 Instructions  

    1. Click the **"Draw card"** button above a card to flip it over, and discuss together what the card means to you as a standalone image/word/idea.  
    2. As a group, discuss how this meaning could represent a water justice past, present, or future (depending on the card position).  
    3. **Imagine the year 2075.** What story could you tell about the timeline you've revealed here? How do the past and present cards interact with the future, 50 years from now?  What does this future look like?
    4. Capture your story in our class <a href="https://docs.google.com/presentation/d/1RzSkivJvGuMd_TTnFqIq3MPWWW_SR43ZdNxIboRI8-g/edit?usp=sharing" target="_blank">slides</a>. Feel free to copy/paste any kind of other visual material that helps to tell your story.  
    5. Share back with the group the story/scenario you come up with.  

    #### **Tips!**
    <ul>
        <li>Stories of the future come to life when there are <i>people</i> involved. Who is in your future? What does their life look like?</li>
        <li>If jumping straight to 50 years feels tricky, try to imagine 10 or 20 years in the future, <i>first</i>. Then jump another 10 years from there, and so on.</li>
        <li>When you're unsure about a card, it's meaning, or how it comes to life, <i>lean in to this curiosity</i>. Chat more about the possibilities of interpretation, and go back over it a few times if you need to.</li>
        <li>What pictures, songs, poems, or other media bring this future to life? Include these in your story, too.</li>
    </ul>

    PS: Double click **"Draw Again"** to shuffle and try a new set, if you want to.  

    ---
    """,
    unsafe_allow_html=True
)


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
positions = ["Prompt 1", "Prompt 2", "Prompt 3"]
cols = st.columns(3)

# Display cards + reveal buttons
for i in range(3):
    with cols[i]:
        # Center-align the button using nested columns
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            if st.button(f"Draw: {positions[i]}", key=f"flip_button_{i}"):
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

st.markdown("---")

# Add a text box
user_message = st.text_area("Use this text box to take notes, if you want to:", height=150)

st.markdown("---")

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
