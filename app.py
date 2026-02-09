from flask import Flask, render_template, request, redirect, Response, flash
from db import *
import csv, io
import os


app=Flask(__name__)
app.secret_key=os.environ.get("SECRET_KEY")



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
        description=request.form.get("description")
        amount=float(request.form["amount"])
        category=request.form.get("category")
        expense_date=request.form["expense_date"]
        is_valid, error=validate_expense(description, amount, category, expense_date)
        if not is_valid:
            flash(error)
            return redirect("/")
            
        add_expense(description,amount, category, expense_date)
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
        filter_category=filter_category)
        

def validate_expense(description, amount, category, expense_date):
    """
    Validates expense from input before saving to database.
    Returns (True, None) if valid, otherwise (false, error_message).
    """
    if not description:
        return False, "Description is required."
    
    if not amount:
        return False, "Amount is required."
    
    try:
        amount=float(amount)
        if amount<=0:
            return False, "Amount must be grater than zero."
    except ValueError:
        return False, "Amount must be a number."
    
    if not category:
        return False,"Category is required."
    if not expense_date:
        return False, "Date is required."
    return True, None
    
    

@app.route("/delete/<int:expense_id>", methods=["POST"])


def delete_expense_route(expense_id):
    delete_expense(expense_id)
    return redirect("/")



@app.route("/export")

def export_csv_route():
    selected_month=request.args.get("month")
    
    rows, filename=export_csv(selected_month)
    

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
