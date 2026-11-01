"""
Priyadharshini E P — Portfolio Website
Flask application: serves pages, handles contact form, manages certificates.
"""

import os
import hmac
import json
import secrets
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, abort

# ---------------------------------------------------------------------------
# App Configuration
# ---------------------------------------------------------------------------
# Static files live in public/static so Vercel can serve them from its CDN.
# Locally, Flask serves the same folder at /static.
app = Flask(__name__, static_folder="public/static", static_url_path="/static")
# Secret key comes from the SECRET_KEY environment variable (set it on your host).
# Locally, a random key is generated each run if none is set.
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

# Password for /admin/messages, from the ADMIN_PASSWORD environment variable.
# If it is not set, the admin page is disabled (returns 404).
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "contact_messages.db")
CERT_DIR = os.path.join(BASE_DIR, "public", "static", "certificates")

# Contact form: set FORMSPREE_ID (e.g. "xabcdwxy") on your host to have messages
# emailed to you via Formspree. Without it, messages are saved to the local SQLite DB.
FORMSPREE_ID = os.environ.get("FORMSPREE_ID", "").strip()
FORM_ENDPOINT = f"https://formspree.io/f/{FORMSPREE_ID}" if FORMSPREE_ID else None
CERT_JSON = os.path.join(BASE_DIR, "certificates.json")

# ---------------------------------------------------------------------------
# Content Data — edit here to update the site
# ---------------------------------------------------------------------------

PROFILE = {
    "name": "Priyadharshini E P",
    "short_name": "Priyadharshini",
    "location": "Bengaluru, India",
    "email": "priyadharshiniep05@gmail.com",
    "phone": "7259905558",
    "linkedin": "https://www.linkedin.com/in/priyadharshiniep",
    "github": "https://github.com/priyadharshiniep05",
    "resume_pdf": "files/Priyadharshini_EP_Resume.pdf",
    "title": "Priyadharshini E P — Business & Data Analyst · Applied AI",
    "role": "Business & Data Analyst · Applied AI",
    "tagline": (
        "Final-year CSE student who turns real-world problems into clear requirements, "
        "data-driven insights and working AI products."
    ),
    "status": "Open to Business Analyst, Data Analyst and AI/ML roles",
    "summary": [
        "I'm a final-year Computer Science and Engineering student at K S Institute of Technology, Bengaluru, "
        "and I work where business problems meet data and technology. I like understanding what users and "
        "organisations actually need, turning that into clear requirements, and then using data to check "
        "whether the solution works.",
        "Because I also build, I can speak both languages. My drowsiness-detection research, WakeNet, was "
        "presented at ICRET 2026 and published in IJARBEST. I've designed and built products for fleet "
        "safety, logistics, flood alerts and healthcare, each starting from a real problem, the people it "
        "affects and the numbers that show impact.",
        "I'm looking for Business Analyst, Data Analyst or AI/ML roles where I can connect stakeholders, "
        "data and engineering, especially on problems with real social impact.",
    ],
    "languages": ["English", "Tamil", "Hindi", "Kannada"],
    "education": {
        "degree": "B.E. in Computer Science and Engineering",
        "institution": "K S Institute of Technology",
        "year": "2027",
        "location": "Bengaluru, India",
    },
}

STATS = [
    {"value": "97.2%", "label": "Drowsiness detection accuracy (WakeNet)"},
    {"value": "5", "label": "Products designed and built end to end"},
    {"value": "1", "label": "Published research paper"},
    {"value": "6", "label": "Hackathons, including one I organised"},
]

SKILLS = [
    {
        "category": "Business Analysis",
        "icon": "◇",
        "items": [
            "Requirements gathering", "BRDs", "User stories", "Process flows",
            "Agile / Scrum", "Jira", "Analytical thinking", "Decision making",
            "Leadership", "Negotiation",
        ],
    },
    {
        "category": "Data & BI",
        "icon": "▤",
        "items": [
            "Excel / Google Sheets", "SQL", "Power BI / Tableau", "Python",
            "Pandas", "NumPy", "Scikit-learn", "Chart.js",
        ],
    },
    {
        "category": "AI & Computer Vision",
        "icon": "◎",
        "items": [
            "PyTorch", "TensorFlow", "YOLOv8 / v11", "Vision Transformers",
            "OpenCV", "MediaPipe", "TensorRT", "Claude API",
        ],
    },
    {
        "category": "Development & Cloud",
        "icon": "⟨/⟩",
        "items": [
            "FastAPI", "Flask", "REST APIs", "WebSockets", "JavaScript",
            "React Native", "Flutter", "Java", "Git", "Docker", "AWS EC2",
            "Raspberry Pi",
        ],
    },
]

RESEARCH = {
    "title": "WakeNet: A Deep-Learning Model for Real-Time Drowsiness Detection",
    "venue": "International Journal of Advanced Research in Basic Engineering Sciences and Technology (IJARBEST)",
    "issue": "Vol. 12, Issue 9 · September 2026 · pp. 40–47",
    "conference": "Presented at the 17th International Conference on Recent Engineering and Technology (ICRET 2026)",
    "authors": "Dr. Sunita Chalageri, Priyadharshini E P, Namratha M H, Nishanth P, Nikhil Kumar P E",
    "url": "https://ijarbest.com/journal/V12i9",
    "abstract": (
        "Driver fatigue is a silent but deadly cause of road accidents. WakeNet combines YOLOv8's fast "
        "face-region detection with the global attention of Vision Transformers to catch subtle signs like "
        "micro-blinks and yawns. A CLAHE pre-processing step keeps it reliable at night, and a mobile app "
        "offers a personal mode for drivers and a fleet mode for managers."
    ),
    "metrics": [
        {"value": "97.2%", "label": "Accuracy, normal lighting"},
        {"value": "92.8%", "label": "Accuracy, low light"},
        {"value": "~30 ms", "label": "Average inference per frame"},
        {"value": "~33 FPS", "label": "Effective frame rate"},
    ],
    "datasets": "Evaluated on the UTA-RLDD and DDD benchmark datasets",
}

PROJECTS = [
    {
        "name": "NoNap",
        "problem": "Fatigue causes crashes that drivers often don't notice coming, and fleet operators have no live view of how alert their drivers are.",
        "year": "2026",
        "featured": True,
        "kicker": "Major project · Road safety · Fleet ops",
        "summary": (
            "A real-time driver drowsiness detection system that turns the WakeNet research into a working, "
            "in-car product with escalating alerts and a fleet dashboard."
        ),
        "highlights": [
            "Phase I: YOLOv8 + Vision Transformer pipeline with CLAHE low-light enhancement, served over FastAPI WebSockets to a React Native app with personal and fleet modes",
            "Phase II: Raspberry Pi camera in the car, FastAPI backend computing eye and mouth aspect ratios (EAR/MAR), and a Flutter iOS app with 3 alert levels that escalate to a fleet manager",
            "44-minute live hardware test: 10 ms median server inference per frame, 32.6 ms Pi round trip, 1.73 s median driver response time",
        ],
        "stack": ["Python", "YOLOv8", "ViT", "FastAPI", "WebSockets", "React Native", "Flutter", "Raspberry Pi"],
        "links": [
            {"label": "Phase II code", "url": "https://github.com/priyadharshiniep05/NoNap-Phase-2"},
            {"label": "Phase I code", "url": "https://github.com/priyadharshiniep05/NoNap"},
        ],
    },
    {
        "name": "Tracksy",
        "problem": "Shippers have to balance cost, speed and carbon across road, air, sea and rail, and a single disruption can delay every delivery after it.",
        "year": "2026",
        "kicker": "Logistics · AI",
        "summary": (
            "A full-stack logistics platform that plans shipments across road, air, sea and rail, "
            "predicts arrival times and reacts to disruptions."
        ),
        "highlights": [
            "Multimodal route optimiser with cost-versus-speed trade-offs and CO₂ estimates per route",
            "Self-learning ETA engine that improves from historical deliveries",
            "Live fleet map over SSE and WebSockets, plus portals for admins, suppliers, customers and drivers",
        ],
        "stack": ["FastAPI", "SQLAlchemy", "WebSockets", "SSE", "JavaScript", "Google Maps API"],
        "links": [{"label": "GitHub", "url": "https://github.com/priyadharshiniep05/Tracksy"}],
    },
    {
        "name": "AquaAlert",
        "problem": "Flood warnings often reach residents too late, especially people with weak or no internet connection.",
        "year": "2026",
        "kicker": "Disaster resilience · ML",
        "summary": (
            "A hyperlocal flood-prediction and community alert system for municipalities, "
            "emergency responders and residents."
        ),
        "highlights": [
            "Random Forest model turns live rainfall and river-level data into a flood-risk score",
            "SMS and push alerts through Twilio, so warnings reach people with poor connectivity",
            "Installable app that works offline, with live flood-zone maps and crowd-sourced flood reports",
        ],
        "stack": ["Python", "Flask", "Scikit-learn", "Twilio", "Leaflet.js", "Chart.js", "PWA"],
        "links": [{"label": "GitHub", "url": "https://github.com/priyadharshiniep05/AquaAlert"}],
    },
    {
        "name": "CareBridge",
        "problem": "Many people in India find it hard to judge how serious their symptoms are or where to go for care.",
        "year": "2026",
        "kicker": "Health-tech · LLMs",
        "summary": (
            "An AI healthcare web app that helps Indian users check symptoms, understand health risks "
            "and find their way through the healthcare system."
        ),
        "highlights": [
            "AI symptom triage and personalised recommendations powered by the Claude API",
            "Appointment booking, medication tracking and a nearby-facility finder",
            "Secure accounts with hashed passwords, installable on phones",
        ],
        "stack": ["Python", "Flask", "Claude API", "MySQL", "JavaScript", "PWA"],
        "links": [{"label": "GitHub", "url": "https://github.com/priyadharshiniep05/CareBridge"}],
    },
    {
        "name": "Yawns to YOLO",
        "problem": "Can a lightweight model detect driver fatigue reliably enough to be used in real vehicles?",
        "year": "2026",
        "kicker": "Research prototype",
        "summary": (
            "The first version of the drowsiness research: a Vision Transformer and YOLOv5 system that "
            "detects fatigue from yawns and eye closure. It led to WakeNet and NoNap."
        ),
        "highlights": [
            "Explored pairing a fast YOLO detector with a Vision Transformer classifier",
            "Laid the groundwork for the YOLOv8 + ViT architecture used in the published paper",
        ],
        "stack": ["Python", "YOLOv5", "Vision Transformer", "OpenCV"],
        "links": [{"label": "GitHub", "url": "https://github.com/priyadharshiniep05/Yawns-to-Yolo"}],
    },
]

ACHIEVEMENTS = [
    {
        "year": "2026",
        "type": "Publication",
        "title": "WakeNet published in IJARBEST",
        "detail": "Vol. 12, Issue 9 (September 2026). Co-authored with Dr. Sunita Chalageri and team.",
    },
    {
        "year": "2026",
        "type": "Conference",
        "title": "Presented at ICRET 2026",
        "detail": "17th International Conference on Recent Engineering and Technology.",
    },
    {
        "year": "",
        "type": "Leadership",
        "title": "Organiser, Sentinel Hack 6.0",
        "detail": "Helped organise and run the hackathon.",
    },
    {
        "year": "",
        "type": "Hackathons",
        "title": "Participant in 5 hackathons",
        "detail": "Hackzion v.2, Hackzion v.3, Axion, Nullpoint and Innovathon.",
    },
    {
        "year": "",
        "type": "Certification",
        "title": "NPTEL: The Joy of Computing using Python",
        "detail": "Elite + Silver Medal.",
    },
    {
        "year": "",
        "type": "Certification",
        "title": "NPTEL: Introduction to Machine Learning",
        "detail": "",
    },
]

COURSES = [
    "Java Database Connectivity (JDBC), Servlets and JSP: Infosys Springboard",
    "Introduction to PyTorch (Become a Deep Learning Engineer): Simplilearn",
    "Software Engineering and Agile Development: Infosys Springboard",
    "Unix/Linux OS Commands: Infosys Springboard",
    "Introduction to Computer Networking: Simplilearn",
    "Theory of Computation and Finite Automata: Infosys Springboard",
    "5-Day Industrial Training on Electric Vehicle Technology: Sri Manakula Vinayaka Engineering College",
]

# ---------------------------------------------------------------------------
# Database Helpers
# ---------------------------------------------------------------------------

def init_db():
    """Create the contact_messages table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def save_message(name, email, message):
    """Insert a contact form submission into the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO messages (name, email, message, created_at) VALUES (?, ?, ?, ?)",
        (name, email, message, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_messages():
    """Retrieve all contact form submissions."""
    if not os.path.exists(DB_PATH):
        return []
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM messages ORDER BY created_at DESC").fetchall()
    conn.close()
    return rows


# ---------------------------------------------------------------------------
# Certificate Scanner
# ---------------------------------------------------------------------------

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def scan_certificates():
    """
    Scan /static/certificates/ folder and merge with certificates.json.
    Returns a list of dicts: [{"name": "...", "file": "...", "path": "..."}]
    """
    certificates = []
    json_map = {}

    # Load optional JSON config
    if os.path.exists(CERT_JSON):
        try:
            with open(CERT_JSON, "r") as f:
                json_data = json.load(f)
                for entry in json_data:
                    json_map[entry.get("file", "")] = entry.get("name", "")
        except (json.JSONDecodeError, KeyError):
            pass

    # Scan the certificates directory
    if os.path.exists(CERT_DIR):
        # Files listed in certificates.json come first, in that order; others follow alphabetically.
        json_order = list(json_map.keys())
        files = sorted(
            os.listdir(CERT_DIR),
            key=lambda f: (json_order.index(f) if f in json_order else len(json_order), f),
        )
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                # Use JSON name if available, otherwise clean up filename
                name = json_map.get(filename, "")
                if not name:
                    name = os.path.splitext(filename)[0]
                    name = name.replace("-", " ").replace("_", " ").title()

                certificates.append({
                    "name": name,
                    "file": filename,
                    "path": f"certificates/{filename}",
                })

    # On hosts where the images aren't bundled with the app (e.g. Vercel's public/ CDN),
    # fall back to the list in certificates.json.
    if not certificates:
        for filename, name in json_map.items():
            certificates.append({"name": name, "file": filename, "path": f"certificates/{filename}"})

    return certificates


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Single-page portfolio containing all sections."""
    certs = scan_certificates()
    return render_template(
        "index.html",
        profile=PROFILE,
        stats=STATS,
        skills=SKILLS,
        research=RESEARCH,
        projects=PROJECTS,
        achievements=ACHIEVEMENTS,
        courses=COURSES,
        certificates=certs,
        form_endpoint=FORM_ENDPOINT,
    )


@app.route("/about")
def about():
    """Redirect to the About section on the single-page."""
    return redirect(url_for("index", _anchor="about"))


@app.route("/projects")
def projects():
    """Redirect to the Projects section on the single-page."""
    return redirect(url_for("index", _anchor="projects"))


@app.route("/certificates")
def certificates():
    """Redirect to the Certificates section on the single-page."""
    return redirect(url_for("index", _anchor="achievements"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Handle contact submissions and redirect to Contact section on index."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        # Basic validation
        if not name or not email or not message:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("index", _anchor="contact"))

        # Save to database
        try:
            save_message(name, email, message)
            flash("Thank you! Your message has been sent.", "success")
        except Exception as e:
            flash("Something went wrong. Please try again.", "error")
            print(f"DB Error: {e}")

        return redirect(url_for("index", _anchor="contact"))

    return redirect(url_for("index", _anchor="contact"))


def _admin_authorized():
    """Check HTTP Basic Auth credentials against ADMIN_USERNAME / ADMIN_PASSWORD."""
    auth = request.authorization
    if not auth or auth.password is None:
        return False
    user_ok = hmac.compare_digest(auth.username or "", ADMIN_USERNAME)
    pass_ok = hmac.compare_digest(auth.password, ADMIN_PASSWORD)
    return user_ok and pass_ok


@app.route("/admin/messages")
def admin_messages():
    """Password-protected admin view for contact form submissions."""
    if not ADMIN_PASSWORD:
        abort(404)
    if not _admin_authorized():
        return Response(
            "Login required.", 401,
            {"WWW-Authenticate": 'Basic realm="Admin"'},
        )
    messages = get_messages()
    return render_template("admin_messages.html", messages=messages, profile=PROFILE)


# ---------------------------------------------------------------------------
# Initialize & Run
# ---------------------------------------------------------------------------

# Create the local message table when running locally (skipped on read-only hosts).
try:
    init_db()
except sqlite3.OperationalError:
    pass

if __name__ == "__main__":
    app.run(debug=True, port=5000)
