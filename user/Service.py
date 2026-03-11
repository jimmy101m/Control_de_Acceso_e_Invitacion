from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from entities.User import User
from .Models import (
    CrearUsuario,
    ActualizarUsuario,
    UsuarioResponse,
    ListaUsuariosResponse,
)
from database.database import DBDependency
from .Util import hash_password


async def crear_usuario(peticion: CrearUsuario, db: DBDependency) -> UsuarioResponse:
    nuevo_usuario = User(
        name=peticion.name,
        email=peticion.email,
        phone=peticion.phone,
        password=hash_password(peticion.password),
    )

    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)

    return nuevo_usuario


async def obtener_usuario_por_id(user_id: UUID, db: DBDependency) -> UsuarioResponse:
    result = await db.execute(select(User).where(User.id == user_id))
    usuario = result.scalar_one_or_none()

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    return usuario


async def listar_usuarios(
    db: DBDependency, skip: int = 0, limit: int = 100
) -> ListaUsuariosResponse:
    result = await db.execute(select(User).offset(skip).limit(limit))
    usuarios = result.scalars().all()

    result_total = await db.execute(select(User))
    total = len(result_total.scalars().all())

    return ListaUsuariosResponse(usuarios=usuarios, total=total)


async def actualizar_usuario(
    user_id: UUID, peticion: ActualizarUsuario, db: DBDependency
) -> UsuarioResponse:
    result = await db.execute(select(User).where(User.id == user_id))
    usuario = result.scalar_one_or_none()

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    if peticion.name is not None:
        usuario.name = peticion.name
    if peticion.email is not None:
        usuario.email = peticion.email
    if peticion.phone is not None:
        usuario.phone = peticion.phone

    await db.commit()
    await db.refresh(usuario)

    return usuario


async def eliminar_usuario(user_id: UUID, db: DBDependency) -> dict:
    result = await db.execute(select(User).where(User.id == user_id))
    usuario = result.scalar_one_or_none()

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    await db.delete(usuario)
    await db.commit()

    return {"message": "Usuario eliminado correctamente"}
