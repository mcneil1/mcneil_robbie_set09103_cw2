from app import db, bcrypt

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from hashlib import md5

Base = declarative_base()

followers = db.Table(
	'followers',	
	db.Column('follower_email', db.String, db.ForeignKey('user.email')),
	db.Column('followed_email', db.String, db.ForeignKey('user.email'))
)

class UserDB(db.Model):
	
	__tablename__ = "user"
	
	email = db.Column(db.String, primary_key=True)
	username = db.Column(db.String, nullable=False,unique=True)
	first_name = db.Column(db.String, nullable=False)
	last_name = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)
	posts = relationship("UserPosts", backref="author")

	followed = db.relationship(
		'UserDB', secondary=followers,
		primaryjoin=(followers.c.follower_email == email),
		secondaryjoin=(followers.c.followed_email == email),
	 	backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')


	def __init__(self,email,username,first_name,last_name,password):
		self.email = email
		self.username = username
		self.first_name = first_name
		self.last_name = last_name
		self.password = bcrypt.generate_password_hash(password)
		
	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self
	
	def is_following(self, user):
		return self.followed.filter(followers.c.followed_email == user.email).count() > 0

	def followed_posts(self):
		followed = UserPosts.query.join(
			followers, (followers.c.followed_email == UserPosts.author_email)).filter(
				followers.c.follower_email == self.email)
		own = UserPosts.query.filter_by(author_email=self.email)
		return followed.union(own).order_by(UserPosts.id.desc())

	def __repr__(self):
		return '{} - {} {} - {}'.format(self.username,self.first_name,self.last_name,self.password)


class UserPosts(db.Model):

	__tablename__ = "posts"

	id = db.Column(db.Integer, primary_key=True)
	header = db.Column(db.String, nullable=False)
	body = db.Column(db.String, nullable=False)
	date = db.Column(db.DateTime, nullable=False)
	author_email = db.Column(db.String, ForeignKey('user.email'))

	def __init__(self, header, body, date, author_email):
		self.header = header
		self.body = body
		self.date = date
		self.author_email = author_email

	def __repr__(self):
		return'<{} - {} - {}>'.format(self.header, self.body, self.date)


