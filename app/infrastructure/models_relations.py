from sqlalchemy import Table, ForeignKey, Column
from app.infrastructure.database import Base

# Таблица для связи many-to-many
user_event_table = Table(
    "user_event",
    Base.metadata,
    # Важно понимать, что здесь будет составной индекс (composite index).
    # который будет содержать два поля: user_id и event_id.
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("event_id", ForeignKey("events.id"), primary_key=True)
)
