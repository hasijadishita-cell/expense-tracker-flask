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
                   amount REAL NOT NULL,
                   category TEXT NOT NULL,
                   expense_date DATE NOT NULL)
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
        category=request.form.get("category")
        expense_date=request.form["expense_date"]

        cursor.execute("INSERT INTO EXPENSES (description, amount, category, expense_date) VALUES (?, ?, ?, ?)", (description, amount, category, expense_date))
        con.commit()
        return redirect("/")
    selected_month=request.args.get("month")
    filter_category=request.args.get("filter_category")

    
    if selected_month!="all" and filter_category and filter_category!="all":
        cursor.execute("SELECT * FROM expenses WHERE CATEGORY=? AND strftime('%Y-%m', expense_date)=? ORDER BY expense_date DESC", (filter_category, selected_month))

    elif selected_month and selected_month!="all":
        cursor.execute("SELECT * FROM expenses WHERE strftime('%Y-%m', expense_date)=? ORDER BY expense_date DESC", (selected_month,))
    elif filter_category and filter_category!="all":
        cursor.execute("SELECT * FROM expenses WHERE CATEGORY=? ORDER BY expense_date DESC", (filter_category,))
    else:
        cursor.execute("SELECT * FROM expenses ORDER BY expense_date DESC")
    expenses=cursor.fetchall()

    if filter_category!="all" and filter_category and selected_month!="all":
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y-%m', expense_date)= ? AND category=?" , (selected_month, filter_category))
    elif selected_month and selected_month!="all":
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%Y-%m', expense_date)= ? " , (selected_month, ))

    elif filter_category and filter_category!="all":
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE CATEGORY=?", (filter_category,))
    else:
        cursor.execute("SELECT SUM(amount) FROM expenses")

    month_total=cursor.fetchone()[0]
    month_total=month_total if month_total else 0


    if selected_month and selected_month!="all":
        cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE strftime('%Y-%m', expense_date)=? GROUP BY category", (selected_month,))
    else:
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    category_summary=cursor.fetchall()
    category_summary=[(c, t or 0) for c, t in category_summary]
    con.close()
    return render_template("index.html", expenses=expenses, month_total=month_total, filter_category=filter_category, selected_month=selected_month, category_summary=category_summary)

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
