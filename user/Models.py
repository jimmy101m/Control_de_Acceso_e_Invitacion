from pydantic import BaseModel, EmailStr
from uuid import UUID

class CrearUsuario(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str

class UsuarioResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    phone: str

    class Config:
        from_attributes = True