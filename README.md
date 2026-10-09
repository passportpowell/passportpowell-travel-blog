#  Passport Powell  Travel Blog

> A beautiful Streamlit-powered travel blog to share your adventures, photos, and videos from around the world.

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org)

##  Features

-  **Photo Albums**  Organize travel photos by location with automatic album discovery
-  **Video Gallery**  Embed YouTube videos directly in your blog
-  **City Information**  Automatic city facts and descriptions for major destinations
-  **Responsive Design**  Beautiful cards with hover effects and mobile-friendly layout
-  **HEIC Support**  Display iPhone HEIC photos natively
-  **Performance Optimized**  Lazy loading and caching for fast page loads

No license file is included in this repository.

##  Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation

**Windows:**
```powershell
# Clone the repository
git clone https://github.com/passportpowell/passportpowell-travel-blog.git
cd passportpowell-travel-blog

# Create and activate virtual environment (recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

**macOS/Linux:**
```bash
# Clone the repository
git clone https://github.com/passportpowell/passportpowell-travel-blog.git
cd passportpowell-travel-blog

# Create and activate virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Then open **http://localhost:8501** in your browser! 

##  Project Structure

```
passportpowell-travel-blog/
 app.py                      # Home page
 pages/
    0_Trips.py             # Photo albums with city info
    2_Videos.py            # YouTube video gallery
    3_Links.py             # Social media links
 lib/
    config.py              # Configuration management
 config/
    site.json              # Site settings (name, about, social links)
 assets/
    images/                # Your travel photos
        2025-11/
           Lima Peru 01/
           Cusco Peru 02/
        2024-09/
            Chiang Mai Thailand/
 requirements.txt           # Python dependencies
```

##  Adding Content

### Photos
1. Create a folder for your trip under `assets/images/`
   - Example: `assets/images/2025-11/Lima Peru 01/`
2. Add your photos (supports `.jpg`, `.jpeg`, `.png`, `.gif`, `.heic`)
3. *Optional:* Add `description.txt` or `description.md` for album context

### City Information
The app automatically detects city names in album folders and displays:
- City name and country
- Tagline
- Fun facts

Currently supported cities: Lima, Cusco, Chiang Mai, Hua Hin, Bangkok, Phuket, Tokyo, Paris, London, New York

### Videos
1. Navigate to the **Videos** page
2. Paste full YouTube video URLs
3. Videos are automatically embedded and saved

### Site Settings
Edit `config/site.json`:
```json
{
  "name": "Passport Powell",
  "about": "Hi! I'm Passport Powell  sharing travel stories...",
  "social": {
    "facebook": "https://www.facebook.com/passportpowell",
    "instagram": "https://www.instagram.com/passportpowell/",
    "youtube": "https://www.youtube.com/@PassportPowell"
  },
  "youtube_videos": []
}
```

##  Pages Overview

| Page | Description |
|------|-------------|
|  **Home** | About section with featured photo and social links |
|  **Trips** | Album grid with city information, 6 albums per load |
|  **Videos** | YouTube video embeds with add/manage functionality |
|  **Links** | Social media link buttons |

##  Technologies Used

- **[Streamlit](https://streamlit.io)**  Web framework for Python
- **[Pillow](https://python-pillow.org/)**  Image processing
- **[pillow-heif](https://github.com/bigcat88/pillow_heif)**  HEIC image support

##  License

This project is open source and available under the [MIT License](LICENSE).

##  Contributing

Contributions, issues, and feature requests are welcome!

##  Contact

**Passport Powell**
- Instagram: [@passportpowell](https://www.instagram.com/passportpowell/)
- YouTube: [@PassportPowell](https://www.youtube.com/@PassportPowell)
- Facebook: [passportpowell](https://www.facebook.com/passportpowell)

---

Made with  and 
