import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        date TEXT,
        category TEXT,
        amount REAL,
        description TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = request.form['amount']
        description = request.form['description']

        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (date, category, amount, description) VALUES (?, ?, ?, ?)", 
                       (date, category, amount, description))

        conn.commit()
        conn.close()
        
        return redirect(url_for('home'))

    return render_template('add_transaction.html')

@app.route('/transactions')
def view_transactions():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    conn.close()
    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
