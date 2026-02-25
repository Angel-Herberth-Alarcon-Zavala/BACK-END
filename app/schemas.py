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

# Creación de usuario (usuarios)
class UsuarioCreate(BaseModel):
    username: str
    email: str
    password: str

class UsuarioResponse(BaseModel):
    usuario_id: UUID 
    username: str
    email: str
    verified: bool
    class Config:
        from_attributes = True

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

class EgresoResponse(BaseModel):
    id: UUID 
    usuario_id: UUID 
    fecha: date
    descripcion: str
    monto: float
    categoria: str

    class Config:
        from_attributes = True