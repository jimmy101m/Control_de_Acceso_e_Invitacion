from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Boolean
from uuid import uuid4, UUID
from datetime import datetime


class Base(DeclarativeBase):
    pass


class BaseClass(Base):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
