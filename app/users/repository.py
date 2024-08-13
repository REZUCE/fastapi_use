import logging
from dataclasses import dataclass

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import UserAlreadyExistsException
from app.users.models import Users
from app.users.schemas import UserCreateSchema

logger = logging.getLogger(__name__)


@dataclass
class UserRepository:
    db_session: AsyncSession

    async def find_one_or_none(self, email: str):
        query = select(Users).where(Users.email == email)
        async with self.db_session as session:
            try:
                result = await session.execute(query)
                user = result.scalars().one_or_none()
                if user:
                    raise UserAlreadyExistsException
            except SQLAlchemyError as e:
                logger.error(f"An error occurred while creating the resume: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error occurred: {str(e)}"
                )

    async def create_user(self, user_data: UserCreateSchema) -> None:
        query = insert(Users).values(
            **user_data.dict(exclude_none=True)  # Убирает поля, где будет None.
        ).returning(Users.id)
        existing_user_query = select(Users).where(Users.email == user_data.email)
        async with self.db_session as session:
            try:
                existing_user = (await session.execute(existing_user_query)).scalars().one_or_none()
                if existing_user:
                    raise UserAlreadyExistsException
                # Todo: Проверить, может тут scalar() нужно.
                # result = await session.execute(query)
                await session.execute(query)
                await session.commit()  # Todo: Как я понимаю можно в целом это не писать.
                # return result.scalars().one()
            except SQLAlchemyError as e:
                logger.error(f"An error occurred while creating the resume: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Database error occurred: {str(e)}"
                )
