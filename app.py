import streamlit as st
from PIL import Image
import random
import os
import base64  # ✅ move these to the top
from io import BytesIO

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

# Require at least 3 cards
if len(card_files) < 3:
    st.error("Not enough cards in the deck (need at least 3).")
else:
    st.subheader("Click a card to reveal it 🔮")

    cols = st.columns(3)
    positions = ["Past", "Present", "Future"]

    def image_to_base64(img):  # ✅ define this once outside the loop
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

    for i in range(3):
        with cols[i]:
            if st.session_state.flipped_cards[i]:
                card_path = os.path.join(card_folder, st.session_state.drawn_cards[i])
                card_image = Image.open(card_path)
                st.image(card_image, use_container_width=True)
            else:
                back_img_base64 = image_to_base64(back_image)
                img_html = f"<img src='data:image/png;base64,{back_img_base64}' style='width:100%; border: none;'>"
                if st.button(img_html, key=f"flip_card_{i}", use_container_width=True):
                    st.session_state.flipped_cards[i] = True

            # Always show the label under the card
            label = positions[i]
            st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: bold; margin-top: 8px;'>{label}</div>", unsafe_allow_html=True)

    if st.button("🔁 Draw Again"):
        st.session_state.drawn_cards = random.sample(card_files, 3)
        st.session_state.flipped_cards = [False, False, False]
