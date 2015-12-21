"""
WSGI config for image_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
from image_converter.models import ConversionTask
from image_converter import tasks

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "image_management.settings")

# enqueue all the pending tasks when start the app
task_list = ConversionTask.objects.all()
for task in task_list:
    if task.celery_status == "STARTED" or task.celery_status == "PENDING":
        try:
            new_task = tasks.convert_image.delay(task.pk)
            if new_task is not None:
                task.task_id = new_task.task_id
                task.save()
        except Exception as e:
            print("Error adding the task '%d': %s" % (task.pk, str(e)))

application = get_wsgi_application()
