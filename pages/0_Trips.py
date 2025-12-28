import streamlit as st
from pathlib import Path
from PIL import Image
import base64
import mimetypes

# Enable HEIC support BEFORE setting page config
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except Exception:
    pass  # HEIC support will be unavailable, but don't break the app

st.set_option("client.showErrorDetails", False)

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


def get_city_info(album_name: str) -> dict | None:
    """Extract city name and return fun facts."""
    city_facts = {
        "lima": {
            "name": "Lima",
            "country": "Peru",
            "tagline": "The City of Kings",
            "facts": [
                "Founded in 1535 by Spanish conquistador Francisco Pizarro",
                "Home to the largest fountain complex in the world (Parque de la Reserva)",
                "Lima's historic center is a UNESCO World Heritage Site",
                "Known as the gastronomic capital of South America"
            ]
        },
        "cusco": {
            "name": "Cusco",
            "country": "Peru",
            "tagline": "The Historic Capital of the Inca Empire",
            "facts": [
                "Once the capital of the Inca Empire, the largest empire in pre-Columbian America",
                "Sits at 11,152 feet (3,399m) above sea level",
                "The city's name means 'navel of the world' in Quechua",
                "Gateway to Machu Picchu, one of the New Seven Wonders of the World"
            ]
        },
        "chiang mai": {
            "name": "Chiang Mai",
            "country": "Thailand",
            "tagline": "The Rose of the North",
            "facts": [
                "Founded in 1296 as the capital of the Lanna Kingdom",
                "Home to over 300 Buddhist temples",
                "Famous for its annual Yi Peng Lantern Festival",
                "Digital nomad hub with a thriving expat community"
            ]
        },
        "hua hin": {
            "name": "Hua Hin",
            "country": "Thailand",
            "tagline": "Thailand's Original Beach Resort",
            "facts": [
                "Thailand's first beach resort, dating back to the 1920s",
                "Home to the royal summer palace, Klai Kangwon",
                "Famous for its night markets and fresh seafood",
                "One of the few places in Thailand where you can see wild elephants"
            ]
        },
        "bangkok": {
            "name": "Bangkok",
            "country": "Thailand",
            "tagline": "The City of Angels",
            "facts": [
                "Official name has 169 characters, the longest city name in the world",
                "Home to the Grand Palace and over 400 Buddhist temples",
                "Known as the 'Venice of the East' for its extensive canal network",
                "One of the world's top tourist destinations"
            ]
        },
        "phuket": {
            "name": "Phuket",
            "country": "Thailand",
            "tagline": "The Pearl of the Andaman",
            "facts": [
                "Thailand's largest island",
                "Famous for its stunning beaches and vibrant nightlife",
                "Home to the Big Buddha, a 45-meter tall marble statue",
                "Major center for diving and water sports"
            ]
        },
        "tokyo": {
            "name": "Tokyo",
            "country": "Japan",
            "tagline": "Where Tradition Meets Innovation",
            "facts": [
                "World's most populous metropolitan area with over 37 million people",
                "Home to the world's busiest train station (Shinjuku)",
                "Has more Michelin-starred restaurants than any other city",
                "Hosted the Summer Olympics in 1964 and 2021"
            ]
        },
        "paris": {
            "name": "Paris",
            "country": "France",
            "tagline": "The City of Light",
            "facts": [
                "Most visited city in the world",
                "The Eiffel Tower was originally intended to be temporary",
                "Home to the world's largest art museum, the Louvre",
                "Has over 400 parks and gardens"
            ]
        },
        "london": {
            "name": "London",
            "country": "United Kingdom",
            "tagline": "A City of Historic Grandeur",
            "facts": [
                "Founded by the Romans nearly 2,000 years ago",
                "The London Underground is the world's oldest underground railway",
                "Over 300 languages are spoken in the city",
                "Home to 4 UNESCO World Heritage Sites"
            ]
        },
        "new york": {
            "name": "New York City",
            "country": "USA",
            "tagline": "The City That Never Sleeps",
            "facts": [
                "Home to the Statue of Liberty, a gift from France in 1886",
                "Over 800 languages are spoken, making it the most linguistically diverse city",
                "Central Park is larger than the principality of Monaco",
                "The city has appeared in over 250 movies per year"
            ]
        }
    }
    
    album_lower = album_name.lower()
    for key, info in city_facts.items():
        if key in album_lower:
            return info
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
    
    # Track how many albums to display (load more incrementally)
    if "albums_to_show" not in st.session_state:
        st.session_state["albums_to_show"] = 6
    
    display_names = names[:st.session_state["albums_to_show"]]

    cols_per_row = 3
    for i in range(0, len(display_names), cols_per_row):
        row = st.columns(cols_per_row)
        for col, name in zip(row, display_names[i : i + cols_per_row]):
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
                        img = Image.open(cover)
                        st.image(img, use_container_width=True)
                    except Exception:
                        st.markdown("<div style='height:220px;background:#f5f5f5;border-radius:12px;display:flex;align-items:center;justify-content:center;color:#999;'>⚠️ Image unavailable</div>", unsafe_allow_html=True)
                st.markdown(f"**{name}**")
                if desc:
                    st.caption(desc.split("\n", 1)[0][:160])
                st.markdown(f"<div class='trip-meta'>{len(imgs)} photos</div>", unsafe_allow_html=True)
                if st.button("View album", key=f"spot-{name}"):
                    st.session_state["selected_album"] = name
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    
    # Show progress and load more button at the bottom
    if display_names:
        st.caption(f"Showing {len(display_names)} of {len(names)} albums")
    
    if len(names) > st.session_state["albums_to_show"]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📁 Load More Albums", use_container_width=True):
                st.session_state["albums_to_show"] += 6
                st.rerun()


def render_spotlight(albums):
    selected = st.session_state.get("selected_album")
    if not selected or selected not in albums:
        return
    st.subheader(f"📸 {selected}")
    data = albums[selected]
    files = data["images"]
    desc = data.get("description", "")
    
    # Show city information if available
    city_info = get_city_info(selected)
    if city_info:
        st.markdown(f"### 🌍 {city_info['name']}, {city_info['country']}")
        st.markdown(f"*{city_info['tagline']}*")
        
        with st.expander("✨ Fun Facts", expanded=True):
            for fact in city_info['facts']:
                st.markdown(f"• {fact}")
        st.markdown("")
    
    if desc:
        st.markdown(desc)
    
    if st.button("← Back to Albums", key="back-to-albums"):
        st.session_state.pop("selected_album", None)
        st.rerun()
    
    st.divider()

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
                img = Image.open(img_path)
                st.image(img, use_container_width=True)
            except Exception as e:
                rel_path = img_path.relative_to(IMAGES_ROOT) if img_path.is_relative_to(IMAGES_ROOT) else img_path
                st.error(f"⚠️ Could not load: {rel_path}")
                continue


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

    col1, col2 = st.columns([2, 1])
    with col1:
        page_size = st.slider("Photos per page", 12, 60, 24, step=6, key="all-pagesize")
    with col2:
        st.metric("Total photos", len(files))
    
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
                img = Image.open(img_path)
                st.image(img, use_container_width=True)
            except Exception as e:
                rel_path = img_path.relative_to(IMAGES_ROOT) if img_path.is_relative_to(IMAGES_ROOT) else img_path
                st.error(f"⚠️ Could not load: {rel_path}")
                continue


albums = collect_albums(IMAGES_ROOT)

if not albums:
    st.info("Add trip folders under assets/images (e.g., assets/images/Chiang Mai 2024/) with photos inside.")
else:
    tab_albums, tab_all = st.tabs(["Albums", "All Photos"])

    with tab_albums:
        # Show selected album at the top if one is selected
        if st.session_state.get("selected_album"):
            render_spotlight(albums)
        else:
            st.info("👇 Browse albums below and click 'View album' to see photos")
        
        st.divider()
        album_cards(albums)

    with tab_all:
        render_all_photos(albums)
