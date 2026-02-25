from typing import List
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fastapi.responses import FileResponse
import os
from fastapi.responses import StreamingResponse
import csv
from io import StringIO
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

# Imports de routers y base de datos
from app.database import get_db
from app.models import Egreso
from app.schemas import EgresoCreate, EgresoUpdate, EgresoResponse

router = APIRouter(
    prefix="/egresos", 
    tags=["Egresos"])

@router.get("/{usuario_id}", response_model=List[EgresoResponse])
def obtener_egresos_usuario(usuario_id: uuid.UUID, db: Session = Depends(get_db)):
    lista_egresos = db.query(Egreso)\
                      .filter(Egreso.usuario_id == usuario_id)\
                      .order_by(Egreso.fecha.desc())\
                      .all()
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
#exportar csv
@router.get("/export/csv/{usuario_id}")
def exportar_egresos_csv(usuario_id: uuid.UUID, db: Session = Depends(get_db)):

    egresos = db.query(Egreso).filter(Egreso.usuario_id == usuario_id).all()

    if not egresos:
        raise HTTPException(status_code=404, detail="No hay egresos para exportar")

    output = StringIO()
    writer = csv.writer(output)

    # Cabeceras
    writer.writerow(["Fecha", "Descripcion", "Monto", "Categoria"])

    # Filas
    for e in egresos:
        writer.writerow([e.fecha, e.descripcion, e.monto, e.categoria])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=egresos.csv"}
    )

#exportar pdf
@router.get("/export/pdf/{usuario_id}")
def exportar_egresos_pdf(usuario_id: uuid.UUID, db: Session = Depends(get_db)):

    egresos = db.query(Egreso).filter(Egreso.usuario_id == usuario_id).all()

    if not egresos:
        raise HTTPException(status_code=404, detail="No hay egresos para exportar")

    filename = f"egresos_{usuario_id}.pdf"
    filepath = os.path.join(os.getcwd(), filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    y = 750

    c.drawString(100, y, "Reporte de Egresos")
    y -= 30

    for e in egresos:
        texto = f"{e.fecha} | {e.descripcion} | {e.monto} | {e.categoria}"
        c.drawString(50, y, texto)
        y -= 20
        if y < 50:
            c.showPage()
            y = 750

    c.save()

    return FileResponse(filepath, filename=filename)