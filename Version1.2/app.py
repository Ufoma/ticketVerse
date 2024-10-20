from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def signin():
    return render_template('signin.html')


@app.route('/signup')
def signup():
    return render_template('signuup.html')


@app.route('/signout')
def logout():
    return render_template('signout.html')


@app.route('/about')
def about():
    return render_template('/pages/about.html')


@app.route('/help')
def help():
    return render_template('/pages/help.html')


@app.route('/buy')
def buy():
    return render_template('/pages/buy.html')


@app.route('/calender')
def calender():
    return render_template('/pages/calender.html')


if __name__ == '__main__':
    app.run(debug=True)
