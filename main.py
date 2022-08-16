from fastapi import FastAPI
from mongita import MongitaClientDisk

client = MongitaClientDisk()
db = client.db
todos = db.todos

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
