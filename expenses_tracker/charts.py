import sqlite3
import matplotlib.pyplot as plt

def show_category_chart():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT category, SUM(amount) 
    FROM transactions 
    WHERE type='Expense'
    GROUP BY category
    """)

    data = cur.fetchall()
    conn.close()

    categories = [i[0] for i in data]
    amounts = [i[1] for i in data]

    plt.figure("Spending Chart")
    plt.pie(amounts, labels=categories, autopct="%1.1f%%")
    plt.title("Category Wise Spending")
    plt.show()
