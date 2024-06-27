# Attack Payload: "NULL' OR 'x'='x"
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import sys

engine = create_engine('sqlite+pysqlite:///database.db', echo=True)
id = sys.argv[1]

query = f"SELECT * FROM students WHERE id = '{id}'"
rs = engine.execute(query) # CWEID 89

for row in rs:
	print('Engine::execute' , row)
