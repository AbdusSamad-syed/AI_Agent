# tools.py
import os
import pandas as pd
from datetime import datetime, timedelta

DATA_DIR = "data"
PATIENTS_CSV = os.path.join(DATA_DIR, "patients.csv")
DOCTOR_XLSX = os.path.join(DATA_DIR, "doctor_schedule.xlsx")
APPOINTMENTS_XLSX = os.path.join(DATA_DIR, "appointments.xlsx")
INTAKE_PDF = os.path.join(DATA_DIR, "new_patient_intake_form.pdf")

def _parse_payload(payload: str):
    """Parse payload constructed by main.py."""
    parts = payload.split("||")
    keys = ["name","dob","doctor","location","patient_type","email","phone","carrier","member_id","group_id"]
    parts += [""] * (len(keys) - len(parts))
    return dict(zip(keys, parts[:len(keys)]))

# ---------- Tool functions ----------
def lookup_patient_tool(payload: str):
    p = _parse_payload(payload)
    df = pd.read_csv(PATIENTS_CSV)
    match = df[(df["Name"].str.lower() == p["name"].lower()) & (df["DOB"] == p["dob"])]
    if not match.empty:
        return f"RETURNING_PATIENT: Found record for {p['name']} (DOB {p['dob']})."
    else:
        return f"NEW_PATIENT: No record for {p['name']} with DOB {p['dob']}."

def schedule_appointment_tool(payload: str):
    p = _parse_payload(payload)
    sched = pd.read_excel(DOCTOR_XLSX)
    row = sched[sched["Doctor"].str.lower() == p["doctor"].lower()]
    if row.empty:
        return f"ERROR: Doctor '{p['doctor']}' not found."
    available = row.iloc[0]["Available_Slots"]
    appt_dt = pd.to_datetime(available)
    duration = 60 if p["patient_type"].lower() == "new" else 30
    appt_entry = {
        "Name": p["name"],
        "Doctor": row.iloc[0]["Doctor"],
        "Slot": appt_dt.strftime("%Y-%m-%d %H:%M"),
        "Duration_min": duration,
        "Location": p["location"],
        "BookedAt": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    try:
        old = pd.read_excel(APPOINTMENTS_XLSX)
        new = pd.concat([old, pd.DataFrame([appt_entry])], ignore_index=True)
    except Exception:
        new = pd.DataFrame([appt_entry])
    new.to_excel(APPOINTMENTS_XLSX, index=False)
    # update slot
    new_slot = (appt_dt + timedelta(minutes=duration)).strftime("%Y-%m-%d %H:%M")
    sched.loc[sched["Doctor"].str.lower() == p["doctor"].lower(), "Available_Slots"] = new_slot
    sched.to_excel(DOCTOR_XLSX, index=False)
    return f"SCHEDULED: {p['name']} with {p['doctor']} at {appt_entry['Slot']} ({duration}min)."

def collect_insurance_tool(payload: str):
    p = _parse_payload(payload)
    if not p["carrier"] or not p["member_id"]:
        return "INSURANCE_INCOMPLETE: Carrier or Member ID missing."
    return f"INSURANCE_SAVED: carrier={p['carrier']}, member_id={p['member_id']}, group_id={p['group_id']}"

def confirm_appointment_tool(payload: str):
    p = _parse_payload(payload)
    try:
        appts = pd.read_excel(APPOINTMENTS_XLSX)
        last = appts[appts["Name"].str.lower() == p["name"].lower()].iloc[-1]
    except Exception:
        return "ERROR: No appointment found to confirm."
    return f"CONFIRMED: {p['name']} with {last['Doctor']} at {last['Slot']}. Email sent to {p['email']}."

def send_intake_form_tool(payload: str):
    p = _parse_payload(payload)
    if not p["email"]:
        return "INTAKE_FORM_NOT_SENT: No email."
    return f"INTAKE_FORM_SENT: Sent to {p['email']} (file: {os.path.basename(INTAKE_PDF)})."

def send_reminders_tool(payload: str):
    p = _parse_payload(payload)
    return "\n".join([
        f"Reminder1 to {p['email'] or p['phone']}: Appointment scheduled.",
        "Reminder2: Have you filled forms? Confirm visit.",
        "Reminder3: Final reminder. Confirm or cancel (state reason)."
    ])
