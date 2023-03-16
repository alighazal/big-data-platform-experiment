from sqlalchemy import Column, Integer, String, ForeignKey, Table, Uuid, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, orm


Base = orm.declarative_base()
class Process(Base):
    __tablename__ = "process"
    process_id =  Column(String, primary_key=True)
    timestamp = Column(DateTime)
    # user_id = Column(Integer)
    status =  Column(String)

engine = create_engine("sqlite:///heyy.db", echo=True)



