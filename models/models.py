from sqlalchemy import Column, String, Integer, Text, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Categories(Base):
    __tablename__ = "Categories"
    id = Column(Integer, primary_key=True)
    name = Column(name="name", type_=String(250))
    value = Column(name="value", type_=String(250))


class Cities(Base):
    __tablename__ = "Cities"
    id = Column(Integer, primary_key=True)
    name = Column(name="name", type_=String(250))
    value = Column(name="value", type_=String(250))


class Advertisements(Base):
    __tablename__ = "Advertisements"
    id = Column(Integer, primary_key=True)
    category = Column(name="category", type_=String(250))
    city = Column(name="city", type_=String(250))
    id_ad = Column(name="id_ad", type_=String(50))
    title = Column(name="title", type_=String(1500))
    text = Column(name="text", type_=Text)
    listed = Column(name="listed", type_=Integer())
    phone_showed = Column(name="phone_showed", type_=Integer())
    email_sent = Column(name="email_sent", type_=Integer())
    shared = Column(name="shared", type_=Integer())
    add_followers = Column(name="add_followers", type_=Integer())
    renew = Column(name="renew", type_=Integer())
    phone = Column(name="phone", type_=String(1500))
    scraping_date = Column(name="scraping_date", type_=Date)


def create_db():
    engine = create_engine("sqlite:///../db/db.sqlite")
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
