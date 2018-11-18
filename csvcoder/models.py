from __future__ import unicode_literals

from django.db import models
from datetime import datetime

class Upload(models.Model):
	file_name = models.CharField(max_length = 250)
	uploaded_time = models.DateTimeField(default = datetime.now)
	size = models.IntegerField()
	geocoding_status = models.IntegerField(default = 1)

class Location(models.Model):
	address = models.TextField(null = True,blank = True)
	upload = models.ForeignKey(Upload)
	lat_long = models.CharField(max_length = 100)
	is_geocoded = models.IntegerField(default=1)





