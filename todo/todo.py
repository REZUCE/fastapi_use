from fastapi import APIRouter, Path, HTTPException, status, Depends, Request
# from starlette.templating import _TemplateResponse

from todo.schema import TodoSchema, TodoItemSchema, TodoItemsSchema
from fastapi.templating import Jinja2Templates

todo_router = APIRouter(tags=["Todo CRUD"])

todo_list = []

templates = Jinja2Templates(directory="templates/")


### По умолчанию 200 статус код!!!

@todo_router.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(request: Request, todo: TodoSchema = Depends(TodoSchema.as_form)):
    todo.id = len(todo_list) + 1  # Якобы сами генерируем index.
    todo_list.append(todo)
    return templates.TemplateResponse(
        "todo.html", context=
        {
            "request": request,
            "todos": todo_list
        })


@todo_router.get("/todo", response_model=TodoItemsSchema)
async def retrieve_todos(request: Request):
    return templates.TemplateResponse(
        "todo.html", context=
        {
            "request": request,
            "todos": todo_list
        })


@todo_router.get("/todo/{todo_id}")
async def get_single_todo(
        request: Request,
        todo_id: int = Path(..., description="The ID of the todo to retrieve.")
):
    for todo in todo_list:
        if todo.id == todo_id:
            return templates.TemplateResponse(
                "todo.html", context=
                {
                    "request": request,
                    "todo": todo
                })
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied ID doesn't exist",
    )


@todo_router.put("/todo/{todo_id}")
async def update_todo(
        todo_data: TodoItemSchema,
        todo_id: int = Path(..., description="The ID of the todo to be updated")
) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
        return {
            "message": "Todo updated successfully."
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied ID doesn't exist",
    )


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
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied ID doesn't exist",
    )


@todo_router.delete("/todo")
async def delete_all_todo() -> dict:
    todo_list.clear()
    return {
        "message": "Todos deleted successfully."
    }
