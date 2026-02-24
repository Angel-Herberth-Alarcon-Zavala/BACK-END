from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
# Imports de routers y base de datos
from app.database import get_db
from app.models import Usuario

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

class LoginRequest(BaseModel):
    username: str
    password: str

# Inicio de sesión
@app.post("/login")
async def login(login_request : LoginRequest, db : Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.username == login_request.username,
        Usuario.password == login_request.password
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=400, 
            detail="Error en login, credenciales incorrectas")


    return {
        "msg" : "Acceso concedido"
    }


"""
@app.post("/login")
def login(user_req: LoginRequest):
    for user in USUARIOS:
        if user["email"] == user_req.email and user["password"] == user_req.password:
            return {
                "msg": True,
                "data": {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                    "role": user["role"],
                    "verified": user["verified"]
                }
            }
    raise HTTPException(
        status_code=401, 
        detail="Correo o contraseña incorrectos")
"""
