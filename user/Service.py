from entities.User import User
from .Models import CrearUsuario
from database.database import DBDependency
from .Util import hash_password


async def crear_usuario(peticion: CrearUsuario, db: DBDependency):

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