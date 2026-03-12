from uuid import UUID
from fastapi import APIRouter, Depends, Query
from .Models import (
    CrearUsuario,
    ActualizarUsuario,
    UsuarioResponse,
    ListaUsuariosResponse,
)
from .Service import (
    crear_usuario,
    obtener_usuario_por_id,
    listar_usuarios,
    actualizar_usuario,
    eliminar_usuario,
    DBDependency,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=201, response_model=UsuarioResponse)
async def crear_usuario_endpoint(peticion: CrearUsuario, db: DBDependency):
    return await crear_usuario(peticion, db)


@router.get("/", response_model=ListaUsuariosResponse)
async def listar_usuarios_endpoint(
    db: DBDependency,
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Límite de registros"),
):
    return await listar_usuarios(db=db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UsuarioResponse)
async def obtener_usuario_endpoint(user_id: UUID, db: DBDependency):
    return await obtener_usuario_por_id(user_id, db)


@router.patch("/{user_id}", response_model=UsuarioResponse)
async def actualizar_usuario_endpoint(
    user_id: UUID,
    peticion: ActualizarUsuario,
    db: DBDependency,
):
    return await actualizar_usuario(user_id, peticion, db)


@router.delete("/{user_id}", status_code=204)
async def eliminar_usuario_endpoint(user_id: UUID, db: DBDependency):
    return await eliminar_usuario(user_id, db)
