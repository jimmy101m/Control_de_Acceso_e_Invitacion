from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, TYPE_CHECKING
from .Base import BaseClass
from .user_roles import user_roles_table

if TYPE_CHECKING:
    from .User import User


class Role(BaseClass):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column()

    users: Mapped[List["User"]] = relationship(
        secondary=user_roles_table,
        back_populates="roles",
    )