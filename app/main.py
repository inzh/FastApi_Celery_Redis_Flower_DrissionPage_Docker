import logging
import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from worker import celery_app


if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class Combo(BaseModel):
    email: str
    password: str
    HasExchange: str


app = FastAPI()


@app.get("/")
def home():
    return {"ping": "pong!!"}


@app.post("/send_combos")
async def send_combos(combo: Combo):
    logger.info(f"Checking: {combo.email}:{combo.password}")
    task_name = "o365.task"
    task = celery_app.send_task(task_name, args=[combo.email, combo.password])
    return JSONResponse({"task_id": task.id})
