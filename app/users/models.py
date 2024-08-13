from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.infrastructure.database import Base
from app.infrastructure.models_relations import user_event_table  # Импортируем общую таблицу


class Users(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationship с событиями через промежуточную таблицу
    events: Mapped[list["Events"]] = relationship("Events", secondary=user_event_table, back_populates="users")

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, email={self.email!r})>"

    def __repr__(self) -> str:
        return self.__str__()
