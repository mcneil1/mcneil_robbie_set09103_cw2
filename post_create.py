from app import db
from models import UserPosts

db.create_all()

db.session.add(UserPosts("First post!", "Hello world, don't mind me, I'm just doing my Zuckerberg tings","robbiemcn98@gmail.com"))

db.session.commit()
