import streamlit as st
from pathlib import Path
from PIL import Image
from lib.config import load_config

# Try to enable HEIC support
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIC_ENABLED = True
except Exception:
    HEIC_ENABLED = False

st.set_page_config(page_title="Gallery — Passport Powell", page_icon="🖼️", layout="wide")
st.title("Gallery")

st.info("Gallery has been merged into the Trips page. Use the Trips page tabs for Albums and All Photos.")
