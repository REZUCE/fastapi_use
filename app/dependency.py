from fastapi import Depends
from app.infrastructure.accessor import Database
from app.core.settings import settings
from app.events.repository import EventRepository
from app.events.service import EventService
from app.users.repository import UserRepository
from app.users.service import UserService

# Создание глобального экземпляра Database
database = Database(settings.DATABASE_URL, settings.DATABASE_URL)


def get_database() -> Database:
    return database


async def get_event_repository(
        db: Database = Depends(get_database)
) -> EventRepository:
    return EventRepository(db_session_cm=db)


async def get_event_service(
        event_repository: EventRepository = Depends(get_event_repository)
) -> EventService:
    return EventService(event_repository=event_repository)


async def get_user_repository(
        db: Database = Depends(get_database)
) -> UserRepository:
    return UserRepository(db_session_cm=db)


async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repository=user_repository)
