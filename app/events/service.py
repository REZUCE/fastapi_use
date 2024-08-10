from dataclasses import dataclass
import logging
from app.events.schemas import EventCreateSchema, EventSchema, EventUpdateSchema
from app.events.repository import EventRepository

logger = logging.getLogger(__name__)


@dataclass
class EventService:
    event_repository: EventRepository

    async def create_event(self, body: EventCreateSchema) -> None:
        await self.event_repository.create_event(event_data=body)

    async def list_event(self) -> list[EventSchema]:
        events = await self.event_repository.list_events()
        events_schemas = [EventSchema.model_validate(event) for event in events]
        return events_schemas

    async def get_event(self, event_id: int) -> EventSchema:
        event = await self.event_repository.get_event(event_id=event_id)
        return EventSchema.model_validate(event)

    async def delete_event(self, event_id: int):
        await self.event_repository.delete_event(event_id=event_id)

    async def delete_all_events(self):
        await self.event_repository.delete_all_events()

    async def update_event(self, event_id: int, body: EventUpdateSchema) -> EventSchema:
        updated_event = await self.event_repository.update_event(event_id, update_data=body)
        return EventSchema.model_validate(updated_event)
