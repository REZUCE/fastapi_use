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
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "item": "Example schema!"
                }
            ]
        }}
