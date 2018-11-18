from celery import shared_task
from celery import task,shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
import utils

@shared_task(bind=True,max_retries = 10)
def query_geocodes(self,upload_id):
	retry_required = utils.geocode_rows(upload_id)
	if retry_required:
		self.retry(countdown=3600)
