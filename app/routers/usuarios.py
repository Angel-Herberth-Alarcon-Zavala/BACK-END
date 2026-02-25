from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models import Usuario
from app.schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.correo_config import conf

# Herramientas para el envío de correos
from fastapi_mail import FastMail, MessageSchema, MessageType

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

    usuario_db = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    db.delete(usuario_db)
    db.commit()

    return {
        "success": True, 
        "message": "Usuario eliminado"
    }

@router.post("/register", response_model=UsuarioResponse)
async def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Verificación de existencia en Base de Datos real
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")

    # 2. Creación del objeto de base de datos
    nuevo_usuario = Usuario(
        username=usuario.username,
        email=usuario.email,
        password=usuario.password, 
        role="user",
        verified=False 
    )

    try:
        # Guardado persistente
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        # 3. Preparación y envío del correo electrónico
        link_verificacion = f"http://127.0.0.1:8000/usuarios/verificar?email={usuario.email}"

        cuerpo_html = f"""
        <div style="font-family: sans-serif; max-width: 600px; margin: auto; border: 1px solid #eee; padding: 20px;">
            <h2 style="color: #2563eb; text-align: center;">¡Bienvenido a FinanzApp!</h2>
            <p>Hola <strong>{usuario.username}</strong>,</p>
            <p>Gracias por registrarte. Para activar tu cuenta y empezar a gestionar tus egresos, por favor confirma tu identidad:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{link_verificacion}" 
                   style="background-color: #2563eb; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                   Verificar Mi Cuenta
                </a>
            </div>
            <p style="font-size: 0.8em; color: #666;">Si no creaste esta cuenta, puedes ignorar este correo con seguridad.</p>
        </div>
        """

        mensaje = MessageSchema(
            subject="Finaliza tu registro en FinanzApp",
            recipients=[usuario.email],
            body=cuerpo_html,
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(mensaje)

        return nuevo_usuario

    except Exception as e:
        db.rollback()
        print(f"Error durante el registro: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno al procesar el registro o enviar el correo.")


@router.get("/verificar")
async def verificar_usuario(email: str = Query(...), db: Session = Depends(get_db)):
    # Buscamos al usuario por el email que viene en la URL
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Solicitud de verificación inválida.")

    if usuario.verified:
        return RedirectResponse(url="http://localhost:5173/login?message=ya_verificado")

    # Actualizamos el estado en la base de datos
    usuario.verified = True
    db.commit()

    # Redirección automática al Login de React (puerto 5173)
    return RedirectResponse(url="http://localhost:5173/login?verified=true")
