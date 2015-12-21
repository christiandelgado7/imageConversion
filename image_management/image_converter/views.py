from django.http import HttpResponse
from django.shortcuts import render

from image_converter.forms import TaskFormSet
from image_converter.models import ConversionTask
from image_management.celery import app
from .tasks import convert_image


def create_tasks(request):
    success_message = None
    error_message = None
    task_list = None
    task_formset = TaskFormSet(prefix='uploader')
    template = "create_tasks.html"
    if request.method == 'POST':
        task_formset = TaskFormSet(request.POST, request.FILES, prefix='uploader')
        if task_formset.is_valid():
            for form in task_formset.forms:
                form.save()
                try:
                    task = convert_image.delay(form.instance.pk)
                    form.instance.task_id = task.task_id
                    form.instance.save()
                    success_message = "Task created"
                except Exception as e:
                    error_message = ("Error creating the Task: %s" % str(e))
        else:
            error_message = "Invalid Values"
        if error_message is None:
            template = "manage_tasks.html"
            task_list = ConversionTask.objects.all()
    return render(request, template,
                  {"task_formset": task_formset,
                   "success_message": success_message,
                   "error_message": error_message,
                   "task_list": task_list,
                   }
                  )


def cancel_task(request):
    if request.method == 'POST':
        for key in request.POST:
            if key == "csrfmiddlewaretoken":
                continue
            value = request.POST[key]
            value = value.rsplit('/')
            app.control.revoke(value[0], terminate=True)
            task = ConversionTask.objects.get(pk=value[1])
            task.save()
    return manage_tasks(request)


def manage_tasks(request):
    task_list = ConversionTask.objects.all()
    return render(request, "manage_tasks.html",
                  {"task_list": task_list,
                   "success_message": None,
                   "error_message": None,
                   }
                  )


def list_images(request):
    task_list = ConversionTask.objects.all().order_by('uploaded')
    image_list = []
    for task in task_list:
        try:
            if task.celery_status == "SUCCESS":
                image_list.append(task)
        except Exception as e:
            print("Error listing the task '%d': %s" % (task.pk, str(e)))
    return render(request, "list_images.html", {"image_list": image_list})

