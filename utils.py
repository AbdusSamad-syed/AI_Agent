# utils.py
import os
import pandas as pd
from datetime import datetime, timedelta

DATA_DIR = "data"
PATIENTS_CSV = os.path.join(DATA_DIR, "patients.csv")
DOCTOR_XLSX = os.path.join(DATA_DIR, "doctor_schedule.xlsx")
INTAKE_PDF = os.path.join(DATA_DIR, "new_patient_intake_form.pdf")

def ensure_sample_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(PATIENTS_CSV):
        names = [f"Patient_{i}" for i in range(1, 51)]
        dobs = pd.date_range("1970-01-01", periods=50).strftime("%Y-%m-%d").tolist()
        df = pd.DataFrame({"Name": names, "DOB": dobs})
        df.to_csv(PATIENTS_CSV, index=False)
    if not os.path.exists(DOCTOR_XLSX):
        docs = ["Dr. Smith","Dr. Kapoor","Dr. Rao"]
        start = datetime.now() + timedelta(days=1)
        slots = [(start + timedelta(hours=i)).strftime("%Y-%m-%d %H:%M") for i in range(len(docs))]
        df = pd.DataFrame({"Doctor": docs, "Available_Slots": slots})
        df.to_excel(DOCTOR_XLSX, index=False)
    if not os.path.exists(INTAKE_PDF):
        with open(INTAKE_PDF, "w") as f:
            f.write("Sample Intake Form")
