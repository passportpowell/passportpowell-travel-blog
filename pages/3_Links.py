import streamlit as st
from lib.config import load_config

st.set_page_config(page_title="Links — Passport Powell", page_icon="🔗")
st.title("Links")

cfg = load_config()
social = cfg.get("social", {})

if not social:
    st.info("Add social links in config/site.json.")
else:
    cols = st.columns(len(social))
    for idx, (label, url) in enumerate(social.items()):
        with cols[idx]:
            try:
                st.link_button(label.capitalize(), url)
            except Exception:
                st.markdown(f"[{label.capitalize()}]({url})")

st.divider()
st.write("Thanks for visiting! Follow along on social for more.")
