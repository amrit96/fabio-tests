from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///world.db', echo=True)

class Continent(Base):
    __tablename__ = 'continent'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    population = Column(Integer)
    area = Column(Float)


class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    population = Column(Integer)
    area = Column(Float)
    hospital_count = Column(Integer)
    national_park = Column(Integer)
    continent = Column(Integer, ForeignKey('continent.id'))


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    population = Column(Integer)
    area = Column(Float)
    road_count = Column(Integer)
    tree_count = Column(Integer)
    country = Column(Integer, ForeignKey('country.id'))


if __name__ == "__main__":
    Base.metadata.create_all(engine)