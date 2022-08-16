from fastapi import FastAPI
from mongita import MongitaClientDisk
from pydantic import BaseModel

client = MongitaClientDisk()
db = client.db
todos = db.todos

app = FastAPI()


class ToDoItem(BaseModel):
    id: int
    title: str
    complete: bool


@app.get("/")
async def root():
    return {"message": "Hello World"}
