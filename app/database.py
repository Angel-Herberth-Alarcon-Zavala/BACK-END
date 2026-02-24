from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Falta dirección real de base de datos
CADENA_CONEXION = "postgresql://admin:admin@localhost:5432/bd_backend"

engine = create_engine(CADENA_CONEXION)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
    

CODIGOS_RECUPERACION = {}
USUARIOS = [
    {"id": 1, 
     "email": "admin@finanzapp.com", 
     "password": "123", 
     "role": "admin", 
     "username": "Administrador General",
     "verified": True},
    {"id": 2, 
     "email": "correo@gmail.com", 
     "password": "abc", 
     "role": "user", 
     "username": "Usuario Prueba",
     "verified": False}
]
EGRESOS = [
    {"fecha": "17-12-2025",
    "categoria": "Transporte",
    "descripcion": "Metropolitano",
    "monto": 20.00}
]
