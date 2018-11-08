from app import db, bcrypt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class UserDB(db.Model):
	
	__tablename__ = "users"
	
	email = db.Column(db.String, primary_key=True)
	first_name = db.Column(db.String, nullable=False)
	last_name = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)
	posts = relationship("UserPosts", backref="author")

	def __init__(self,email,first_name,last_name,password):
		self.email = email
		self.first_name = first_name
		self.last_name = last_name
		self.password = bcrypt.generate_password_hash(password)

	def __repr__(self):
		return '{} {} - {}'.format(self.first_name,self.last_name,self.password)


class UserPosts(db.Model):

	__tablename__ = "posts"

	id = db.Column(db.Integer, primary_key=True)
	header = db.Column(db.String, nullable=False)
	body = db.Column(db.String, nullable=False)
	author_email = db.Column(db.String, ForeignKey('users.email'))

	def __init__(self, header, body, author_email):
		self.header = header
		self.body = body
		self.author_email = author_email

	def __repr__(self):
		return'<{} - {}>'.format(self.header, self.body)
