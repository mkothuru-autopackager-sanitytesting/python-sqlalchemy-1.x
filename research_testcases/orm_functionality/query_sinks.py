# Attack Payload: "NULL OR 'x'='x'"
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Query
from sqlalchemy.orm import declarative_base
import sys
from sqlalchemy.sql import text, select

engine = create_engine("sqlite:///:memory:", echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	name = Column(String)
	fullname = Column(String)
	nickname = Column(String)
	
	def __repr__(self):
		return "<User(name='%s', fullname='%s', nickname='%s')>" % (
			self.name,
			self.fullname,
			self.nickname,
		)

print(User.__table__)	

Base.metadata.create_all(engine)
session.add_all(
	[
		User(name="wendy", fullname="Wendy Williams", nickname="windy"),
		User(name="mary", fullname="Mary Contrary", nickname="mary"),
		User(name="fred", fullname="Fred Flintstone", nickname="freddy"),
		User(name="ed", fullname="Ed Jones", nickname="edsnickname"),
	]
)
session.commit()
tainted_filter=sys.argv[1]

#ed = session.query(User).filter(User.name==tainted_filter)
#ed = session.query(User).filter_by(name="ed").first()

result = session.query(text("fullname from users where name = " + tainted_filter)) # CWEID 89

for row in result:
	print("Session::query " , row)

result = session.query(User).filter(text('id = {}'.format(tainted_filter))) # CWEID 89

for row in result:
	print("Query::filter", row)

result = session.query(User).from_statement(text("select id, name, nickname, fullname from users where id = "+ tainted_filter)) # CWEID 89

for row in result:
	print("Query::from_statement", row)

## Current payload doesn't work, but any prefix could be manipulated and injected
stmt = select(User).prefix_with(tainted_filter, dialect="sqlite") # CWEID 89
result = session.execute(stmt)

for row in result:
	print("Query::prefix_with" , row)

result = session.query(text("fullname from users")).where(text('id = {}'.format(tainted_filter))) # CWEID 89
# Namespace for result == <class 'sqlalchemy.orm.query.Query'>

for row in result:
	print('Session::Query::where' , row)

result = session.query(text("fullname from users")).distinct(text('id = {}'.format(tainted_filter))) # CWEID 89

for row in result:
	print('Session::Query::distinct' , row)

result = session.query(text("fullname from users")).order_by(text('id = {}'.format(tainted_filter))) # CWEID 89

for row in result:
	print('Session::Query::order_by' , row)

result = session.query(text("fullname from users")).group_by(text('id = {}'.format(tainted_filter))) # CWEID 89

for row in result:
	print('Session::Query::group_by' , row)

result = session.query(text("fullname from users")).group_by(text('id = {}'.format(1))).having(text('id = {}'.format(tainted_filter))) # CWEID 89

for row in result:
	print('Session::Query::having' , row)

#for c in dir(session.query(User)):
#	print(c)
