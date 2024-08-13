from sqlalchemy.orm import mapped_column
from sqlalchemy import Table, ForeignKey
from app.infrastructure.database import Base

# Таблица для связи many-to-many
user_event_table = Table(
    "user_event",
    Base.metadata,
    # Важно понимать, что здесь будет составной индекс (composite index).
    # который будет содержать два поля: user_id и event_id.
    mapped_column("user_id", ForeignKey("users.id"), primary_key=True),
    mapped_column("event_id", ForeignKey("events.id"), primary_key=True)
)
