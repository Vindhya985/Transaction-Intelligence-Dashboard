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
            category TEXT
        )
    """)

    conn.commit()
    conn.close()

def store_transactions(df):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR REPLACE INTO transactions (
                transaction_id,
                date,
                description,
                debit,
                credit,
                balance,
                category
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            row["Transaction_ID"],
            row["Date"],
            row["Description"],
            row["Debit"],
            row["Credit"],
            row["Balance"],
            row["Category"]
        ))

    conn.commit()
    conn.close()
def get_transactions():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]