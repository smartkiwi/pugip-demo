import datetime
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.schema import MetaData, Column, ForeignKey
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
    birth_date = Column(DateTime)
    books = relationship(Book, backref="author")


db_uri = "sqlite:///"

engine = create_engine(db_uri, echo=True)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session = Session(bind=engine)

book = Book()
book.title = 'Essential SQLAlchemy'
book.publication_date = datetime.datetime.strptime('2010-05-05','%Y-%m-%d')
book.pages_count = 240

author = Author(name='Rick Copeland')
author.books.append(book)
session.add(book)

session.flush()
session.close()



