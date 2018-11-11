from app import db
from models import UserPosts
from datetime import datetime

db.create_all()

db.session.add(UserPosts("First post!", "Hello world, don't mind me, I'm just doing my Zuckerberg tings",datetime.now(),"robbiemcn98@gmail.com"))

db.session.commit()
