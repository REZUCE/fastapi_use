import json
from dataclasses import dataclass
import logging
from app.events.schemas import EventCreateSchema, EventSchema, EventUpdateSchema
from app.users.repository import UserRepository
from app.users.schemas import UserCreateSchema

logger = logging.getLogger(__name__)


@dataclass
class UserService:
    user_repository: UserRepository

    async def create_user(self, body: UserCreateSchema) -> None:
        await self.user_repository.create_user(user_data=body)
