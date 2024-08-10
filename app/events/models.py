from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON
from app.infrastructure.database import Base


class Events(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, unique=True)

    title: Mapped[str] = mapped_column(String(125), nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, candidate_name={self.title!r}, file_path={self.description[:20]!r}, rating={self.location[:20]!r})>"

    def __repr__(self) -> str:
        return self.__str__()
