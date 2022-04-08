from sqlalchemy import create_engine, Table, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///world.db', echo=True)

class Continent(Base):
    __tablename_ = 'continent'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    population = Column(Integer)
    area = Column(Float)


class Country(Base):
    __tablename_ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    population = Column(Integer)
    area = Column(Float)
    hospital_count = Column(Integer)
    national_park = Column(Integer)


class City(Base):
    __tablename_ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    population = Column(Integer)
    area = Column(Float)
    road_count = Column(Integer)
    tree_count = Column(Integer)