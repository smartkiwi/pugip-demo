from sqlalchemy.engine import create_engine

engine = create_engine("sqlite:///")

connection = engine.connect()

#SQLite
r = connection.scalar("select datetime(current_timestamp, 'localtime');")
#Postgresql
#r = connection.scalar("select now();")
print r

connection.close()
