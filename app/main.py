import logging
import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from worker import celery_app
from celery.result import AsyncResult

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class Combo(BaseModel):
    email: str
    password: str
    source: str


app = FastAPI()


@app.get("/")
def home():
    return {"ping": "pong!!"}


@app.post("/send_combos")
async def send_combos(combo: Combo):
    logger.info(f"starting o365 check task: {combo.email}:{combo.password}")
    task_name = "o365.task"
    task = celery_app.send_task(task_name, args=[combo.email, combo.password])
    return JSONResponse({"task_id": task.id})


@app.get("/status/{task_id}")
async def task_status(task_id: str):
    task = AsyncResult(task_id)
    if task.state == "SUCCESS":
        return {"status": "done", "result": task.result}
    elif task.state == "PENDING":
        return {"status": "pending"}
    else:
        return {"status": "failed"}
