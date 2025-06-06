import streamlit as st
from PIL import Image
import random
import os

# -------------------- PAGE SETUP --------------------
st.set_page_config(page_title="Tug of Futures", layout="centered")
st.title("🌏 Tug of Futures: Utopia vs. Dystopia")

st.markdown("""
### 📝 Instructions

1. Click **"Reveal Utopia"** or **"Reveal Dystopia"** to draw a card for that future.
2. Each side has its own deck (cards may match).
3. No repeats on the same side until reset.
4. Click **"Reset Decks"** to start fresh.

---
""")

# -------------------- LOAD CARDS --------------------
card_folder = "cards"
card_files = [f for f in os.listdir(card_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

if len(card_files) < 4:
    st.error("Not enough cards in the deck (need at least 4).")
    st.stop()

back_image = Image.open("back.jpg")

# -------------------- SESSION STATE SETUP --------------------
def init_deck(side):
    """Initialize shuffled deck and state for a given side"""
    st.session_state[f"{side}_unused"] = random.sample(card_files, len(card_files))
    st.session_state[f"{side}_used"] = []
    st.session_state[f"{side}_card"] = None

# On first load
if "utopia_unused" not in st.session_state:
    init_deck("utopia")
if "dystopia_unused" not in st.session_state:
    init_deck("dystopia")

# -------------------- DRAW FUNCTIONS --------------------
def draw_card(side):
    """
    Draw a card from the specified side's deck ("utopia" or "dystopia").
    Moves it from unused to used and updates display.
    """
    unused = st.session_state[f"{side}_unused"]
    used = st.session_state[f"{side}_used"]

    if not unused:
        # Reshuffle used cards into unused when empty
        st.session_state[f"{side}_unused"] = random.sample(used, len(used))
        st.session_state[f"{side}_used"] = []
        unused = st.session_state[f"{side}_unused"]

    # Draw a new card and update state
    new_card = unused.pop()
    used.append(new_card)
    st.session_state[f"{side}_card"] = new_card

# -------------------- UI LAYOUT --------------------
cols = st.columns(4)

# ---------- UTOPIA SIDE (Cols 0 & 1) ----------
with cols[0]:
    st.image(back_image, use_container_width=True)
    st.markdown("**Utopia (Next)**", unsafe_allow_html=True)
    if st.button("🌿 Reveal UTOPIAN card", key="reveal_utopia"):
        draw_card("utopia")

with cols[1]:
    card = st.session_state.get("utopia_card")
    if card:
        st.image(Image.open(os.path.join(card_folder, card)), use_container_width=True)
    else:
        st.empty()
    st.markdown("**Utopia (Revealed)**", unsafe_allow_html=True)

# ---------- DYSTOPIA SIDE (Cols 3 & 2) ----------
with cols[3]:
    st.image(back_image, use_container_width=True)
    st.markdown("**Dystopia (Next)**", unsafe_allow_html=True)
    if st.button("🔥 Reveal DYSTOPIAN card", key="reveal_dystopia"):
        draw_card("dystopia")

with cols[2]:
    card = st.session_state.get("dystopia_card")
    if card:
        st.image(Image.open(os.path.join(card_folder, card)), use_container_width=True)
    else:
        st.empty()
    st.markdown("**Dystopia (Revealed)**", unsafe_allow_html=True)

# -------------------- RESET BUTTON --------------------
if st.button("🔁 Reset Decks"):
    init_deck("utopia")
    init_deck("dystopia")
