import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List
from .models import NucleiFinding

# Store the database in the project root
DB_PATH = Path(__file__).resolve().parent.parent / "scans.db"

def init_db():
    """Initialize database tables if they do not exist."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Scans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                scan_date TEXT NOT NULL
            )
        """)
        # Findings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER,
                template_id TEXT,
                name TEXT,
                severity TEXT,
                matched_at TEXT,
                FOREIGN KEY (scan_id) REFERENCES scans(id)
            )
        """)
        conn.commit()

def save_scan(target: str, findings: List[NucleiFinding]):
    """Save a scan and its findings to the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Insert scan record
        scan_date = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO scans (target, scan_date) VALUES (?, ?)", 
            (target, scan_date)
        )
        scan_id = cursor.lastrowid
        
        # Insert finding records
        for f in findings:
            cursor.execute("""
                INSERT INTO findings (scan_id, template_id, name, severity, matched_at)
                VALUES (?, ?, ?, ?, ?)
            """, (scan_id, f.template_id, f.name, f.severity, f.matched_at))
            
        conn.commit()

def get_past_scans():
    """Retrieve a list of previous scans for history display."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, target, scan_date FROM scans ORDER BY id DESC")
        return cursor.fetchall()