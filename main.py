from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    title: str
    description: str
    status: bool = False


tasks_db = []
task_id_counter = 1


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if task:
        return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    global task_id_counter
    new_task = task.model_dump()
    new_task["id"] = task_id_counter
    task_id_counter += 1
    tasks_db.append(new_task)
    return new_task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    task_index = next((index for index, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if task_index is not None:
        tasks_db[task_index] = {"id": task_id, **updated_task.model_dump()}
        return tasks_db[task_index]
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if task:
        tasks_db.remove(task)
        return task
    raise HTTPException(status_code=404, detail="Task not found")
