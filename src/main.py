from fastapi import FastAPI
from worker import create_task


app = FastAPI()


@app.get("/")
def hello():
    return {"Hello": "World"}


@app.post("/tasks", status_code=201)
def run_task():
    task = create_task.delay()
    return {"task_id": task.id}
