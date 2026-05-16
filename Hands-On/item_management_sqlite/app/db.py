import sqlite3
import os

DB_FILE = "items.db"


def get_connection():
    """Get a database connection with row factory for named column access."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Create the items table if it doesn't exist and seed with sample data if empty."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            is_offer INTEGER DEFAULT 0,
            tax REAL DEFAULT 0.0
        )
    """)

    # Seed data if table is empty
    count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    if count == 0:
        sample = [
            ("Laptop", 999.99, 1, 99.99),
            ("Mouse", 25.50, 0, 2.55),
            ("Keyboard", 75.00, 1, 7.50),
            ("Monitor", 299.99, 0, 29.99),
            ("Webcam", 89.99, 1, 8.99),
            ("Headphones", 150.00, 0, 15.00),
            ("USB Cable", 12.99, 0, 1.29),
            ("Desk Lamp", 45.00, 1, 4.50),
            ("Chair", 199.99, 0, 19.99),
            ("Desk", 350.00, 1, 35.00),
            ("Printer", 180.00, 0, 18.00),
            ("Speaker", 120.00, 1, 12.00),
            ("Tablet", 450.00, 0, 45.00),
            ("Smartwatch", 250.00, 1, 25.00),
            ("Router", 85.00, 0, 8.50),
            ("External Drive", 110.00, 1, 11.00),
            ("Phone Case", 19.99, 0, 1.99),
            ("Charger", 29.99, 1, 2.99),
            ("Backpack", 65.00, 0, 6.50),
            ("Mouse Pad", 14.99, 1, 1.49),
            ("Webcam Stand", 39.99, 0, 3.99),
            ("Cable Organizer", 9.99, 1, 0.99),
        ]
        conn.executemany(
            "INSERT INTO items (name, price, is_offer, tax) VALUES (?, ?, ?, ?)",
            sample,
        )

    conn.commit()
    conn.close()


def dict_from_row(row):
    """Convert a sqlite3.Row to a plain dict (handles NULL → None)."""
    if row is None:
        return None
    return dict(row)
