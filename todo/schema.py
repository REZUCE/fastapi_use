from pydantic import BaseModel


# class Item(BaseModel):
#
#     status: str


class TodoItemSchema(BaseModel):
    item: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "item": "Example: Read the next chapter of the book"
                }
            ]
        }
    }


class TodoItemsSchema(BaseModel):
    todos: list[TodoItemSchema]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "todos": [
                        {"item": "Example schema 1!"},
                        {"item": "Example schema 2!"},
                        {"item": "Example schema 3!"}
                    ]
                }
            ]
        }
    }


class TodoSchema(BaseModel):
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
