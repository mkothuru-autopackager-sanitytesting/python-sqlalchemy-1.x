# Attack Payload: "NULL OR 'x'='x'"
from sqlalchemy import create_engine
import sys
from sqlalchemy.sql import text

engine = create_engine('sqlite+pysqlite:///database.db', echo=True)
id = sys.argv[1]


with engine.connect() as connection:
	query = text('select * from students where id=%s' % id)
	rs = connection.execute(query) # CWEID 89

	for row in rs:
		print('Connection::execute' , row)

	query = f"SELECT * FROM students WHERE id = {id}"

	rs = connection.exec_driver_sql(query) # CWEID 89

	for row in rs:
		print('Connection::exec_driver_sql' , row)

connection = engine.raw_connection()
try:
	cursor = connection.cursor()
	rs = cursor.execute(query) # CWEID 89
	for row in rs:
		print('Connection::cursor', row)
finally:
	connection.close()
