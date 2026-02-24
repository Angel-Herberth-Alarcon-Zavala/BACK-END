from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Imports de routers y base de datos
from app.database import get_db
from app.models import EgresosList
from app.schemas import EgresoUpdate

router = APIRouter(
    prefix="/egresos", 
    tags=["Egresos"])

@router.get("/")
def get_egresos(db: Session = Depends(get_db)):
    lista_egresos = db.query(EgresosList).all()
    return lista_egresos

@router.put("/{egreso_id}")
def edit_egreso(egreso_id: str, db: Session = Depends(get_db)):
    pass

