from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from celery.result import AsyncResult
from celery_worker.tasks import create_task

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/create_task/")
async def create_task_route(task_name: str = Form(...)):
    task = create_task.delay(task_name)
    return {"task_id": task.id}

@app.get("/get_task_status/{task_id}")
async def get_task_status(task_id: str):
    task = AsyncResult(task_id, app=create_task.app)
    return {"task_status": task.status, "result": task.result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
