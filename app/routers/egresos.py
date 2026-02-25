from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

# Imports de routers y base de datos
from app.database import get_db
from app.models import Egreso
from app.schemas import EgresoCreate, EgresoUpdate

router = APIRouter(
    prefix="/egresos", 
    tags=["Egresos"])

@router.get("/{usuario_id}")
def obtener_egresos_usuario(usuario_id: uuid.UUID, db: Session = Depends(get_db)):
    lista_egresos = db.query(Egreso).filter(Egreso.usuario_id == usuario_id).all()
    return lista_egresos

@router.post("/")
def crear_egreso(datos: EgresoCreate, db: Session = Depends(get_db)):
    nuevo_egreso = Egreso(
        fecha=datos.fecha,
        descripcion=datos.descripcion,
        monto=datos.monto,
        categoria=datos.categoria,
        usuario_id=datos.usuario_id
    )

    db.add(nuevo_egreso)
    db.commit()
    db.refresh(nuevo_egreso)

    return nuevo_egreso

@router.put("/{egreso_id}")
def editar_egreso(egreso_id: uuid.UUID, datos: EgresoUpdate, db: Session = Depends(get_db)):

    egreso_existente = db.query(Egreso).filter(Egreso.id == egreso_id).first()
    
    if not egreso_existente:
        raise HTTPException(status_code=404, detail="Egreso no encontrado")
    
    if datos.fecha is not None:
        egreso_existente.fecha = datos.fecha
    if datos.descripcion is not None:
        egreso_existente.descripcion = datos.descripcion
    if datos.monto is not None:
        egreso_existente.monto = datos.monto
    if datos.categoria is not None:
        egreso_existente.categoria = datos.categoria
        
    db.commit()
    db.refresh(egreso_existente)
    
    return egreso_existente

@router.delete("/{egreso_id}")
def eliminar_egreso(egreso_id: uuid.UUID, db: Session = Depends(get_db)):

    egreso_existente = db.query(Egreso).filter(Egreso.id == egreso_id).first()
    
    if not egreso_existente:
        raise HTTPException(status_code=404, detail="Egreso no encontrado")
    
    db.delete(egreso_existente)
    db.commit()
    
    return {"success": True, "message": "Egreso eliminado permanentemente"}