from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_bcrypt import Bcrypt
from datetime import datetime
#import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)

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


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		date = datetime.now()
		email = session['email']
		post = UserPosts(header=title,body=body,date=date,author_email=email)
		db.session.add(post)
		db.session.commit()

	posts = db.session.query(UserPosts).all()
	return render_template('index.html',posts=posts)


@app.route('/login/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		enteredEmail = request.form['email']
		enteredPassword = request.form['password']
		user = UserDB.query.filter_by(email=enteredEmail).first()
		if user is None:
			error = "Email is incorrect"

		elif bcrypt.check_password_hash(user.password, enteredPassword) != True:
			error = "Password is Incorrect"
				
		else:
			session['logged_in'] = True
			session['email'] = request.form['email']
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
		userEmail = request.form['email']
		userName = request.form['username']
		newUser = UserDB.query.filter_by(email=userEmail).first()
		newUsername = UserDB.query.filter_by(username=userName).scalar()

		if request.form['password'] != request.form['password-repeat']:
			error = 'Passwords do not match, please try again.'

		if newUsername is not None:
			error = 'Username is taken!'
		
		elif newUser is None:	
			userPassword = request.form['password']
			userFName = request.form['first_name']
			userLName = request.form['last_name']	
				
			user = UserDB(email=userEmail,first_name=userFName,last_name=userLName,password=userPassword)
			db.session.add(user)
			db.session.commit()			

			session['logged_in'] = True
			return redirect(url_for('home'))
	
		else: 
			error = 'Username is taken!'
	return render_template('signup.html', error=error)


#def connect_db():
#	return sqlite3.connect(app.database)


if __name__ == '__main__' :
	app.run(debug=True)
