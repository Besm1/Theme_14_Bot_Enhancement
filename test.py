import pprint
from distutils.util import execute
from sqlite3 import Connection, Cursor

connection = Connection('healthcare_shop.db')
cursor = connection.cursor()

cursor.execute('''
create table if not exists test (
id INTEGER PRIMARY KEY
, t text)
''')
connection.commit()

nmax = cursor.execute('select max(id) from test').fetchone()[0]
nmax = 1 if nmax is None else nmax + 1

for i in range(10):
    cursor.execute(f"insert into test (t) values ('text number {nmax + i}')")
connection.commit()

pprint.pprint(cursor.execute('select * from test').fetchall())

connection.close()