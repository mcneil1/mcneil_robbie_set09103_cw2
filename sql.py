import sqlite3

with sqlite3.connect("user.db") as connection:
	c = connection.cursor()
	c.execute("CREATE TABLE users(email TEXT, password TEXT)")

