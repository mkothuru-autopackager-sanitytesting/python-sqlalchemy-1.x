---
**Note:** Latest version of this document is at https://veracode.atlassian.net/wiki/spaces/RES/pages/2035187842/Python+SQLAlchemy+1.x
---
# SQLAlchemy

As of this research work, latest version is 1.4. 

# Modeling

T = Return values of function text() from class [sqlalchemy.sql.elements.TextClause](https://github.com/sqlalchemy/sqlalchemy/blob/main/lib/sqlalchemy/sql/elements.py) should be considered tainted if arguments of text() function is non-parameterized query strings. Non-parameterized queries could also be string variables in certain APIs. You can consider these as a propogators.

Examples of non-parameterized payloads which are commonly seen:

```
text("fullname from users where name = " + tainted_filter)
```

```
text(f"SELECT * FROM students WHERE id = {id}")
```

```
query = "SELECT * FROM students WHERE id = " + id
rs = session.execute(query) # CWEID 89
```

```
query = text('select * from students where id=%s' % id)
rs = connection.execute(query) # CWEID 89
```

```
text(tainted_data)
```

# Taint Analysis

|Class|Source|Sink|Propogators|CWEID|Notes|Testcases|
|---|---|---|---|---|---|---|
|sqlalchemy.engine.Connection||exec_driver_sql(T,..)||89|T = non-parameterized SQL query, either string or thru `sqlalchemy.sql.text()` method|[core_sync_sinks/connection.py](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/blob/main/research_testcases/core_sync_sink/connection.py)|
|sqlalchemy.engine.Engine||execute(T,...)||89|T = non-parameterized SQL query, either string or thru `sqlalchemy.sql.text()` method|[core_sync_sinks/engine.py](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/blob/main/research_testcases/core_sync_sink/engine.py)|
|sqlalchemy.ext.asyncio.AsyncConnection||execute(T,...)||89|T = non-parameterized SQL query, either string or thru `sqlalchemy.sql.text()` method|[core_async_sinks/connection.py](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/blob/main/research_testcases/core_async_sink/connection.py)|
|sqlalchemy.ext.asyncio.AsyncConnection||exec_driver_sql(T,...)||89|T = non-parameterized SQL query, either string or thru `sqlalchemy.sql.text()` method|[core_async_sinks/connection.py](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/blob/main/research_testcases/core_async_sink/connection.py)|
|sqlalchemy.ext.asyncio.AsyncSession||execute(T,...)||89|T = non-parameterized SQL query, either string or thru `sqlalchemy.sql.text()` method|[core_async_sinks/session.py](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/blob/main/research_testcases/core_async_sink/session.py)|
|sqlalchemy.orm.session.Session||query(T)||89|T=non-parameterized query|[orm_functionality/query_sinks.py](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/blob/main/research_testcases/orm_functionality/query_sinks.py)|
|sqlalchemy.orm.query.Query||filter(T)||89|T=non-parameterized query|[orm_functionality/query_sinks.py](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/blob/main/research_testcases/orm_functionality/query_sinks.py)|
|sqlalchemy.orm.query.Query||from_statement(T)||89|T=non-parameterized query|[orm_functionality/query_sinks.py](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/blob/main/research_testcases/orm_functionality/query_sinks.py)|
|sqlalchemy.orm.query.Query||prefix_with(T)||89|T=non-parameterized query|[orm_functionality/query_sinks.py](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/blob/main/research_testcases/orm_functionality/query_sinks.py)|
|sqlalchemy.orm.query.Query||where(T)||89|T=non-parameterized query|[orm_functionality/query_sinks.py](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/blob/main/research_testcases/orm_functionality/query_sinks.py)|
|sqlalchemy.orm.query.Query||distinct(T)||89|T=non-parameterized query|[orm_functionality/query_sinks.py](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/blob/main/research_testcases/orm_functionality/query_sinks.py)|
|sqlalchemy.orm.query.Query||order_by(T)||89|T=non-parameterized query|[orm_functionality/query_sinks.py](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/blob/main/research_testcases/orm_functionality/query_sinks.py)|
|sqlalchemy.orm.query.Query||having(T)||89|T=non-parameterized query|[orm_functionality/query_sinks.py](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/blob/main/research_testcases/orm_functionality/query_sinks.py)|
|sqlite3.Cursor||execute(T)||89|T = non-parameterized SQL query, either string |[core_sync_sinks/connection.py](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/blob/main/research_testcases/core_sync_sink/connection.py)|
|sqlalchemy.orm.scoping.scoped_session||execute(T)||89|T = Non-parameterized sql query or string|[flask-sqlalchemy-simple]()|
|sqlalchemy.engine.base.Engine||execute(T)||89|T = non-parameterized query or string|[flask-sqlalchemy-simple]()|


**Note:**
- Sinks from `sqlalchemy.orm.query.Query` namespace would be applied on a Model which would be a class. However good thing is, irrespective of Model class defination, we should just look at above configured sinks and if it has non-parameterized queries.

Fix existing scanner:
- `sqlalchemy.sql.text` shouldn't be a sink. However we still need to parse it to identify non-parameterized queries being passed to `execute` methods. But flag it at `execute` method only. Refer testcases under [core_sync_sinks](https://gitlab.laputa.veracode.io/research-roadmap/python-sqlalchemy-1.x/-/tree/main/research_testcases/core_sync_sink)

- Namespace of sinks starting with `Query` is incorrect. All should be renamed to `sqlalchemy.orm.Query`.
- Change `sqlalchemy.orm.Session.session.execute` to `sqlalchemy.orm.session.Session.execute`, note the capital & small case "S" in both the sessions.

- Remove below sinks:
```
sqlalchemy.sql.select.limit
sqlalchemy.sql.select.offset
sqlalchemy.orm.Query.limit
sqlalchemy.orm.Query.offset
sqlalchemy.sql.select.update
sqlalchemy.sql.insert
sqlalchemy.sql.delete
sqlalchemy.sql.update
sqlalchemy.orm.Query.limit
sqlalchemy.orm.Query.offset
sqlalchemy.orm.Query.filter
sqlalchemy.orm.Query.from_statement
sqlalchemy.orm.Query.where
```



----------------------------------------------------


Research Workarea:

ToDo:

Existing sinks:

```
sqlalchemy.sql.text,call,Call,taint,sink,89,0,sql_injection_python -- remove
sqlalchemy.sql.insert,call,Call,taint,sink,89,ANY,sql_injection_python -- remove
sqlalchemy.sql.delete,call,Call,taint,sink,89,ANY,sql_injection_python -- remove
sqlalchemy.sql.update,call,Call,taint,sink,89,ANY,sql_injection_python -- remove
sqlalchemy.sql.select.limit,call,Call,taint,sink,89,0,sql_injection_python -- remove
sqlalchemy.sql.select.offset,call,Call,taint,sink,89,0,sql_injection_python -- remove
sqlalchemy.sql.select.where,call,Call,taint,sink,89,0,sql_injection_python --- testcase exists
sqlalchemy.sql.select.filter,call,Call,taint,sink,89,0,sql_injection_python --- testcase exists
sqlalchemy.sql.select.update,call,Call,taint,sink,89,0,sql_injection_python -- remove

sqlalchemy.engine.Connection.execute,call,Call,taint,sink,89,0,sql_injection_python -- added in core_sync_sinks/connection.py
sqlalchemy.orm.Session.session.execute,call,Call,taint,sink,89,0,sql_injection_python -- added in core_sync_sinks/session.py

sqlalchemy.orm.Query.from_statement,call,Call,taint,sink,89,0,sql_injection_python -- remove
sqlalchemy.orm.Query.prefix_with,call,Call,taint,sink,89,0,sql_injection_python
sqlalchemy.orm.Query.where,call,Call,taint,sink,89,0,sql_injection_python -- done
sqlalchemy.orm.Query.insert,call,Call,taint,sink,89,0,sql_injection_python -- remove
sqlalchemy.orm.Query.delete,call,Call,taint,sink,89,0,sql_injection_python -- remove
sqlalchemy.orm.Query.update,call,Call,taint,sink,89,0,sql_injection_python -- remove
sqlalchemy.orm.Query.filter,call,Call,taint,sink,89,0,sql_injection_python -- removed
#flask.g.session.query.filter,call,Call,taint,sink,89,0,sql_injection_python
sqlalchemy.orm.Session.query.filter,call,Call,taint,sink,89,0,sql_injection_python --- testcase exists
sqlalchemy.orm.Query.limit,call,Call,taint,sink,89,0,sql_injection_python -- remove
sqlalchemy.orm.Query.offset,call,Call,taint,sink,89,0,sql_injection_python -- remove
```

# Reference:
- [Architectural Overview](https://docs.sqlalchemy.org/en/14/intro.html)
- [SQLAlchemy What's New in 1.4](https://docs.sqlalchemy.org/en/14/changelog/migration_14.html)
