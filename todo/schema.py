from pydantic import BaseModel


# class Item(BaseModel):
#
#     status: str


class TodoItemUpdateSchema(BaseModel):
    item: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "item": "Example: Read the next chapter of the book"
                }
            ]
        }}


class TodoPostSchema(BaseModel):
    id: int
    item: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "item": "Example schema!"
                }
            ]
        }}
