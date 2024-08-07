from fastapi import APIRouter, Path
from todo.schema import TodoSchema

todo_router = APIRouter()

todo_list = []


@todo_router.post("/todo")
async def add_todo(todo: TodoSchema) -> dict:
    # Важно помнить, что есть еще класс Body.
    todo_list.append(todo)
    return {"message": "Todo added successfully"}


@todo_router.get("/todo")
async def retrieve_todos() -> dict:
    return {"todo": todo_list}


@todo_router.get("/todo/{todo_id}")
async def get_single_todo(todo_id: int = Path(..., description="The ID of the todo to retrieve.")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "todo": todo
            }
    return {
        "message": "Todo with supplied ID doesn't exist."
    }
