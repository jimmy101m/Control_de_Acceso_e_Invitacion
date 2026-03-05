from fastapi import APIRouter
from .Models import CrearUsuario, UsuarioResponse
from .Service import crear_usuario, DBDependency

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=201, response_model=UsuarioResponse)
async def crear_usuario_endpoint(peticion: CrearUsuario, db: DBDependency):
    return await crear_usuario(peticion, db)