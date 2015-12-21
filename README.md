imageConversion
===============
---------------

Image Conversion Tool In Django

Exercise
========
The exercise consists on developing an Image Conversion utility that will be usable via browser.

The users will be able to submit a PNG file through the web that will be converted to JPG format (submitting a PNG file generates a conversion task in the server)

The web page will also show all submitted tasks and its state information (queued, running, error, complete, ...)

The users will be able to download the resulting JPG file from a completed task.

We will suppose that our processing resources are limited and we will only allow a maximum of 3 conversion tasks to be executed simultaneously in the server, the rest of submitted tasks will be accepted but queued for later processing.

In case of getting an error while processing, a description of the error for that task will be shown.


Comments
--------
* You can assume that all users of the system act as a single anonymous user and share the same tasks.

* You will need to manually extend the processing time of each task for testing purposes.

* The beauty of the webpage is not important (usability is important though)


Getting started
===============


- Install redis as a Celery “Broker”. You can install redis server via brew or from the official download [page](http://redis.io/download):

    > brew install redis
    
- Start the Redis server
    >redis-server
    
- You can test that Redis is working properly by typing this into your terminal:
    >redis-cli ping  \#Redis should reply with PONG
    
- Create and activate a virtualenv using Python 3.5.1.

- Install the dependencies listed in the requirements.txt file:
    > pip install -r requirements.txt
    
- Start celery instance using the django-celery management command to run celery on the foreground:

    > python manage.py celeryd -l info

- Start the development server to use the app:

    > python manage.py runserver

Requirements
============

This app was developed using this environment: 

Python version
--------------
* Python 3.5.1.

Python libraries
----------------

* Django==1.9
* celery==3.1.19
* django-celery==3.1.17
* django-crispy-forms==1.5.2
* django-model-utils==2.4
* image==1.4.3
* redis==2.10.5

External
--------
* Redis Server==3.0.5

Operative System
--------
* Mac OSx El Capitan 10.11.1


Implementation notes
====================


In the settings.py file there setted all the celery configuration params. Including the **BROKER_URL**, the **CELERY_RESULT_BACKEND**, and the option called **TASK_SLEEP_TIME** that sets time in seconds wich the conversion tasks will wait to execute, this value is set in 20 seg for testing propose.

If the service is shut down, restarting the app will restart any task that was being processed at the moment, and also maintain the pending task queue.

The app allow the users to cancel a submitted task.


