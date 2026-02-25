from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse



# Imports de routers y base de datos
from .routers import resetPassword, egresos, usuarios
from app.schemas import LoginRequest
from app.models import Usuario
from app.database import get_db

# Aplicación FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    #allow_credentials=True
)
@app.get("/")
def root():
    return RedirectResponse(url="/docs")

# Inicio de sesión
@app.post("/login")
def login(user_req: LoginRequest, db: Session = Depends(get_db)):
    usuario_encontrado = db.query(Usuario).filter(Usuario.email == user_req.email).first()
    
    if not usuario_encontrado or usuario_encontrado.password != user_req.password:
        raise HTTPException(status_code=404, detail="Correo o contraseña incorrectos.")
    
    return {
        "success": True,
        "message": "Login exitoso",
        "user": {
            "id": usuario_encontrado.id, 
            "username": usuario_encontrado.username,
            "email": usuario_encontrado.email,
            "role": usuario_encontrado.role,
            "verified": usuario_encontrado.verified
        }
    }
    
app.include_router(resetPassword.router)
app.include_router(egresos.router)
app.include_router(usuarios.router)