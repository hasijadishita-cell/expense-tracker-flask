# Expense Tracker (Flask + SQLite)

A simple web-based Expense Tracker built using **Flask** and **SQLite**.
It allows users to add expenses, filter them by month, view category-wise summaries (including a pie chart), and export expenses to CSV.

This project was built to practice **backend logic, database queries, templating (Jinja), and basic frontend integration**.

---

## Features

- Add expense with description, amount, category, and date
- Filter expenses by **month**
- View **total spending** for the selected month
- Category-wise expense summary
- Visual **pie chart** for category distribution
- Export expenses for a selected month as **CSV**
- Data stored locally using SQLite

---

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, Jinja templates
- **Charts:** Chart.js (via Content Delivery Network)

---

## Project Structure

Expense Tracker/
|
|
|____app.py           # Main Flask application
|
|___expenses.db       #SQLite database
|
|___requirements.txt  #Project dependencies
|
|___templates/
  |___index.html      #Main UI template
|
|___static/
  |___style.css       #Styling

---

## How It Works

- Users add expenses through a form in the web interface.
- Flask handles form submissions and stores data in a SQLite database.
- Expenses can be filtered by month using SQL querries.
- The backend calculates total spending and category-wise summaries.
- Category-wise data is visualized using  pie chart.
- Users can export monthly expense data as CSV file.

---

## Setup Instructions

1. clone the repository:
'''bash
git clone https://github.com/hasijadishita/expense-tracker-flask.git
cd expense-tracker-flask

2. Create a virtual environment:
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\scripts\activate        # Windows

3. Install Dependencies:
pip install -r requirements.txt

4. Run the application:
python app.py              # Windows
python3 app.py             # Mac/Linux

5. Live demo:
https://expense-tracker-flask-pb6g.onrender.com

---

## CSV Export

- Users can export expenses for a selected month.
- When the Export CSV button is clicked, the backend generates a CSV file.
- The file is automatically downloaded and can be opened in Excel or Google Sheets.
- CSV export is handled entirely on the server side using Flask responses.

---

## What I Learned

- Building a backend application using Flask and SQLite
- Writing SQL queries with filtering and aggregation
- Separating backend logic from frontend templates 
- Passing data safely from Flask to JavaScript
- Handling file downloads using HTTP response headers
- Refactoring large functions into reusable helper functions

---

## Future Improvements

- User authentication and multiple user accounts
- Editing and deleting existing expense
- Monthly comparison charts
- Converting the project into API

## Author 

Dishita Hasija
Bachelor of Engineering (Software Engineering)
RMIT University
