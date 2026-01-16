import sqlite3

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



# EXPORTING AND DOWNLOADING THE EXPENSES
def export_csv(selected_month):
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
    return rows, filename

    

    
