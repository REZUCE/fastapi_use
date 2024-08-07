from fastapi import APIRouter
from todo.schema import TodoSchema

todo_router = APIRouter()

todo_list = []


@todo_router.post("/todo")
async def add_todo(todo: TodoSchema) -> dict:
    # Если засунуть объект todo в список, то получится словарь, потому что у объекта есть
    # ключ и значение если его принтануть или сделать так todo.id.
    print(todo)
    print(todo.id)
    todo_list.append(todo)
    return {"message": "Todo added successfully"}


@todo_router.get("/todo")
async def retrieve_todos() -> dict:
    return {"todo": todo_list}
