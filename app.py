from flask import Flask, render_template, request, redirect
import sqlite3


app=Flask(__name__)
db_name="expenses.db"

def get_connection():
    return sqlite3.connect(db_name)

def init_db():
    con=get_connection()
    cursor=con.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   description TEXT NOT NULL,
                   amount REAL NOT NULL)
                   """)
    con.commit()
    con.close()


@app.route("/", methods=["GET", "POST"])

def index():
    con=get_connection()
    cursor=con.cursor()

    if request.method=="POST":
        description=request.form.get("description")
        amount=float(request.form["amount"])

        cursor.execute("INSERT INTO EXPENSES (description, amount) VALUES (?, ?)", (description, amount))
        con.commit()
        return redirect("/")
    
    cursor.execute("SELECT * FROM expenses")
    expenses=cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total=cursor.fetchone()[0]
    total=total if total else 0
    con.close()
    return render_template("index.html", expenses=expenses, total=total)

@app.route("/delete/<int:expense_id>", methods=["POST"])

def delete_expense(expense_id):
    con=get_connection()
    cursor=con.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    con.commit()
    con.close()
    return redirect("/")


if __name__=="__main__":
    init_db()
    app.run(debug=True)
