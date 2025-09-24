Simple Appointment Booking (beginner-friendly)

Files
- `app.py` — tiny Flask app that keeps data in memory (no database).
- `templates/` — minimal HTML pages for listing providers and booking an appointment.

Run
1. Create a virtualenv and install requirements:

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

2. Run the app:

```bash
python app.py
```

3. Open `http://127.0.0.1:5000` in your browser and book appointments.

Notes for students
- This shows how to build simple CRUD interactions with Flask.
- Data is stored in `APPOINTMENTS` list only while the server runs; add persistence later with SQLite or PostgreSQL.
- You can extend by adding validation, authentication, or a calendar view.
