from celery_worker.celery import app

@app.task
def create_task(task_name):
    # Simulate some task execution here
    result = f"Task '{task_name}' completed successfully"
    return result
