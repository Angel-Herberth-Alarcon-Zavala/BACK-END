import uuid
from sqlalchemy import Column, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID 
from app.database import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "Usuario"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        index=True
    )
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")
    verified = Column(Boolean, default=False)
    egreso = relationship("Egreso", back_populates="usuario")

class Egreso(Base):
    __tablename__ = "Egreso"

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        index=True
    )
    usuario_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("Usuario.id"), 
        nullable=False
    )
    fecha = Column(Date, nullable=False)
    descripcion = Column(String)
    monto = Column(Float, nullable=False)
    categoria = Column(String)
    usuario = relationship("Usuario", back_populates="egreso")