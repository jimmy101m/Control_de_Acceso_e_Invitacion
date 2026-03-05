from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import ForeignKey
from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING
from entities.Base import BaseClass

if TYPE_CHECKING:
    from entities.User import User


class Invitacion(BaseClass):
    __tablename__ = "Invitaciones"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)

    expired_at: Mapped[datetime] = mapped_column(index=True)
    token: Mapped[str] = mapped_column(unique=True, index=True)
    used: Mapped[bool] = mapped_column(default=False)

    invitado_por: Mapped["User"] = relationship(
        back_populates="invitaciones",
    )


