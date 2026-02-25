from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models import Usuario
from app.schemas import UsuarioCreate, UsuarioUpdate

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"])

@router.get("/")
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.post("/")
def crear_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):

    if db.query(Usuario).filter(Usuario.email == datos.email).first():
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )
    
    nuevo_usuario = Usuario(
        username=datos.username,
        email=datos.email,
        password=datos.password,
        role=datos.role,
        verified=datos.verified
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario

@router.put("/{usuario_id}")
def editar_usuario(usuario_id: uuid.UUID, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
        
    if datos.username is not None: usuario_db.username = datos.username
    if datos.email is not None: usuario_db.email = datos.email
    if datos.role is not None: usuario_db.role = datos.role
    if datos.password is not None: usuario_db.password = datos.password
    if datos.verified is not None: usuario_db.verified = datos.verified
        
    db.commit()
    db.refresh(usuario_db)

    return usuario_db

@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: uuid.UUID, db: Session = Depends(get_db)):

    usuario_db = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    db.delete(usuario_db)
    db.commit()

    return {
        "success": True, 
        "message": "Usuario eliminado"
    }