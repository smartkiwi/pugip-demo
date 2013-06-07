import os
from sqlalchemy.engine import create_engine

dbname = "some.db"
db_uri = "sqlite:///%s" % dbname
if os.path.exists(dbname):
    os.remove(dbname)

engine = create_engine(db_uri)

connection = engine.connect()

#SQLite
r = connection.scalar("select datetime(current_timestamp, 'localtime');")
#Postgresql
#r = connection.scalar("select now();")
print r

connection.close()
