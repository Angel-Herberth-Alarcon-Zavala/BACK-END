from pydantic import BaseModel
from datetime import date

# Login (main)
class LoginRequest(BaseModel):
    username: str
    password: str

# Confirmación para cambio de contraseña (resetPassword)
class EmailRequest(BaseModel):
    email: str
class codeRequest(BaseModel):
    email: str
    code: str
class ResetPasswordRequest(BaseModel):
    email: str
    nuevo_password: str

# Consulta individual o en lista de egresos (egresos)
class EgresoCreate(BaseModel):
    fecha: date
    descripcion: str
    monto: float
    categoria: str
class EgresoUpdate(BaseModel):
    fecha: date | None = None
    descripcion: str | None = None
    monto: float | None = None
    categoria: str | None = None