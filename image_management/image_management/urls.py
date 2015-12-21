from django.conf.urls import include, url
from django.contrib import admin

from django.conf.urls.static import static


from image_management import settings

urlpatterns = [
    url(r'^$', include('image_converter.urls', namespace="image_converter")),
    url(r'^admin/', admin.site.urls),
    url(r'^image_converter/', include('image_converter.urls')),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

