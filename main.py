from fastapi import FastAPI, HTTPException, Depends
from mongita import MongitaClientDisk
from pydantic import BaseModel

app = FastAPI()

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


@app.post("/todos", response_model=ToDoItem)
async def create_todo_item(new_todo: ToDoItem, todos=Depends(get_todos_db)):
    if todos.count_documents({"id": new_todo.id}) > 0:
        raise HTTPException(
            status_code=400,
            detail=f"To-do item with id {new_todo.id} already exists",
        )
    todos.insert_one(new_todo.dict())
    return new_todo
