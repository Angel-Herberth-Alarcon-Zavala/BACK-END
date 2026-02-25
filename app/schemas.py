from uuid import UUID
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
class EgresoCreate(BaseModel):
    fecha: date
    descripcion: str
    monto: float
    categoria: str
    usuario_id: UUID   
class EgresoUpdate(BaseModel):
    fecha: date | None = None
    descripcion: str | None = None
    monto: float | None = None
    categoria: str | None = None

# Consulta individual o en lista de usuarios (usuarios)
class UsuarioCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"
    verified: bool = True

class UsuarioUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    role: str | None = None
    password: str | None = None
    verified: bool | None = None