from celery import Celery
from celery.schedules import crontab
from core.config.settings import settings 

redis_url = settings.REDIS_URL

celery_app = Celery(
    "bar_do_jaum_worker",
    broker=redis_url,
    backend=redis_url
)

# Adicione esta importação aqui para forçar o registro da task
import tasks.order_tasks

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=False,
    beat_schedule={
        "check-orders-status-every-2-minutes": {
            "task": "tasks.check_orders_status",
            "schedule": crontab(minute="*/2"),
        },
    },
)

celery_app.autodiscover_tasks(["tasks"])
