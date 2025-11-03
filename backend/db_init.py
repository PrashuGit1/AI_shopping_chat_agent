import sqlite3

conn = sqlite3.connect("phones.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE phones (
  id INTEGER PRIMARY KEY,
  model TEXT NOT NULL,
  brand TEXT NOT NULL,
  price INTEGER NOT NULL, -- in INR
  camera_mp REAL, -- main camera megapixels
  battery_mah INTEGER,
  display_inch REAL,
  ram_gb INTEGER,
  storage_gb INTEGER,
  soc TEXT,
  notes TEXT -- freeform (use cautiously)
)

""")
