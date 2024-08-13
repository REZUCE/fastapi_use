from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON
from app.infrastructure.database import Base
from app.infrastructure.models_relations import user_event_table  # Импортируем общую таблицу


class Events(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(125), nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationship с пользователями через промежуточную таблицу
    users: Mapped[list["Users"]] = relationship("Users", secondary=user_event_table, back_populates="events")

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, title={self.title!r}, description={self.description[:20]!r}, location={self.location[:20]!r})>"

    def __repr__(self) -> str:
        return self.__str__()
