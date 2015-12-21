# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf.urls.static import static

from image_management import settings
from . import views

urlpatterns =[
    url(r'^$', views.list_images, name='root'),
    url(r'^index$', views.list_images, name='index'),
    url(r'^images', views.list_images, name='images'),
    url(r'^tasks', views.manage_tasks, name='task'),
    url(r'^cancel_tasks', views.cancel_task, name='cancel_tasks'),
    url(r'^get_image/(?P<pk>\d+)/', views.manage_tasks, name='get_image'),
    url(r'^upload', views.create_tasks, name='upload'),
    url(r'^show/(?P<image_id>[A-Za-z0-9.,_-]+)$', views.show_view, name='show'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)