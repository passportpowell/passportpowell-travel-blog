import streamlit as st
from pathlib import Path
from PIL import Image
import mimetypes
import base64

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except Exception:
    pass

st.set_page_config(page_title="Album — Passport Powell", page_icon="📸", layout="wide")

SUPPORTED = {".jpg", ".jpeg", ".png", ".gif", ".heic"}
IMAGES_ROOT = Path("assets/images")


def pretty_name(rel_path: Path) -> str:
    parts = []
    for part in rel_path.parts:
        cleaned = part.replace("-", " ").replace("_", " ")
        cleaned = " ".join(word.capitalize() for word in cleaned.split())
        parts.append(cleaned)
    return " / ".join(parts)


def load_album_description(album_dir: Path) -> str:
    for fname in ("description.txt", "description.md"):
        fpath = album_dir / fname
        if fpath.exists():
            try:
                return fpath.read_text(encoding="utf-8").strip()
            except Exception:
                continue
    return ""


@st.cache_data(show_spinner=False)
def collect_albums(root: Path):
    albums = {}
    if not root.exists():
        return albums
    loose = [p for p in sorted(root.iterdir()) if p.is_file() and p.suffix.lower() in SUPPORTED]
    if loose:
        albums["Unsorted"] = {"images": loose, "description": load_album_description(root)}
    for album_dir in sorted(p for p in root.rglob("*") if p.is_dir()):
        images = [img for img in sorted(album_dir.iterdir()) if img.is_file() and img.suffix.lower() in SUPPORTED]
        if images:
            rel = album_dir.relative_to(root)
            name = pretty_name(rel)
            albums[name] = {"images": images, "description": load_album_description(album_dir)}
    return albums


@st.cache_data(show_spinner=False)
def to_data_uri(img_path: Path) -> str | None:
    try:
        mime, _ = mimetypes.guess_type(img_path.name)
        mime = mime or "image/jpeg"
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64,{b64}"
    except Exception:
        return None


albums = collect_albums(IMAGES_ROOT)
album_param = st.query_params.get("album")

if not album_param:
    album_param = st.session_state.get("selected_album")

if not albums:
    st.info("Add trip folders under assets/images (e.g., assets/images/Chiang Mai 2024/) with photos inside.")
    st.stop()

if not album_param or album_param not in albums:
    st.warning("Select an album from Trips. Redirecting...")
    st.switch_page("pages/0_Trips.py")

data = albums.get(album_param)
files = data["images"]
desc = data.get("description", "")

st.title(album_param)
if desc:
    st.markdown(desc)

# Hero cover
cover = files[0]
data_uri = to_data_uri(cover)
if data_uri:
    st.markdown(f"<img style='width:100%; max-height:420px; object-fit:cover; border-radius:14px;' src='{data_uri}' />", unsafe_allow_html=True)
else:
    st.image(str(cover), use_container_width=True)

st.divider()

page_size = st.slider("Photos per page", 12, 60, 36, step=6, key="album-pagesize")
total = len(files)
pages = (total + page_size - 1) // page_size or 1
page = st.number_input("Page", 1, pages, 1, key="album-page")
start = (int(page) - 1) * page_size
end = min(start + page_size, total)
view = files[start:end]
st.write(f"Showing {start+1}–{end} of {total}")

cols = st.columns(3)
for i, img_path in enumerate(view):
    with cols[i % 3]:
        try:
            st.image(Image.open(img_path), use_container_width=True)
        except Exception:
            st.image(str(img_path))

st.divider()
st.page_link("pages/0_Trips.py", label="← Back to Trips")
