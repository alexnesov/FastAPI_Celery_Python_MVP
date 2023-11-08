from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from celery import Celery
from celery.result import AsyncResult
import celeryconfig

app = FastAPI()

# Configure Celery
celery = Celery(
    'myapp',
    broker='redis://localhost:6379/0',
    include=['myapp.tasks']
)
celery.config_from_object(celeryconfig)

# Configure templates
templates = Jinja2Templates(directory="templates")


@app.post("/create_task/")
async def create_task(task_name: str = Form(...)):
    task = celery.send_task("myapp.tasks.process_task", args=[task_name])
    return {"task_id": task.id, "status": "Processing"}


@app.get("/")
async def read_root(request: Request):
    tasks = []
    for task_id in celery.control.inspect().active().keys():
        result = AsyncResult(task_id, app=celery)
        tasks.append({"task_id": task_id, "status": result.status})

    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
