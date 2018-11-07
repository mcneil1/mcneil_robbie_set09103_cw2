from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
#import sqlite3

app = Flask(__name__)

app.secret_key = "}lm';(:W7tA5Bot"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

from models import *



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
		enteredEmail = request.form['email']
		enteredPassword = request.form['password']
		user = UserDB.query.filter_by(email=enteredEmail).first()
		if user is None:
			error = "Email is incorrect"

		elif user.password != enteredPassword:
			error = "Password is Incorrect"
				
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
			userEmail = request.form['email']
			userPassword = request.form['password']
			userFName = request.form['first_name']
			userLName = request.form['last_name']	
				
			user = UserDB(email=userEmail,first_name=userFName,last_name=userLName,password=userPassword)
			db.session.add(user)
			db.session.commit()			

			session['logged_in'] = True
			return redirect(url_for('home'))
	return render_template('signup.html', error=error)


#def connect_db():
#	return sqlite3.connect(app.database)


if __name__ == '__main__' :
	app.run(debug=True)
