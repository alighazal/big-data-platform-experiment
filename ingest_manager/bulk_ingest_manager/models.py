from sqlalchemy import Column, Integer, String, ForeignKey, Table, Uuid, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, orm


Base = orm.declarative_base()

class ProjectConstraints(Base):
    __tablename__ = "project_constraints"
    project_name =  Column(String, primary_key=True)
    allowed_file_ext =  Column(String)
    max_file_size =  Column(Integer)
    created_at = Column(DateTime)

engine = create_engine("sqlite:///project-constraints.db", echo=True)



