from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.database.base import Base


class APIKey(Base):
    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    key_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )