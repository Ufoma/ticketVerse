from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

# Configure the db url
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLALchemy and Migrate
db = SQLAlchemy(app)
Migrate = Migrate(app, db)


# test


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        # Query the database for the user
        user = User.query.filter_by(username=username).first()

        # Check hashed password
        if user and check_password_hash(user.password, password):
            # Password is correct, log the user in (this could be a session setup, etc.)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to home or dashboard
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('signin.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


# @app.route('/signout')
# def logout():
#     return render_template('signout.html')


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


if __name__ == '__main__':
    app.run(debug=True)
