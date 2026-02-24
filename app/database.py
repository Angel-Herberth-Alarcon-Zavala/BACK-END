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
