from pydantic import BaseModel


# class Item(BaseModel):
#
#     status: str


class TodoSchema(BaseModel):
    """
    {
        "id": 1,
        "item": {
            "item": "Nested models",
            "Status": "completed"
        }
    }
    """
    id: int
    item: str

    # Можно добавить вот такой пример request body.
    class Config:
        Schema_extra = {
            "Example": {
                "id": 1,
                "item": "Example schema!"
            }
        }
