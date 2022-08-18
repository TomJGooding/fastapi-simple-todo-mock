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


class Task(BaseModel):
    id: int
    title: str
    complete: bool


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/todos", response_model=list[Task])
async def get_all_todos(todos=Depends(get_todos_db)):
    all_todos = todos.find({})
    return [{key: task[key] for key in task if key != "_id"} for task in all_todos]


@app.get("/todos/{task_id}", response_model=Task)
async def get_task_by_id(task_id: int, todos=Depends(get_todos_db)):
    if todos.count_documents({"id": task_id}) < 1:
        raise HTTPException(status_code=404, detail=f"No task with id {task_id} found")
    task = todos.find_one({"id": task_id})
    return {key: task[key] for key in task if key != "_id"}


@app.post("/todos", response_model=Task)
async def create_task(new_task: Task, todos=Depends(get_todos_db)):
    if todos.count_documents({"id": new_task.id}) > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Task with id {new_task.id} already exists",
        )
    todos.insert_one(new_task.dict())
    return new_task


@app.put("/todos/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task, todos=Depends(get_todos_db)):
    if todos.count_documents({"id": task_id}) < 1:
        raise HTTPException(status_code=404, detail=f"No task with id {task_id} found")
    todos.replace_one({"id": task_id}, updated_task.dict())
    return updated_task


@app.delete("/todos/{task_id}")
async def delete_task(task_id: int, todos=Depends(get_todos_db)):
    delete_result = todos.delete_one({"id": task_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"No task with id {task_id} found")
    return {"OK": True}
