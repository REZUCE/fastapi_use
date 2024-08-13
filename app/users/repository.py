import logging
from dataclasses import dataclass
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, insert
from fastapi import HTTPException, status
from app.core.exception import UserAlreadyExistsException
from app.infrastructure.accessor import Database
from app.users.models import Users
from app.users.schemas import UserCreateSchema

logger = logging.getLogger(__name__)


@dataclass
class UserRepository:
    db_session_cm: Database  # Используем тип Database

    async def create_user(self, user_data: UserCreateSchema) -> None:
        query = insert(Users).values(
            **user_data.dict(exclude_none=True)
        )
        existing_user_query = select(Users).where(Users.email == user_data.email)

        async with self.db_session_cm.get_session() as session:
            try:
                existing_user = (await session.execute(existing_user_query)).scalars().one_or_none()
                if existing_user:
                    raise UserAlreadyExistsException
                await session.execute(query)
                # commit не нужен, так как контекстный менеджер делает это автоматически
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"An error occurred while creating the user: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error occurred: {str(e)}"
                )
