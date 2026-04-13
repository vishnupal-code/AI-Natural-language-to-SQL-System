import sqlite3

conn = sqlite3.connect("clinic.db")
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables:", tables)

# Check patients count
cursor.execute("SELECT COUNT(*) FROM patients")
print("Patients:", cursor.fetchone())

# Check doctors count
cursor.execute("SELECT COUNT(*) FROM doctors")
print("Doctors:", cursor.fetchone())

# Check appointments count
cursor.execute("SELECT COUNT(*) FROM appointments")
print("Appointments:", cursor.fetchone())

conn.close()