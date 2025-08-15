import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm_arbitrage.settings")
app = Celery("crm_arbitrage")
app.conf.worker_redirect_stdouts = False
app.conf.worker_hijack_root_logger = False
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()  # ищет tasks.py в инсталл-приложениях
