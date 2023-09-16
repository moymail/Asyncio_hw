from sqlalchemy import Column, Integer, JSON, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from dsn import engine


Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class SwapiPeople(Base):
    __tablename__ = "swapi_people"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=300))
    height = Column(String(length=200))
    mass = Column(String(length=100))
    hair_color = Column(String(length=100))
    skin_color = Column(String(length=100))
    eye_color = Column(String(length=100))
    birth_year = Column(String(length=100))
    gender = Column(String(length=100))
    homeworld = Column(String(length=300))
    films = Column(Text)
    species = Column(Text)
    vehicles = Column(Text)
    starships = Column(Text)