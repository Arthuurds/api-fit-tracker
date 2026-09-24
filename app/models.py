from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    registros = relationship("RegistroExecucao", back_populates="usuario")

class Exercicio(Base):
    __tablename__ = "exercicios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    grupo_muscular = Column(String, nullable=False)

    registros = relationship("RegistroExecucao", back_populates="exercicio")

class RegistroExecucao(Base):
    __tablename__ = "registros"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    exercicio_id = Column(Integer, ForeignKey("exercicios.id"), nullable=False)
    carga_kg = Column(Float, nullable=False)
    repeticoes = Column(Integer, nullable=False)
    data = Column(DateTime, default=datetime.now)

    usuario = relationship("Usuario", back_populates="registros")
    exercicio = relationship("Exercicio", back_populates="registros")