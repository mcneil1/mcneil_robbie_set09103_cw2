from app import db
from models import UserDB

db.create_all()

db.session.add(UserDB("robbiemcn98@gmail.com","OG_Rob","Robbie","McNeil","password"))

db.session.commit()
