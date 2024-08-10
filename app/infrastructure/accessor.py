from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from app.core.settings import settings
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class Database:
    def __init__(self, url: str, ro_url: str) -> None:
        self._async_engine = create_async_engine(
            url=url,
            pool_pre_ping=True,  # Помогает избежать таймаут.
            # echo=settings.ECHO_SQL,
            isolation_level="READ COMMITTED"
        )
        # Сессия подразумевает старт транзакции. Как минимум три запросы, если вы открыли и закрыли сессию.
        self._async_session = async_sessionmaker(
            bind=self._async_engine,
            # Отключение expire_on_commit убирает дополнительные запросы к базе данных после коммита, оставляя данные
            # в памяти без проверки их актуальности. Это означает, что после коммита SQLAlchemy не будет автоматически
            # проверять, изменились ли данные в базе данных, и будет использовать те данные, которые уже находятся в
            # памяти.
            expire_on_commit=False
        )
        # READ
        self._read_only_async_engine = create_async_engine(
            url=ro_url,
            pool_pre_ping=True,
            # echo=settings.ECHO_SQL,
            isolation_level="AUTOCOMMIT"
        )
        self._read_only_async_session = async_sessionmaker(
            bind=self._read_only_async_engine,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
        """
        Создание контекстного менеджера без необходимости создавать класс
        или отдельные методы __aenter__() и __aexit__().
        """
        session: AsyncSession = self._async_session()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.commit()
            await session.close()

    @asynccontextmanager
    async def get_read_only_session(self) -> AsyncGenerator[AsyncSession, Any]:
        """
        Создание контекстного менеджера без необходимости создавать класс
        или отдельные методы __aenter__() и __aexit__().
        """
        session: AsyncSession = self._read_only_async_session()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.commit()
            await session.close()


database = Database(settings.DATABASE_URL, settings.DATABASE_URL)
