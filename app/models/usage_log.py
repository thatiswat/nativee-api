from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class UsageLog(Base):

    __tablename__ = "usage_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    api_key_id: Mapped[int] = mapped_column(
        ForeignKey("api_keys.id")
    )

    endpoint: Mapped[str] = mapped_column(
        String(100)
    )

    provider: Mapped[str] = mapped_column(
        String(50)
    )

    latency_ms: Mapped[float] = mapped_column(
        Float
    )

    success: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )