import logging
from dataclasses import dataclass

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete, insert, update
from app.core.exception import EventNotFoundException, EventsNotFoundTableException, EventNotUpdateException
from app.events.models import Events
from app.events.schemas import EventCreateSchema, EventUpdateSchema
from app.infrastructure.accessor import Database

logger = logging.getLogger(__name__)


@dataclass
class EventRepository:
    db_session_cm: Database  # Используем тип Database

    async def create_event(self, event_data: EventCreateSchema) -> None:
        query = insert(Events).values(
            **event_data.dict(exclude_none=True)  # Убирает поля, где будет None.
        )
        async with self.db_session_cm.get_session() as session:
            try:
                await session.execute(query)
                # Необязательно, так как контекстный менеджер делает это автоматически.
                # Уберу позже, если будет ошибка.
                # await session.commit()
            except SQLAlchemyError as e:
                logger.error(f"An error occurred while creating the event: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error occurred: {str(e)}"
                )

    async def list_events(self) -> list[Events]:
        query = select(Events)
        async with self.db_session_cm.get_session() as session:
            try:
                result = (await session.execute(query)).scalars().all()
                if not result:
                    raise EventsNotFoundTableException
                return result
            except SQLAlchemyError as e:
                logger.error(f"An error occurred while listing events: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error occurred: {str(e)}"
                )

    async def get_event(self, event_id: int) -> Events:
        query = select(Events).where(Events.id == event_id)
        async with self.db_session_cm.get_session() as session:
            try:
                result = (await session.execute(query)).scalar_one_or_none()
                if not result:
                    raise EventNotFoundException
                return result
            except SQLAlchemyError as e:
                logger.error(f"An error occurred while getting the event: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error occurred: {str(e)}"
                )

    async def delete_event(self, event_id: int) -> None:
        query = delete(Events).where(Events.id == event_id)
        async with self.db_session_cm.get_session() as session:
            try:
                result = await session.execute(query)
                # Необязательно, так как контекстный менеджер делает это автоматически.
                # Уберу позже, если будет ошибка.
                # await session.commit()
                if result.rowcount == 0:
                    raise EventNotFoundException
            except SQLAlchemyError as e:
                logger.error(f"An error occurred while deleting the event: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error occurred: {str(e)}"
                )

    async def delete_all_events(self) -> None:
        query = delete(Events)
        async with self.db_session_cm.get_session() as session:
            try:
                result = await session.execute(query)
                # Необязательно, так как контекстный менеджер делает это автоматически.
                # Уберу позже, если будет ошибка.
                # await session.commit()
                if result.rowcount == 0:
                    raise EventsNotFoundTableException
            except SQLAlchemyError as e:
                logger.error(f"An error occurred while deleting all events: {e}")
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error occurred: {str(e)}"
                )

    async def update_event(self, event_id: int, update_data: EventUpdateSchema) -> Events:
        # Todo: Думаю можно сделать одним запросом.
        query = select(Events).where(Events.id == event_id)
        update_query = (
            update(Events)
            .where(Events.id == event_id)
            .values(**update_data.dict(exclude_none=True))
            .returning(Events)
        )
        async with self.db_session_cm.get_session() as session:
            try:
                result = await session.execute(query)
                event_to_update = result.scalar_one_or_none()
                if not event_to_update:
                    raise EventNotFoundException
                result = await session.execute(update_query)
                # Необязательно, так как контекстный менеджер делает это автоматически.
                # Уберу позже, если будет ошибка.
                # await session.commit()
                updated_event = result.scalar_one_or_none()
                if not updated_event:
                    raise EventNotUpdateException
                return updated_event
            except SQLAlchemyError as e:
                logging.error(f"An error occurred while updating the event: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error occurred: {str(e)}"
                )
