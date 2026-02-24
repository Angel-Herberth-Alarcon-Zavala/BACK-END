from sqlalchemy import Column, String, Float, Date
from app.database import Base
import uuid

class EgresosList(Base):
    __tablename__ = "egresos" 

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True)
    fecha = Column(Date)
    descripcion = Column(String) 
    monto = Column(Float)
    categoria = Column(String)