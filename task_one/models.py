from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str]
    content: Mapped[str] = mapped_column(nullable=False)
    completed: Mapped[bool] = mapped_column(default=False)
    date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
