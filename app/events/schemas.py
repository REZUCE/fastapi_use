from pydantic import BaseModel, ConfigDict


class EventSchema(BaseModel):
    id: int
    title: str
    image: str
    description: str
    tags: list[str]
    location: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "title": "Презентация книги по FastAPI",
                    "image": "https://linktomyimage.com/image.png",
                    "description": "На этом мероприятии мы будем обсуждать содержимое книги по FastAPI. Обязательно возьмите с собой свою копию, чтобы выиграть призы!",
                    "tags": ["python", "fastapi", "книга", "презентация"],
                    "location": "Google Meet"
                }
            ]
        }
    )


class EventCreateSchema(BaseModel):
    title: str
    image: str
    description: str
    tags: list[str]
    location: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "FastAPI Book Launch",
                    "image": "https://linktomyimage.com/image.png",
                    "description": "We will be discussing the contents of the FastAPI book in this event.Ensure to come with your own copy to win gifts!",
                    "tags": ["python", "fastapi", "book", "launch"],
                    "location": "Google Meet"
                }
            ]
        }
    }


class EventUpdateSchema(BaseModel):
    title: str | None = None
    image: str | None = None
    description: str | None = None
    tags: list[str] | None = None
    location: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "FastAPI Book Launch",
                    "image": "https://linktomyimage.com/image.png",
                    "description": "We will be discussing the contents of the FastAPI book in this event.Ensure to come with your own copy to win gifts!",
                    "tags": ["python", "fastapi", "book", "launch"],
                    "location": "Google Meet"
                }
            ]
        }
    }
