import sqlite3

conn = sqlite3.connect('complaints.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    location TEXT,
    category TEXT,
    incident_date TEXT,
    proof_filename TEXT,
    application_id TEXT,
    urgency TEXT,
    status TEXT
)
''')
conn.commit()
conn.close()

