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
