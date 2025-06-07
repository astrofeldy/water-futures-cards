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
4. Double click **"Reset the Deck"** to start over with fresh cards.

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
cols = st.columns(4)

# ----- COL 0: UTOPIA DRAW BUTTON -----
with cols[0]:
    st.image(back_image, use_container_width=True)
    st.markdown("<div style='text-align: center; font-weight: bold;'>Utopia (Next)</div>", unsafe_allow_html=True)
    if st.button("🌿 Reveal UTOPIAN card", key="reveal_utopia"):
        draw_card("utopia")

# ----- COL 1: UTOPIA CARD DISPLAY -----
with cols[1]:
    if st.session_state.utopia_card:
        card_path = os.path.join(card_folder, st.session_state.utopia_card)
        st.image(Image.open(card_path), use_container_width=True)
    else:
        st.empty()
    st.markdown("<div style='text-align: center; font-weight: bold;'>Utopia (Revealed)</div>", unsafe_allow_html=True)

# ----- COL 3: DYSTOPIA DRAW BUTTON -----
with cols[3]:
    st.image(back_image, use_container_width=True)
    st.markdown("<div style='text-align: center; font-weight: bold;'>Dystopia (Next)</div>", unsafe_allow_html=True)
    if st.button("🔥 Reveal DYSTOPIAN card"):
        draw_card("dystopia")

# ----- COL 2: DYSTOPIA CARD DISPLAY -----
with cols[2]:
    if st.session_state.dystopia_card:
        card_path = os.path.join(card_folder, st.session_state.dystopia_card)
        st.image(Image.open(card_path), use_container_width=True)
    else:
        st.empty()
    st.markdown("<div style='text-align: center; font-weight: bold;'>Dystopia (Revealed)</div>", unsafe_allow_html=True)

#----troubleshoot   
#info = st.columns(4)

#with info[0]:
    #st.markdown("<div style='text-align: center; font-weight: bold;'>Unused</div>", unsafe_allow_html=True)
    #st.write(st.session_state.unused_cards)

#with info[1]:
 #   st.markdown("<div style='text-align: center; font-weight: bold;'>Used</div>", unsafe_allow_html=True)
  #  st.write(st.session_state.used_cards)

#with info[2]:
 #   st.markdown("<div style='text-align: center; font-weight: bold;'>Utopia</div>", unsafe_allow_html=True)
  #  st.write(st.session_state.utopia_card)

#with info[3]:
 #   st.markdown("<div style='text-align: center; font-weight: bold;'>Distopia</div>", unsafe_allow_html=True)
  #  st.write(st.session_state.dystopia_card)


# -------------------- RESET BUTTON --------------------
if st.button("🔁 Reset the Deck"):
    st.session_state.unused_cards = random.sample(card_files, len(card_files))
    st.session_state.used_cards = []
    st.session_state.utopia_card = None
    st.session_state.dystopia_card = None
