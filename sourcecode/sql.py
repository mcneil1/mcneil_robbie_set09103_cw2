import sqlite3

with sqlite3.connect("users.db") as connection:
	c = connection.cursor()
	c.execute("CREATE TABLE users(email TEXT,first_name TEXT, last_name TEXT, password TEXT)")
	c.execute("INSERT INTO users (email,first_name,last_name,password) VALUES ('robbiemcn98@gmail.com','Rob','McNeil','Password')")
