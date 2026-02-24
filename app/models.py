from sqlalchemy import Column, String, Float, Date
from app.database import Base
import uuid

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    username = Column(String, unique=True)
    password = Column(String, unique=True)

class Egreso(Base):
    __tablename__ = "egreso" 
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True)
    fecha = Column(Date)
    descripcion = Column(String) 
    monto = Column(Float)
    categoria = Column(String)