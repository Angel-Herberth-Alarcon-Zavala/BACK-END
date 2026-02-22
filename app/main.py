from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from .routers import resetPassword
from app.database import USUARIOS, CODIGOS_RECUPERACION

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    #allow_credentials=True
)


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

app.include_router(resetPassword.router)