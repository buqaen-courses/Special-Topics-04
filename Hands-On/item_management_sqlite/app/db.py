import sqlite3
import os

DB_FILE = "items.db"


def get_connection():
    """Get a database connection with row factory for named column access."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row      # ← lets you write row["name"] instead of row[0]
    conn.execute("PRAGMA journal_mode=WAL")  # ← better concurrent performance
    return conn


def init_db():
    """Create the items table if it doesn't exist and seed with sample data."""
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
            # … 22 items total (same as the original seed)
        ]
        conn.executemany(
            "INSERT INTO items (name, price, is_offer, tax) VALUES (?, ?, ?, ?)",
            sample,
        )

    conn.commit()
    conn.close()


def dict_from_row(row):
    """Convert a sqlite3.Row to a plain dict."""
    if row is None:
        return None
    return dict(row)