from pathlib import Path
import json

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "site.json"
DEFAULT = {
    "name": "Passport Powell",
    "about": "Hi! I'm Passport Powell — sharing travel stories, tips, photos, and videos from my journeys around the world.",
    "social": {
        "facebook": "https://www.facebook.com/passportpowell",
        "instagram": "https://www.instagram.com/passportpowell/",
        "youtube": "https://www.youtube.com/@PassportPowell"
    },
    "youtube_videos": []
}

def load_config():
    try:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    # Ensure directory exists and write default if missing
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT, f, indent=2)
    except Exception:
        # If writing fails, still return DEFAULT
        return DEFAULT
    return DEFAULT

def save_config(cfg):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
