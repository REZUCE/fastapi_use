from fastapi import APIRouter, Path
from todo.schema import TodoPostSchema, TodoItemUpdateSchema

todo_router = APIRouter(tags=["Todo CRUD"])

todo_list = []


@todo_router.post("/todo")
async def add_todo(todo: TodoPostSchema) -> dict:
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


@todo_router.put("/todo/{todo_id}")
async def update_todo(
        todo_data: TodoItemUpdateSchema,
        todo_id: int = Path(..., description="The ID of the todo to be updated")
) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
        return {
            "message": "Todo updated successfully."
        }
    return {
        "message": "Todo with supplied ID doesn't exist."
    }


@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(todo_id: int) -> dict:
    for index in range(len(todo_list)):
        # Здесь range, потому что по индексу удаляем.
        todo = todo_list[index]
        if todo.id == todo_id:
            todo_list.pop(index)
            return {
                "message": "Todo deleted successfully."
            }
    return {
        "message": "Todo with supplied ID doesn't exist."
    }


@todo_router.delete("/todo")
async def delete_all_todo() -> dict:
    todo_list.clear()
    return {
        "message": "Todos deleted successfully."
    }
