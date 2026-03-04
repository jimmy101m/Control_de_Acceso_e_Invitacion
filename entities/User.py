from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column
from fraccionamiento.database.database import Base
from datetime import datetime

class BaseClass(Base):
    __abstract__ = True
    id: Mapped[uuid4] = mapped_column(primary_key=True, index=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(), onupdate=datetime.now())
    status: Mapped[bool] = mapped_column(default=True)

class User(BaseClass):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()