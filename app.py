from flask import Flask, render_template, request, redirect, Response
import sqlite3
import csv, io


app=Flask(__name__)
db_name="expenses.db"

def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
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






# ADD EXPENSES
def add_expense(description, amount, category, expense_date):
    con=get_connection()
    cursor=con.cursor()

    cursor.execute("""
                    INSERT INTO EXPENSES (description, amount, category, expense_date) VALUES (?, ?, ?, ?)"""
                       , (description, amount, category, expense_date))
    con.commit()
    con.close()

# GET ALL THE EXPENSES
def get_expenses(selected_month, filter_category):
    """
    Fetches expenses from th database based on the selected month and category filter.

    Returns a list of expense records ordered by data.
    """
    con=get_connection()
    cursor=con.cursor()
    if selected_month!="all" and filter_category and filter_category!="all":
        cursor.execute("SELECT * FROM expenses WHERE CATEGORY=? AND strftime('%Y-%m', expense_date)=? ORDER BY expense_date DESC", (filter_category, selected_month))

    elif selected_month and selected_month!="all":
        cursor.execute("SELECT * FROM expenses WHERE strftime('%Y-%m', expense_date)=? ORDER BY expense_date DESC", (selected_month,))
    elif filter_category and filter_category!="all":
        cursor.execute("SELECT * FROM expenses WHERE CATEGORY=? ORDER BY expense_date DESC", (filter_category,))
    else:
        cursor.execute("SELECT * FROM expenses ORDER BY expense_date DESC")
    expenses=cursor.fetchall()
    con.close()
    return expenses


# GET TOTAL EXPENSES
def get_total(selected_month, filter_category):
    """
    Calculates the total amount spent based on the selected month and category filter.

    Returns the total expense as a number.
    """
    con=get_connection()
    cursor=con.cursor()
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
    con.close()
    return month_total



# GET CATEGORY SUMMARY 
def get_category_summary(selected_month, filter_category):
    """
    Calculates the total spending per category for the selected month and category filter.
    Returns a list.
    """
    con=get_connection()
    cursor=con.cursor()
    if selected_month and selected_month!="all":
        cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE strftime('%Y-%m', expense_date)=? GROUP BY category", (selected_month,))
    else:
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    category_summary=cursor.fetchall()
    category_summary=[(c, t or 0) for c, t in category_summary]
    con.close()
    return category_summary

@app.route("/", methods=["GET", "POST"])
# MAIN LOOP
def index():
    """
    Main application route.

    Handles:
    - Adding new expense (POST request)
    - Filtering expenses by month and category (GET request)
    - Displaying totals and category summary
    """

    if request.method=="POST":
        add_expense(request.form.get("description"),
        float(request.form["amount"]),
        request.form.get("category"),
        request.form["expense_date"])
        return redirect("/")
        

    selected_month=request.args.get("month")
    filter_category=request.args.get("filter_category")

    expenses=get_expenses(selected_month, filter_category)
    month_total=get_total(selected_month, filter_category)
    category_summary=get_category_summary(selected_month, filter_category)

    return render_template(
        "index.html",
        expenses=expenses,
        month_total=month_total,
        category_summary=category_summary,
        selected_month=selected_month,
        filter_category=filter_category
    )

    
    

@app.route("/delete/<int:expense_id>", methods=["POST"])


# DELETE EXPENSE
def delete_expense(expense_id):
    """
    Deletes a single expense from the database using its unique ID.
    """
    con=get_connection()
    cursor=con.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    con.commit()
    con.close()
    return redirect("/")



@app.route("/export")

# EXPORTING AND DOWNLOADING THE EXPENSES
def export_csv():
    """
    Exports expense data for the selected month as a CSV file.

    The CSV file is generated dynamically and downloaded through the browser.
    """
    selected_month=request.args.get("month")
    con=get_connection()
    cursor=con.cursor()
    if selected_month and selected_month!="all":
        cursor.execute("SELECT * FROM expenses WHERE strftime('%Y-%m', expense_date)=?", (selected_month,))
        filename=f"expenses_{selected_month}.csv"
    else:
        cursor.execute("SELECT * FROM expenses")
        filename="expenses_all.csv"
    rows=cursor.fetchall()
    con.close()

    output=io.StringIO()
    writer=csv.writer(output)
    writer.writerow(["Description", "Amount", "Category", "Date"])
    for row in rows:
        writer.writerow(row)

    response=Response(
        output.getvalue(),
        mimetype="text/csv")
    response.headers["Content-Disposition"]=f"attachment; filename={filename}"
    return response

  

if __name__=="__main__":
    init_db()
    app.run(debug=True)
