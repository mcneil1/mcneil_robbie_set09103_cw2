from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy import desc
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
			flash('You must login to access this page')
			return redirect(url_for('login'))
	return wrap


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():

	email = session['email']
	current_user = UserDB.query.filter_by(email = email).first()
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		date = datetime.now()

		post = UserPosts(header=title,body=body,date=date,author_email=email)
		db.session.add(post)
		db.session.commit()

	posts = current_user.followed_posts().all()
	userUsername = session['username']
	profileURL = "http://set09103.napier.ac.uk:9159/profile/" + userUsername + "/"
	return render_template('index.html',posts=posts,profileURL=profileURL)


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
			session['username'] = user.username
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
	
			user = UserDB(email=userEmail,username=userName,first_name=userFName,last_name=userLName,password=userPassword)
			db.session.add(user)
			db.session.commit()			

			session['logged_in'] = True
			session['email'] = userEmail
			session['username'] = userName
			return redirect(url_for('home'))
	
		else: 
			error = 'Username is taken!'
	return render_template('signup.html', error=error)

@app.route('/profile/<username>/')         
@login_required
def profile(username):

	user = UserDB.query.filter_by(username=username).first()

	userUsername = session['username']
	thisUser = UserDB.query.filter_by(username=userUsername).first()
	
	if user is None:
		return render_template('404.html')
	 
	name = user.first_name + " " + user.last_name	
	profileURL = "http://set09103.napier.ac.uk:9159/profile/" + userUsername + "/"
	email = session['email']

	posts = db.session.query(UserPosts).filter_by(author_email=user.email).all()
	posts.reverse()
 
	return render_template('profile.html',thisUser=thisUser,user=user,username=username,posts=posts,name=name,profileURL=profileURL)


@app.route('/explore/')
@login_required
def explore():
	userUsername = session['username']
	profileURL = "http://set09103.napier.ac.uk:9159/profile/" + userUsername + "/"
	posts = db.session.query(UserPosts).all()
	posts.reverse()
	return render_template('explore.html',profileURL=profileURL,posts=posts)
	

@app.route('/follow/<username>/')
@login_required
def follow(username):
	user = UserDB.query.filter_by(username=username).first()
	thisUser = session['username']
	current_user = UserDB.query.filter_by(username=thisUser).first()
	if user is None:
		flash('User @{} not found.'.format(username))
		return redirect(url_for('home'))
	if user == current_user:
		flash('You cannot follow yourself.')
		return redirect(url_for('profile', username = username))
	current_user.follow(user)
	db.session.commit()
	flash('You are now following @{}!'.format(username))
	return redirect(url_for('profile', username=username))


@app.route('/unfollow/<username>/')
@login_required
def unfollow(username):
        user = UserDB.query.filter_by(username=username).first()
        thisUser = session['username']
        current_user = UserDB.query.filter_by(username=thisUser).first()
        if user is None:
                flash('User @{} not found.'.format(username))
                return redirect(url_for('home'))
        if user == current_user:
                flash('You cannot unfollow yourself.')
                return redirect(url_for('profile', username = username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are no longer following @{}!'.format(username))
        return redirect(url_for('profile', username=username))



@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'), 404

#def connect_db():
#	return sqlite3.connect(app.database)


if __name__ == '__main__' :
	app.run(debug=True)
