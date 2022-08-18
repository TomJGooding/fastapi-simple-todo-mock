from fastapi import Depends, FastAPI, HTTPException
from mongita import MongitaClientDisk
from pydantic import BaseModel

description = "The To-Do List API allows you to add, delete and update tasks"

app = FastAPI(title="To-Do List API", description=description)

db_client = MongitaClientDisk()
db = db_client.db


# Dependency
def get_todos_db():
    todos = db.todos
    return todos


print(type(get_todos_db()))


class ToDoItem(BaseModel):
    id: int
    title: str
    complete: bool


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/todos", response_model=list[ToDoItem])
async def get_all_todos(todos=Depends(get_todos_db)):
    all_todos = todos.find({})
    return [
        {key: todo_item[key] for key in todo_item if key != "_id"}
        for todo_item in all_todos
    ]


@app.get("/todos/{todo_id}", response_model=ToDoItem)
async def get_todo_item_by_id(todo_id: int, todos=Depends(get_todos_db)):
    if todos.count_documents({"id": todo_id}) < 1:
        raise HTTPException(
            status_code=404, detail=f"No to-do item with id {todo_id} found"
        )
    todo_item = todos.find_one({"id": todo_id})
    return {key: todo_item[key] for key in todo_item if key != "_id"}


@app.post("/todos", response_model=ToDoItem)
async def create_todo_item(new_todo: ToDoItem, todos=Depends(get_todos_db)):
    if todos.count_documents({"id": new_todo.id}) > 0:
        raise HTTPException(
            status_code=400,
            detail=f"To-do item with id {new_todo.id} already exists",
        )
    todos.insert_one(new_todo.dict())
    return new_todo


@app.put("/todos/{todo_id}", response_model=ToDoItem)
async def update_todo_item(
    todo_id: int, updated_todo: ToDoItem, todos=Depends(get_todos_db)
):
    if todos.count_documents({"id": todo_id}) < 1:
        raise HTTPException(
            status_code=404, detail=f"No to-do item with id {todo_id} found"
        )
    todos.replace_one({"id": todo_id}, updated_todo.dict())
    return updated_todo


@app.delete("/todos/{todo_id}")
async def delete_todo_item(todo_id: int, todos=Depends(get_todos_db)):
    delete_result = todos.delete_one({"id": todo_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=404, detail=f"No to-do item with id {todo_id} found"
        )
    return {"OK": True}
