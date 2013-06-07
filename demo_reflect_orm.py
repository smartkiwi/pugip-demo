#ORM mapping demo
#reflection

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import mapper
from sqlalchemy.orm.session import Session
from sqlalchemy.schema import Table, MetaData

dbname = "some.db"
db_uri = "sqlite:///%s" % dbname

class ObjectType(object):
    def __repr__(self):
        return "%s(id='%s', name='%s')" % (self.__class__.__name__, self.id, self.name)

class MonObject(object):
    pass

class Metric(object):
    pass


meta = MetaData()
e = create_engine(db_uri, echo=True)

obj_type = Table('obj_type', meta, autoload=True, autoload_with=e)


mapper(ObjectType, obj_type)


###doing queries
session = Session(bind=e)
q = session.query(ObjectType)
print q
result = q.all()
for r in result:
    print r

