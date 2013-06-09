#ORM mapping demo
#reflection

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.schema import Table, MetaData

dbname = "some.db"
db_uri = "sqlite:///%s" % dbname


class ObjectType(object):
    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "%s(id='%s', name='%s')" % (self.__class__.__name__, self.id, self.name)

class MonObject(object):
    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "%s(id='%s', name='%s', obj_type_id='%s')" % (
        self.__class__.__name__, self.id, self.name, self.obj_type_id)


meta = MetaData()


e = create_engine(db_uri, echo=True)

obj_type_table = Table('obj_type', meta, autoload=True, autoload_with=e)
mon_obj_table = Table('mon_obj', meta, autoload=True, autoload_with=e)



mapper(MonObject, mon_obj_table)
mapper(ObjectType, obj_type_table,
       properties={'objects': relationship(
                    MonObject,
                    primaryjoin=(obj_type_table.c.id == mon_obj_table.c.obj_type_id),
                    backref="obj_type"
       )
    }
)



###doing queries
session = Session(bind=e)
q = session.query(ObjectType).filter(ObjectType.id<3)
print q
result = q.all()
for r in result:
    print r
    print len(r.objects)
    print r.objects


###creating objects
for i in xrange(4):
    new_obj_type = ObjectType(name="new_type%s" % i)
    for j in xrange(4):
        new_mon_obj = MonObject(name="new_mon_obj%s" % j)
        new_obj_type.objects.append(new_mon_obj)
    session.add(new_mon_obj)

session.flush()
session.commit()


