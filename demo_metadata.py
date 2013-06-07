# metadata demo:
# - defining and creating tables
# - populating records
# - selecting records

dbname = "some.db"
db_uri = "sqlite:///%s" % dbname

from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData, Table, Column, ForeignKey
from sqlalchemy.sql.expression import select, or_
from sqlalchemy.types import Integer, String, Float

metadata = MetaData()

object_type = Table(
    'obj_type', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String)
)

mon_obj = Table(
    'mon_obj', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('obj_type_id', Integer, ForeignKey("obj_type.id"))
)




engine = create_engine(db_uri, echo=True)
metadata.drop_all(engine)
metadata.create_all(engine)

#populate records into Object Type table:
conn = engine.connect()
data = []

for i in xrange(9):
    data.append({'name': "type%s" % i})

insert_stmt = object_type.insert()
print insert_stmt
conn.execute(insert_stmt, data)


#inserting related object - boring at this point - need to know related object_type id

insert_stmt2 = mon_obj.insert()
data2 = []
for j in xrange(4):
    for i in xrange(4):
        data2.append({'name':"obj%s" % j, 'obj_type_id': i})
conn.execute(insert_stmt2, data2)

#select
select_stmt = select([object_type.c.id, object_type.c.name]).where(or_(
    object_type.c.name.like("%1"),
    object_type.c.name.like("%4")
    )
)
print select_stmt
result = conn.execute(select_stmt)
print result.keys()
for row in result:
    print row

conn.close()