from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

# Imports de routers y base de datos
from .routers import resetPassword, egresos
from app.schemas import LoginRequest
from app.database import get_db, USUARIOS

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

app.include_router(resetPassword.router)
app.include_router(egresos.router)