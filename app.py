import streamlit as st
from pathlib import Path
from PIL import Image
from lib.config import load_config

st.set_page_config(
    page_title="Passport Powell Travel Blog",
    page_icon="🧳",
    layout="wide",
)

cfg = load_config()

title = cfg.get("name", "Travel Blog")
st.title(title)

# About section
st.subheader("About")
st.write(cfg.get("about", "Add your story in config/site.json."))

# Social links
social = cfg.get("social", {})
if social:
    st.subheader("Find me online")
    cols = st.columns(len(social))
    for idx, (label, url) in enumerate(social.items()):
        with cols[idx]:
            try:
                st.link_button(label.capitalize(), url)
            except Exception:
                st.markdown(f"[{label.capitalize()}]({url})")

# Featured image (first image in assets/images if present)
images_dir = Path("assets/images")
if images_dir.exists():
    images = [p for p in images_dir.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif"}]
    if images:
        st.subheader("Featured Photo")
        try:
            st.image(Image.open(images[0]), use_container_width=True)
        except Exception:
            st.image(str(images[0]))

st.divider()
st.info("Use the sidebar to open Gallery and Videos pages.")
