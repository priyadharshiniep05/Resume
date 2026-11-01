# Priyadharshini E P — Portfolio

A professional personal portfolio and resume website built with **Flask**, vanilla **HTML/CSS/JS**, and a strict monochrome editorial design.

## Quick Start

```bash
# 1. Create a virtual environment (first time only)
python3 -m venv .venv

# 2. Activate the virtual environment
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the development server
python3 app.py

# 5. Open in browser
open http://127.0.0.1:5000
```

The site will be live at **http://127.0.0.1:5000**.

## Project Structure

```
Resume/
├── app.py                  # Flask entry point — run with python3 app.py
├── requirements.txt        # Python dependencies
├── certificates.json       # Certificate metadata (images in static/certificates/)
├── contact_messages.db     # SQLite database for contact form submissions
├── static/
│   ├── css/style.css       # All styles (monochrome editorial theme)
│   ├── js/main.js          # Vanilla JS (scroll reveal, lightbox, parallax)
│   ├── images/             # Profile photo and assets
│   └── certificates/       # Certificate images
└── templates/
    ├── base.html            # Shared layout (nav, footer, meta)
    ├── index.html           # Single-page scroll-snap layout
    └── admin_messages.html  # Admin view for contact submissions
```

## Features

- **Single-page scroll-snap navigation** — all sections snap into full-viewport view
- **Scroll progress bar** and **active nav highlighting** via Intersection Observer
- **Contact form** with Flask backend and SQLite storage
- **Certificate gallery** with lightbox modal
- **Admin panel** at `/admin/messages` to view contact submissions
- **Fully responsive** — mobile-first with breakpoints at 768px and 1024px

## Adding Certificates

1. Place certificate images in `static/certificates/`
2. Edit `certificates.json` to register them:
   ```json
   [
     {"name": "Certificate Name", "path": "certificates/filename.jpg"}
   ]
   ```
3. Restart the server — they'll appear automatically in the Certificates section

## Tech Stack

| Layer    | Technology              |
|----------|------------------------|
| Backend  | Python 3, Flask        |
| Frontend | HTML5, CSS3, Vanilla JS|
| Database | SQLite                 |
| Fonts    | Playfair Display, Inter|
