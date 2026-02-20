from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.responses import RedirectResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

USUARIOS = [
    {"id": 1, 
     "email": "admin@finanzapp.com", 
     "password": "123", 
     "role": "admin", 
     "username": "Administrador General",
     "verified": True},
    {"id": 2, 
     "email": "correo@gmail.com", 
     "password": "abc", 
     "role": "user", 
     "username": "Usuario Prueba",
     "verified": False}
]

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

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