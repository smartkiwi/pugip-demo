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
    Column('obj_type', Integer, ForeignKey("obj_type.id"))
)

metric = Table(
    'metric', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('obj_type', Integer, ForeignKey("obj_type.id"))
)

metric_value = Table(
    'metric_value', metadata,
    Column('id', Integer, primary_key=True),
    Column('metric_id', Integer, ForeignKey("metric.id")),
    Column('object_id', Integer, ForeignKey("mon_obj.id")),
    Column('value', Float, nullable=False),
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


#select
select_stmt   = select([object_type.c.id, object_type.c.name]).where(or_(
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