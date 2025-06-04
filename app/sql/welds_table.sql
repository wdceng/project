CREATE TABLE welds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drawing_no TEXT NOT NULL,
    revision TEXT,
    spool_no TEXT,
    weld_no TEXT NOT NULL,
    location TEXT,
    weld_type TEXT,
    size REAL,               -- Now numeric (decimal-friendly)
    schedule TEXT,
    fabrication_no TEXT,
    root_welders TEXT,
    root_process TEXT,
    balance_welders TEXT,
    fabrication_date DATE,
    vt TEXT,
    pt TEXT,
    mt TEXT,
    rt TEXT,
    ut TEXT
);