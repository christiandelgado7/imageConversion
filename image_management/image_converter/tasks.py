from io import BytesIO
from time import sleep

from PIL import Image
from celery import task
from django.core.files.base import ContentFile

from image_converter.models import ConversionTask
from image_management import settings


@task(name="convert_image")
def convert_image(pk):
    new_task = None
    try:
        new_task = ConversionTask.objects.get(pk=pk)
        if settings.TASK_SLEEP_TIME:
            sleep(settings.TASK_SLEEP_TIME)

    except ConversionTask.DoesNotExist:
        new_task.message = ("Error: Invalid Task id '%d'" % pk)
        new_task.save()
        raise

    try:
        print("converting task_id: %s, pk: %s" % (new_task.task_id, new_task.pk))
        file_name = new_task.file.name.rsplit(".", 1)[0]
        stream = BytesIO()
        image_png = Image.open(new_task.file)

        # adding white background
        image_jpg = Image.new("RGB", image_png.size, (255, 255, 255))
        image_jpg.paste(image_png, (0, 0), image_png)
        image_jpg.save(stream, format="jpeg")
        new_task.file.delete()
        new_task.file.save(file_name + ".jpg",
                           ContentFile(stream.getvalue()),
                           False)
    except IOError as e:
        new_task.message = ("IOError: converting the file in jpg : %s" % str(e)[:150])
        new_task.save()
        raise
    except Exception as e:
        new_task.message = ("Unexpected Error : %s" % str(e)[:150])
        new_task.save()
        raise
    finally:
        image_png.close()
        image_jpg.close()
        stream.close()
    new_task.save()
