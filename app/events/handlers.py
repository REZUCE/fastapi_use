from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status, Depends

from app.core.exception import EventNotFoundException, EventsNotFoundTableException, EventNotUpdateException
from app.dependency import get_event_service
from app.events.schemas import EventSchema, EventCreateSchema, EventUpdateSchema
from app.events.service import EventService

event_router = APIRouter(
    tags=["Event"],
)


@event_router.put("/{event_id}", response_model=EventSchema)
async def update_event(
        event_service: Annotated[EventService, Depends(get_event_service)],
        event_id: int,
        body: EventUpdateSchema = Body(...),
) -> EventSchema:
    try:
        return await event_service.update_event(event_id=event_id, body=body)
    except EventNotFoundException as e:
        # Todo: потестить вызов.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e
        )
    except EventNotUpdateException as e:
        # Todo: потестить вызов.
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e
        )


@event_router.get(
    '/{event_id}',
    response_model=EventSchema
)
async def retrieve_event_by_id(
        event_id: int,
        event_service: Annotated[EventService, Depends(get_event_service)]
):
    try:
        return await event_service.get_event(event_id=event_id)
    except EventNotFoundException as e:
        # Todo: потестить вызов.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e
        )
        # raise HTTPException(
        #     status_code=status.HTTP_404_NOT_FOUND,
        #     detail=e.detail
        # )


@event_router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
async def create_event(
        event_service: Annotated[EventService, Depends(get_event_service)],
        body: EventCreateSchema = Body(...)
) -> dict:
    await event_service.create_event(body=body)
    return {
        "message": "Event created successfully"
    }


@event_router.delete("/{event_id}")
async def delete_event(
        event_service: Annotated[EventService, Depends(get_event_service)],
        event_id: int
) -> dict:
    try:
        await event_service.delete_event(event_id=event_id)
        return {
            "message": "Event deleted successfully"
        }
    except EventNotFoundException as e:
        # Todo: потестить вызов.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e
        )


@event_router.get("/", response_model=list[EventSchema])
async def retrieve_all_events(
        event_service: Annotated[EventService, Depends(get_event_service)]
) -> list[EventSchema]:
    try:
        return await event_service.list_event()
    except EventsNotFoundTableException as e:
        # Todo: потестить вызов.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e
        )


@event_router.delete("/delete_all")
async def delete_all_events(
        event_service: Annotated[EventService, Depends(get_event_service)]
) -> dict:
    try:
        await event_service.delete_all_events()
        return {
            "message": "All events deleted successfully"
        }
    except EventsNotFoundTableException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e
        )
