# Priyadharshini E P — Portfolio

Personal portfolio site: business & data analyst with applied-AI research.
Built with **Flask**, vanilla **HTML/CSS/JS**, a monochrome editorial design and an iOS-style glass UI.

## Run it locally

```bash
python3 -m venv .venv          # first time only
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Open http://127.0.0.1:5000

## Update the content

Almost everything lives in plain lists near the top of `app.py`:

| To change… | Edit |
|---|---|
| Name, title, summary, contact details | `PROFILE` |
| Numbers under the hero | `STATS` |
| Skills | `SKILLS` |
| Research paper | `RESEARCH` |
| Projects | `PROJECTS` (copy a block to add one) |
| Hackathons, awards, publications | `ACHIEVEMENTS` |
| Courses | `COURSES` |
| Certificates | add the image to `public/static/certificates/`, then its name to `certificates.json` |
| Résumé PDF | replace `public/static/files/Priyadharshini_EP_Resume.pdf` |

Then publish:

```bash
git add -A
git commit -m "Describe what you changed"
git push
```

Vercel redeploys automatically after every push.

## Deploy on Vercel

1. Sign in at https://vercel.com with GitHub and **Add New → Project → Import** this repo.
2. Leave the defaults (Vercel detects Flask from `app.py`) and add these **Environment Variables**:

   | Name | Value |
   |---|---|
   | `SECRET_KEY` | a long random string: `python3 -c "import secrets; print(secrets.token_hex(32))"` |
   | `FORMSPREE_ID` | the ID from your Formspree form URL, e.g. `xabcdwxy` from `https://formspree.io/f/xabcdwxy` |

3. Click **Deploy**.

### Contact form

Vercel can't store files, so on the live site messages are emailed to you through
[Formspree](https://formspree.io) (free tier). Create a form there with your email,
copy its ID into `FORMSPREE_ID`, and redeploy.

When you run the site locally without `FORMSPREE_ID`, messages are saved to
`contact_messages.db` instead. You can read them at `/admin/messages` if you start the app with
`ADMIN_PASSWORD=yourpassword python3 app.py`.

## Project structure

```
Resume/
├── app.py                 # Flask app + all site content
├── certificates.json      # certificate display names and order
├── requirements.txt
├── public/static/         # served by Vercel's CDN (and by Flask locally)
│   ├── css/style.css
│   ├── js/main.js
│   ├── images/profile.jpg
│   ├── certificates/
│   └── files/Priyadharshini_EP_Resume.pdf
└── templates/
    ├── base.html
    ├── index.html
    └── admin_messages.html
```
