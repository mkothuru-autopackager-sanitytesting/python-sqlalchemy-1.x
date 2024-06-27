# Attack Payload: "NULL OR 'x'='x'"
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import sys

engine = create_engine('sqlite+pysqlite:///database.db', echo=True)
id = sys.argv[1]

Session = sessionmaker(engine)

with Session() as session:
	query = "SELECT * FROM students WHERE id = " + id 
	rs = session.execute(query) # CWEID 89

	for row in rs:
		print('Session::execute' , row)

	query = "SELECT * FROM students where id = 1"
	rs = session.execute(query) # FP CWEID 89

	for row in rs:
		print("Session::execute::FP", row)
