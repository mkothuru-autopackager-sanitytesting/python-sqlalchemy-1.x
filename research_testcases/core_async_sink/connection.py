# Attack Payload: "NULL OR 'x'='x'"
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from sqlalchemy.sql import text
import sys

engine = create_async_engine('sqlite+aiosqlite:///database.db', echo=True)
id = sys.argv[1]

async def async_main():
	async with engine.connect() as connection:
		stmt = text(f"SELECT * FROM students WHERE id = {id}")
		result = await connection.execute(stmt)	# CWEID 89
		for row in result:
			print('AsyncConnection::execute ', row)

asyncio.run(async_main())
