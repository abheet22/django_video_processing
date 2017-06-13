from django.db import models
from datetime import datetime

# Create your models here.
class Videos(models.Model):
    creator_id = models.IntegerField(default=1)
    video_name = models.CharField(max_length=20)
    video_url = models.CharField(max_length=10000)
    time_created = models.DateTimeField(default=datetime.now)