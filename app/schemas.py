from pydantic import BaseModel
from datetime import date

# Login (main)
class LoginRequest(BaseModel):
    email: str
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
class EgresoUpdate(BaseModel):
    fecha: date | None = None
    descripcion: str | None = None
    monto: float | None = None
    categoria: str | None = None