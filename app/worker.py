import os

from celery import Celery


# If you want to keep track of the tasks’ states, you need to enable result backend
# In this example, we dont need the tasks’ states
celery_app = Celery(
    "tasks",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
    # backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
)

celery_app.conf.timezone = 'Asia/Shanghai'
celery_app.conf.enable_utc = False
