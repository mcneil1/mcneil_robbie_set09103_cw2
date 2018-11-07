from app import db

class UserDB(db.Model):
	
	__tablename__ = "users"
	
	email = db.Column(db.String, primary_key=True)
	first_name = db.Column(db.String, nullable=False)
	last_name = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)

	def __init__(self,email,first_name,last_name,password):
		self.email = email
		self.first_name = first_name
		self.last_name = last_name
		self.password = password

	def __repr__(self):
		return '<{} {}'.format(self.first_name,self.last_name) 
