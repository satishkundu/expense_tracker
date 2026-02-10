import sqlite3
import csv

def export_csv():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM transactions")
    data = cur.fetchall()

    with open("expenses_report.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID","Date","Category","Description","Amount","Type"])
        writer.writerows(data)

    conn.close()
    print("Data Exported Successfully!")
