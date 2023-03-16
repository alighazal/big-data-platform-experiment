from sqlalchemy import Column, Integer, String, ForeignKey, Table, Uuid, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, orm


Base = orm.declarative_base()
class IngestionEvent(Base):
    __tablename__ = "logs"
    id =  Column(String, primary_key=True)
    status =  Column(String)
    src =  Column(String)
    records_count =  Column(String)
    timestamp = Column(DateTime)

engine = create_engine("sqlite:///logs.db", echo=True)



