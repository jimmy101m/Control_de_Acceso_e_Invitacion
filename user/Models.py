from pydantic import BaseModel, EmailStr
from uuid import UUID


class CrearUsuario(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str


class ActualizarUsuario(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None


class UsuarioResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    phone: str

    class Config:
        from_attributes = True


class ListaUsuariosResponse(BaseModel):
    usuarios: list[UsuarioResponse]
    total: int
