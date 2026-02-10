import sqlite3

def connect():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY,
        date TEXT,
        category TEXT,
        description TEXT,
        amount REAL,
        type TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert(date, category, description, amount, type):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO transactions VALUES (NULL,?,?,?,?,?)",
                (date, category, description, amount, type))

    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM transactions")
    rows = cur.fetchall()

    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM transactions WHERE id=?", (id,))

    conn.commit()
    conn.close()

def update(id, date, category, description, amount, type):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("""
    UPDATE transactions 
    SET date=?, category=?, description=?, amount=?, type=? 
    WHERE id=?
    """, (date, category, description, amount, type, id))

    conn.commit()
    conn.close()

def monthly_total():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT SUM(amount) FROM transactions WHERE type='Expense'
    """)

    total = cur.fetchone()[0]
    conn.close()

    return total if total else 0


connect()
