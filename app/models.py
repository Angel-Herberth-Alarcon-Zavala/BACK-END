from sqlalchemy import UUID, Column, ForeignKey, String, Float, Date, Boolean
from app.database import Base
import uuid

class Egreso(Base):
    __tablename__ = "Egreso" 

    usuario_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("Usuario.usuario_id"))
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True)
    fecha = Column(Date)
    descripcion = Column(String) 
    monto = Column(Float)
    categoria = Column(String)

class Usuario(Base):
    __tablename__ = "Usuario"

    usuario_id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True)
    username = Column(String)
    email = Column(String) 
    password = Column(String)
    role = Column(String)
    verified = Column(Boolean)