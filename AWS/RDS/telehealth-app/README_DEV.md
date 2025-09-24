# Telehealth App — Development README

Quick developer instructions for initializing the local database and running the app.

Prerequisites
- Python 3.11+ and a virtual environment (this repo uses `.venv` under the project folder).
- PostgreSQL accessible from the environment defined in the project's `.env` file.
- The project `requirements.txt` installed into the venv (e.g. `pip install -r requirements.txt`).

Environment
- Copy or edit `.env` in `AWS/RDS/telehealth-app` to set these variables (example names shown):

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=telehealth_db
DB_USER=telehealth_user
DB_PASSWORD=supersecret
FLASK_ENV=development
```

Initializing the database (dev)
1. Activate the virtualenv (if using the included `.venv`):

```bash
. .venv/bin/activate
```

2. Run the initializer to create tables, indexes, and sample data:

```bash
python init_database.py
```

- The script will create tables and add sample users/providers/patients. Look for `✅` messages in the output.

Sample credentials created by the initializer
- Admin: `admin@telehealth.com` / `AdminPass123!`
- Provider: `dr.smith@telehealth.com` / `DocPass123!`
- Patient 1: `patient1@telehealth.com` / `Patient123!`
- Patient 2: `patient2@telehealth.com` / `Patient123!`

Notes
- The initializer uses hashed passwords (bcrypt) and `ON CONFLICT` upserts so it is safe to run multiple times against the same DB.
- If you get foreign key errors, ensure the `users` inserts succeed (check the script output) — missing keys in the sample user dictionaries will raise exceptions and prevent `RETURNING user_id` from running.
- For development the app has demo fallbacks when `FLASK_ENV=development`; production usage requires real DB credentials and proper seeding.

Next steps
- Run the Flask app:

```bash
python app.py
```

- Run integration tests in `tests/test_api.py` to verify endpoints.

If you'd like, I can commit these changes to a branch and open a PR.