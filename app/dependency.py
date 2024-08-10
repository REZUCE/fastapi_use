from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.accessor import database
from app.events.repository import EventRepository
from app.events.service import EventService


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with database.get_session() as session:
        yield session


async def get_event_repository(
        db_session: AsyncSession = Depends(get_db_session)
) -> EventRepository:
    return EventRepository(db_session=db_session)


async def get_event_service(
        event_repository: EventRepository = Depends(get_event_repository)
) -> EventService:
    return EventService(event_repository=event_repository)
