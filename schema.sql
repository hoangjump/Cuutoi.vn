CREATE TABLE IF NOT EXISTS points (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lat REAL NOT NULL,
  lon REAL NOT NULL,
  note TEXT,
  phone TEXT,
  name TEXT,
  address TEXT,
  type TEXT DEFAULT 'help',          -- help | donor | donor_inactive
  last_update DATETIME DEFAULT CURRENT_TIMESTAMP,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
