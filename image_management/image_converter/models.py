from django.db import models

from model_utils.fields import AutoCreatedField
from image_management.celery import app


class ConversionTask(models.Model):
    uploaded = AutoCreatedField("created")
    name = models.CharField(max_length=150, blank=True)
    file = models.ImageField(upload_to="%Y%m%d")
    message = models.CharField(max_length=150, null=True, blank=True)
    task_id = models.CharField(max_length=50, null=True, blank=True)

    @property
    def celery_status(self):
        try:
            return app.AsyncResult(self.task_id).status
        except:
            return "FAILURE"

    class Meta:
        ordering = ["-uploaded", "name"]

    def __unicode__(self):
        return self.name
