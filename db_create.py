from app import db
from models import UserDB

db.create_all()

db.session.add(UserDB("robbiemcn98@gmail.com","Robbie","McNeil","password"))

db.session.commit()
