import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'test'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        # Query the user by email and password
        cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        # Assuming password is the 3rd column
        if user and check_password_hash(user[2], password):
            # Assuming user ID is the first column
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    # You need to return the signin form if not POST
    return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user (email, password) VALUES (?, ?)", (email, hashed_password))
        conn.commit()
        conn.close()

        flash('Registration successful. Please sign in.', 'success')
        return redirect(url_for('signin'))

    return render_template('signup.html')


def init_db():
    try:
        with sqlite3.connect('user.db') as conn:
            cursor = conn.cursor()

            # Check if the table already exists
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
            table_exists = cursor.fetchone()

            if table_exists:
                print("Table 'user' already exists.")
            else:
                # Create the user table if it doesn't exist
                cursor.execute(""" 
                CREATE TABLE user ( 
                    id INTEGER PRIMARY KEY, 
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                ); 
                """)
                print("Table 'user' created.")

            # Commit the transaction
            conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def init_db():
    try:
        with sqlite3.connect('user.db') as conn:
            cursor = conn.cursor()

            # Check if the table already exists
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
            table_exists = cursor.fetchone()

            if table_exists:
                print("Table 'user' already exists.")
            else:
                # Create the user table if it doesn't exist
                cursor.execute(""" 
                CREATE TABLE user ( 
                    id INTEGER PRIMARY KEY, 
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                ); 
                """)
                print("Table 'user' created.")

            # Commit the transaction
            conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('signin'))
    return render_template('dashboard.html')


@app.route('/signout')
def signout():
    session.pop('user_id', None)  # Remove user from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('signin'))


@app.route('/about')
def about():
    return render_template('/pages/about.html')


@app.route('/help')
def help():
    return render_template('/pages/help.html')


@app.route('/buy')
def buy():
    return render_template('/pages/buy.html')


@app.route('/calendar')
def calendar():
    return render_template('/pages/calendar.html')


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
