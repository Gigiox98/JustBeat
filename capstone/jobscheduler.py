from .models import RecoverUser
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.utils import timezone

def delete_recover_password_job(): # pragma: no cover
    RecoverUser.objects.filter(insertionDate__lte = (timezone.now() - timedelta(hours=1, minutes=0))).delete()
  
def delete_friend_request_job(): # pragma: no cover
    RecoverUser.objects.filter(insertionDate__lte = (timezone.now() - timedelta(days=7))).delete()

def start(): # pragma: no cover
    scheduler = BackgroundScheduler()
    scheduler.add_job(
      delete_recover_password_job,
      trigger=CronTrigger(hour="*/1"),  # Every 1 hour
      id="delete_recover_password_job",
      max_instances=1,
      replace_existing=True,
    )

    scheduler.add_job(
      delete_friend_request_job,
      trigger=CronTrigger(hour="0", minute="0"), # Every day at 0:00
      id="delete_friend_request_job",
      max_instances=1,
      replace_existing=True,
    )

    try:
      scheduler.start()
    except KeyboardInterrupt:
      scheduler.shutdown()