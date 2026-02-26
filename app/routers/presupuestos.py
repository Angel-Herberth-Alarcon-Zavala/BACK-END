from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, models
from ..database import get_db

router = APIRouter(
    prefix="/presupuestos", 
    tags=["Presupuestos"])

@router.post("/", response_model=schemas.PresupuestoOut)
def guardar_presupuesto(presu: schemas.PresupuestoCreate, db: Session = Depends(get_db)):
    presupuesto_db = db.query(models.Presupuesto).filter(
        models.Presupuesto.usuario_id == presu.usuario_id,
        models.Presupuesto.categoria == presu.categoria
    ).first()

    if presupuesto_db:
        presupuesto_db.monto_limite = presu.monto_limite
    else:
        presupuesto_db = models.Presupuesto(
            usuario_id=presu.usuario_id,
            categoria=presu.categoria,
            monto_limite=presu.monto_limite
        )
        db.add(presupuesto_db)
    
    db.commit()
    db.refresh(presupuesto_db)
    return presupuesto_db

@router.get("/{usuario_id}")
def obtener_presupuestos(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(models.Presupuesto).filter(models.Presupuesto.usuario_id == usuario_id).all()