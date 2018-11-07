from app import db
from models import UserDB

db.create_all()

db.session.add(UserDB("rmcneil98@outlook.com","Robbie","McNeil","Admin"))

db.session.commit()
