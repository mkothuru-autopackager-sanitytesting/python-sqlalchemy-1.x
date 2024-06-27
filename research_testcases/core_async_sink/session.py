# Attack Payload: "NULL OR 'x'='x'"
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.sql import text
import asyncio
import sys
from sqlalchemy.orm import sessionmaker

engine = create_async_engine('sqlite+aiosqlite:///database.db', echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
id = sys.argv[1]

async def async_main():
	async with async_session() as session:
		stmt = text(f"SELECT * FROM students WHERE id = {id}")
		result = await session.execute(stmt) # CWEID 89
		for row in result:
			print('AsyncSession::execute ', row)

asyncio.run(async_main())
