from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = "dev-secret-key"

# In-memory demo data
PROVIDERS = [
    {"id": "p1", "name": "Dr. Alice", "specialty": "Pediatrician"},
    {"id": "p2", "name": "Dr. Bob", "specialty": "Dentist"},
    {"id": "p3", "name": "Dr. Carol", "specialty": "Family Medicine"},
]

# appointments: list of dicts {id, provider_id, patient_name, datetime, notes}
APPOINTMENTS = []

@app.route("/")
def index():
    # show providers and upcoming appointments
    # allow filtering by specialty via ?specialty=...
    specialty = request.args.get('specialty', '')

    # compute unique specialties for the dropdown
    specialties = sorted({p.get('specialty', '') for p in PROVIDERS if p.get('specialty')})

    if specialty:
        providers = [p for p in PROVIDERS if p.get('specialty') == specialty]
    else:
        providers = PROVIDERS

    upcoming = sorted(APPOINTMENTS, key=lambda a: a['datetime'])
    return render_template("index.html", providers=providers, appointments=upcoming, specialties=specialties, selected_specialty=specialty)

@app.route("/book/<provider_id>", methods=["GET", "POST"])
def book(provider_id):
    provider = next((p for p in PROVIDERS if p['id'] == provider_id), None)
    if not provider:
        flash("Provider not found.")
        return redirect(url_for('index'))

    if request.method == 'POST':
        patient_name = request.form.get('name', '').strip()
        date_str = request.form.get('date', '').strip()
        time_str = request.form.get('time', '').strip()
        notes = request.form.get('notes', '').strip()

        if not patient_name or not date_str or not time_str:
            flash('Please provide your name, date and time for the appointment.')
            return redirect(url_for('book', provider_id=provider_id))

        try:
            dt = datetime.fromisoformat(f"{date_str}T{time_str}")
        except ValueError:
            flash('Invalid date/time format. Use YYYY-MM-DD and HH:MM.')
            return redirect(url_for('book', provider_id=provider_id))

        # create appointment
        appt = {
            'id': str(uuid.uuid4()),
            'provider_id': provider_id,
            'provider_name': provider['name'],
            'patient_name': patient_name,
            'datetime': dt,
            'notes': notes,
        }
        APPOINTMENTS.append(appt)
        flash('Appointment booked!')
        return redirect(url_for('index'))

    return render_template('book.html', provider=provider)

if __name__ == '__main__':
    app.run(debug=True)
