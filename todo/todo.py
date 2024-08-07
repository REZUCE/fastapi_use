from fastapi import APIRouter, Path
from todo.schema import TodoSchema

todo_router = APIRouter()

todo_list = []


@todo_router.post("/todo")
async def add_todo(todo: TodoSchema) -> dict:
    todo_list.append(todo)
    return {"message": "Todo added successfully"}


@todo_router.get("/todo")
async def retrieve_todos() -> dict:
    return {"todo": todo_list}


"""
Здесь добавлен параметр пути. Path помогает отличать параметры пути от других аргументов
присутствующих в функции маршрута.

Класс Path принимает первый позиционный аргумент, равный None или
многоточие (...). Если в качестве первого аргумента задано многоточие (...),
параметр пути становится обязательным. Класс Path также содержит
аргументы, используемые для числовой проверки, если параметр пути
является числом. Определения включают gt и le – gt означает больше, а le
означает меньше. При использовании маршрут будет проверять параметр пути
на соответствие этим аргументам.

Параметр запроса — это необязательный параметр, который обычно появляется
после вопросительного знака в URL-адресе. Он используется для фильтрации
запросов и возврата определенных данных на основе предоставленных запросов.
В функции обработчика маршрута аргумент, не совпадающий с параметром пути,
является запросом. Вы также можете определить запрос, создав экземпляр класса
FastAPI Query() в аргументе функции, например:
async query_route(query: str = Query(None):
    return query

"""
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
