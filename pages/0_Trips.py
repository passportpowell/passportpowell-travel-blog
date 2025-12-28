import streamlit as st
from pathlib import Path
from PIL import Image
import base64
import mimetypes

st.set_option("client.showErrorDetails", False)

# Try to enable HEIC support
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except Exception:
    pass

st.set_page_config(page_title="Trips — Passport Powell", page_icon="🧭", layout="wide")
st.title("Trips")
st.caption("Browse albums or jump into all photos in one view.")

st.markdown(
    """
    <style>
    .trip-card {
        border: 1px solid #e8e8e8;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
        padding: 12px;
        background: #ffffff;
        transition: transform 0.12s ease, box-shadow 0.12s ease;
        display: flex;
        flex-direction: column;
        gap: 8px;
        height: 100%;
    }
    .trip-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 36px rgba(0,0,0,0.10);
    }
    .trip-card img {
        border-radius: 10px;
    }
    .cover-img {
        width: 100%;
        height: 220px;
        object-fit: cover;
        border-radius: 12px;
        display: block;
        background: #f5f5f5;
    }
    .trip-meta {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 6px;
    }
    .pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        background: #f3f4f6;
        color: #444;
        font-size: 0.9rem;
        margin-bottom: 6px;
    }
    .card-footer {
        margin-top: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
    for fname in ("description.txt", "description.md"):  # simple per-album note
        fpath = album_dir / fname
        if fpath.exists():
            try:
                return fpath.read_text(encoding="utf-8").strip()
            except Exception:
                continue
    return ""


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


@st.cache_data(show_spinner=False)
def collect_albums(root: Path):
    """Collect any folder (at any depth) under root that contains supported images."""
    albums = {}
    if not root.exists():
        return albums

    # Include root-level loose images as "Unsorted"
    root_imgs = [p for p in sorted(root.iterdir()) if p.is_file() and p.suffix.lower() in SUPPORTED]
    if root_imgs:
        albums["Unsorted"] = {"images": root_imgs, "description": load_album_description(root)}

    for album_dir in sorted(p for p in root.rglob("*") if p.is_dir()):
        imgs = [img for img in sorted(album_dir.iterdir()) if img.is_file() and img.suffix.lower() in SUPPORTED]
        if imgs:
            rel = album_dir.relative_to(root)
            album_name = pretty_name(rel)
            albums[album_name] = {
                "images": imgs,
                "description": load_album_description(album_dir),
                "sort_key": rel.as_posix().lower(),
            }
    return albums


def album_cards(albums):
    names = [name for name, _ in sorted(albums.items(), key=lambda item: item[1].get("sort_key", item[0]), reverse=True)]
    # Limit initial render for speed; allow user to expand
    show_all = st.checkbox("Show all albums", value=st.session_state.get("show_all_albums", False))
    st.session_state["show_all_albums"] = show_all
    if not show_all:
        names = names[:12]

    cols_per_row = 3
    for i in range(0, len(names), cols_per_row):
        row = st.columns(cols_per_row)
        for col, name in zip(row, names[i : i + cols_per_row]):
            data = albums[name]
            imgs = data["images"]
            cover = imgs[0]
            desc = data.get("description", "")
            with col:
                st.markdown("<div class='trip-card'>", unsafe_allow_html=True)
                data_uri = to_data_uri(cover)
                if data_uri:
                    st.markdown(f"<img class='cover-img' src='{data_uri}' />", unsafe_allow_html=True)
                else:
                    try:
                        st.image(Image.open(cover), use_container_width=True)
                    except Exception:
                        st.image(str(cover))
                st.markdown(f"**{name}**")
                if desc:
                    st.caption(desc.split("\n", 1)[0][:160])
                st.markdown(f"<div class='trip-meta'>{len(imgs)} photos</div>", unsafe_allow_html=True)
                if st.button("View album", key=f"spot-{name}"):
                    st.session_state["selected_album"] = name
                    st.switch_page("Album")
                st.markdown("</div>", unsafe_allow_html=True)


def render_spotlight(albums):
    selected = st.session_state.get("selected_album")
    if not selected or selected not in albums:
        st.info("Select an album card above to view it here.")
        return
    st.divider()
    st.subheader(f"Album: {selected}")
    data = albums[selected]
    files = data["images"]
    desc = data.get("description", "")
    if desc:
        st.markdown(desc)

    page_size = st.slider("Photos per page", 9, 48, 18, step=3, key="spot-pagesize")
    total = len(files)
    pages = (total + page_size - 1) // page_size or 1
    page = st.number_input("Page", 1, pages, 1, key="spot-page")
    start = (int(page) - 1) * page_size
    end = min(start + page_size, total)
    view = files[start:end]
    st.write(f"Showing {start+1}–{end} of {total}")

    cols = st.columns(3)
    seen = set()
    for i, img_path in enumerate(view):
        if img_path in seen:
            continue
        seen.add(img_path)
        with cols[i % 3]:
            try:
                st.image(Image.open(img_path), use_container_width=True)
            except Exception:
                st.image(str(img_path))


def render_all_photos(albums):
    # Deduplicate across all albums
    files = []
    seen = set()
    for data in albums.values():
        for img in data["images"]:
            if img in seen:
                continue
            seen.add(img)
            files.append(img)

    if not files:
        st.info("No photos found in assets/images.")
        return

    page_size = st.slider("Photos per page", 12, 60, 36, step=6, key="all-pagesize")
    total = len(files)
    pages = (total + page_size - 1) // page_size or 1
    page = st.number_input("Page", 1, pages, 1, key="all-page")
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


albums = collect_albums(IMAGES_ROOT)

if not albums:
    st.info("Add trip folders under assets/images (e.g., assets/images/Chiang Mai 2024/) with photos inside.")
else:
    ordered_names = [name for name, _ in sorted(albums.items(), key=lambda item: item[1].get("sort_key", item[0]), reverse=True)]
    if "selected_album" not in st.session_state and ordered_names:
        st.session_state["selected_album"] = ordered_names[0]

    tab_albums, tab_all = st.tabs(["Albums", "All Photos"])

    with tab_albums:
        album_cards(albums)
        render_spotlight(albums)

    with tab_all:
        render_all_photos(albums)
