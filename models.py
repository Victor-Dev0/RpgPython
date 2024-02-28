from sqlalchemy import create_engine, String, Integer, Column, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CONN = "sqlite:///personagem.db"

engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Personagem(Base):
    __tablename__ = "Personagem"
    id = Column(Integer, primary_key=True)
    Nome = Column(String(50), nullable=False)
    VidaMaxima = Column(Integer())
    Vida = Column(Integer())
    Dano = Column(Integer())
    Exp = Column(Integer())
    ExpMaxima = Column(Integer())
    Nivel = Column(Integer())

Base.metadata.create_all(engine)