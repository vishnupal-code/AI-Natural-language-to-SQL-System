# using faker library to generate random data for patients
# Sqlite3 to create database and tables, and insert data into them
# random library to generate random data for doctors, appointments, treatments, and invoices

import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta


fake = Faker()
import os
DB_NAME = os.path.join(os.path.dirname(__file__), "clinic.db")


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        date_of_birth DATE,
        gender TEXT,
        city TEXT,
        registered_date DATE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        department TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        appointment_date DATETIME,
        status TEXT,
        notes TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treatments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        treatment_name TEXT,
        cost REAL,
        duration_minutes INTEGER,
        FOREIGN KEY(appointment_id) REFERENCES appointments(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        invoice_date DATE,
        total_amount REAL,
        paid_amount REAL,
        status TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
    """)

    conn.commit()


# Insert Doctors
def insert_doctors(conn):
    cursor = conn.cursor()

    specializations = [
        "Dermatology", "Cardiology", "Orthopedics",
        "General", "Pediatrics"
    ]

    doctors = []
    for _ in range(15):
        spec = random.choice(specializations)
        doctors.append((
            fake.name(),
            spec,
            spec + " Department",
            fake.phone_number()
        ))

    cursor.executemany("""
    INSERT INTO doctors (name, specialization, department, phone)
    VALUES (?, ?, ?, ?)
    """, doctors)

    conn.commit()
    return len(doctors)


# Insert Patients
def insert_patients(conn):
    cursor = conn.cursor()

    cities = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Pune", "Jaipur", "Lucknow"]

    patients = []
    for _ in range(200):
        patients.append((
            fake.first_name(),
            fake.last_name(),
            fake.email() if random.random() > 0.2 else None,
            fake.phone_number() if random.random() > 0.1 else None,
            fake.date_of_birth(minimum_age=1, maximum_age=90),
            random.choice(["M", "F"]),
            random.choice(cities),
            fake.date_between(start_date='-1y', end_date='today')
        ))

    cursor.executemany("""
    INSERT INTO patients (first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, patients)

    conn.commit()
    return len(patients)



# Insert Appointments
def insert_appointments(conn):
    cursor = conn.cursor()

    statuses = ["Scheduled", "Completed", "Cancelled", "No-Show"]

    appointments = []
    for _ in range(500):
        appointments.append((
            random.randint(1, 200),
            random.randint(1, 15),
            fake.date_time_between(start_date='-1y', end_date='now'),
            random.choices(statuses, weights=[2, 5, 2, 1])[0],
            fake.text(max_nb_chars=50) if random.random() > 0.3 else None
        ))

    cursor.executemany("""
    INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, notes)
    VALUES (?, ?, ?, ?, ?)
    """, appointments)

    conn.commit()
    return len(appointments)


# Insert Treatments
def insert_treatments(conn):
    cursor = conn.cursor()

    treatments = []
    for _ in range(350):
        treatments.append((
            random.randint(1, 500),
            random.choice(["Consultation", "Surgery", "Therapy", "Checkup"]),
            round(random.uniform(50, 5000), 2),
            random.randint(10, 180)
        ))

    cursor.executemany("""
    INSERT INTO treatments (appointment_id, treatment_name, cost, duration_minutes)
    VALUES (?, ?, ?, ?)
    """, treatments)

    conn.commit()
    return len(treatments)



def insert_invoices(conn):
    cursor = conn.cursor()

    statuses = ["Paid", "Pending", "Overdue"]

    invoices = []
    for _ in range(300):
        total = round(random.uniform(100, 5000), 2)
        paid = total if random.random() > 0.3 else round(random.uniform(0, total), 2)

        status = "Paid" if paid == total else random.choice(["Pending", "Overdue"])

        invoices.append((
            random.randint(1, 200),
            fake.date_between(start_date='-1y', end_date='today'),
            total,
            paid,
            status
        ))

    cursor.executemany("""
    INSERT INTO invoices (patient_id, invoice_date, total_amount, paid_amount, status)
    VALUES (?, ?, ?, ?, ?)
    """, invoices)

    conn.commit()
    return len(invoices)



# MAIN FUNCTION
def main():
    conn = sqlite3.connect(DB_NAME)

    create_tables(conn)

    d = insert_doctors(conn)
    p = insert_patients(conn)
    a = insert_appointments(conn)
    t = insert_treatments(conn)
    i = insert_invoices(conn)

    print(f"Created {p} patients, {d} doctors, {a} appointments, {t} treatments, {i} invoices")

    conn.close()


if __name__ == "__main__":
    main()