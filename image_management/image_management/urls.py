from django.conf.urls import include, url
from django.contrib import admin

from django.conf.urls.static import static


from image_management import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^image_converter/', include('image_converter.urls')),
    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}, name="media"),
    # url(r'^', include('imageConversionApp.urls')),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

