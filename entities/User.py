from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING
from .Base import BaseClass
from .user_roles import user_roles_table

if TYPE_CHECKING:
    from .Role import Role
    from .invitacion import Invitacion


class User(BaseClass):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    phone: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column()

    roles: Mapped[List["Role"]] = relationship(
        secondary=user_roles_table,
        back_populates="users",
    )

    invitaciones: Mapped[List["Invitacion"]] = relationship(
        back_populates="invitado_por",
    )
