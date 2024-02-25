from worker import celery_app
from o365_check import login_check


@celery_app.task(name="o365.task", ignore_result=True)
def start_o365_check(email, passwd):
    login_check(email, passwd)
