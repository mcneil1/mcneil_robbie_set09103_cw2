from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import sqlite3

app = Flask(__name__)

app.secret_key = "}lm';(:W7tA5Bot"
app.database = "user.db"

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You mut login to access this page')
			return redirect(url_for('login'))
	return wrap


@app.route('/')
@login_required
def home():
	return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['email'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True
			flash('Successfully logged in!')
			return redirect(url_for('home'))
	return render_template('login.html', error=error)


@app.route('/logout/')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('Successfully logged out')
	return redirect(url_for('login'))


@app.route('/register/', methods=['GET','POST'])
def register():
	error = None
	if request.method == 'POST':
		if request.form['password'] != request.form['password-repeat']:
			error = 'Passwords do not match, please try again.'
		else:
			email = request.form['email']
			password = request.form['password']	
			
			g.db = connect_db()
			cur = g.db.execute('INSERT INTO users (email,password) VALUES (?,?)',(email,password) )
			g.db.commit()
			g.db.close()			

			session['logged_in'] = True
			return redirect(url_for('home'))
	return render_template('signup.html', error=error)


def connect_db():
	return sqlite3.connect(app.database)


if __name__ == '__main__' :
	app.run(debug=True)
