import datetime
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.sql.expression import case
from sqlalchemy.sql.functions import count
from sqlalchemy.types import Integer, String, DateTime

__author__ = 'vvlad'


Base = declarative_base()
class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    publication_date = Column(DateTime)
    pages_count = Column(Integer)
    author_id = Column(Integer, ForeignKey('author.id'))

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship(Book, backref="author")


db_uri = "sqlite:///"
engine = create_engine(db_uri, echo=False)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)



insert_stmt = Book.__table__.insert()
print insert_stmt
data = {'title': 'Essential SQLAlchemy', 'publication_date': datetime.datetime.strptime('2010-05-05', '%Y-%m-%d'),
        'pages_count': 240}
engine.connect().execute(insert_stmt, data)


session = Session(bind=engine)
q = session.query(Book).filter(Book.title == 'Essential SQLAlchemy')
print q
book = q.one()
print (book.id, book.title)


author = Author(name='Rick Copeland')
author.books.append(book)
session.add(book)
session.flush()

####
# select CASE WHEN (BOOK.pages_count > 200) THEN 1 ELSE 0 END is_novel, count(*)
# from BOOK
# group by CASE WHEN (BOOK.pages_count > 200) THEN 1 ELSE 0 END
# order by CASE WHEN (BOOK.pages_count > 200) THEN 1 ELSE 0 END
#
is_novel_column = case([(Book.pages_count>200, 1)], else_=0)
novel_query = session.query(is_novel_column.label('is_alias'), count()).\
    group_by(is_novel_column).\
    order_by(is_novel_column)

print novel_query
print novel_query.all()


session.close()



