import os
import sqlite3

DATABASE_NAME = "transactions.db"
BASE_DIR = os.path.dirname(__file__)
DATABASE_NAME = os.path.join(BASE_DIR, "transactions.db")

def create_database():
    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            date TEXT,
            description TEXT,
            debit REAL,
            credit REAL,
            balance REAL,
            category TEXT,
            mode TEXT
        )
    """)

    conn.commit()
    conn.close()