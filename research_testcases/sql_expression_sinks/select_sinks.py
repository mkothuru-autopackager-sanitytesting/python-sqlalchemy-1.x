# Attack Payload: "NULL OR 'x'='x'"
from sqlalchemy import create_engine
import sys
from sqlalchemy.sql import text
from sqlalchemy.sql import select

from sqlalchemy import Table, Column, Integer, String, MetaData

engine = create_engine("sqlite:///:memory:", echo=True)
metadata_obj = MetaData()
tainted_where = sys.argv[1]

users = Table(
	"users",
	metadata_obj,
	Column("id", Integer, primary_key=True),
	Column("name", String),
	Column("fullname", String),
)

metadata_obj.create_all(engine)	
conn = engine.connect()

ins = users.insert()
conn.execute(ins, {"id": 1, "name": "wendy", "fullname": "Wendy Williams"})
conn.execute(ins, {"id": 2, "name": "mansi", "fullname": "Mansi Sheth"})
conn.execute(ins, {"id": 3, "name": "dhaval", "fullname": "Dhaval Sheth"})

s = select(users).where(text(tainted_where)) 

result = conn.execute(s) # CWEID 89

for row in result:
	print("Select::Where" , row)

s = select(users).filter(text('id = {}'.format(tainted_where))) 
result = conn.execute(s) # CWEID 89

for row in result:
	print("Select::filter", row)
