import streamlit as st
from lib.config import load_config, save_config

st.set_page_config(page_title="Videos — Passport Powell", page_icon="📹")
st.title("Videos")

cfg = load_config()
videos = cfg.get("youtube_videos", [])

if not videos:
    st.info("Add YouTube video URLs below to feature them here.")

for url in videos:
    st.video(url)

st.divider()
st.subheader("Add a YouTube video")
new_url = st.text_input("YouTube video URL (e.g., https://www.youtube.com/watch?v=...)", "")
if st.button("Add Video"):
    if new_url and new_url.startswith("http"):
        cfg.setdefault("youtube_videos", []).append(new_url)
        try:
            save_config(cfg)
            st.success("Video added! Refresh to see it listed.")
        except Exception as e:
            st.error(f"Could not save config: {e}")
    else:
        st.warning("Please enter a valid URL.")
