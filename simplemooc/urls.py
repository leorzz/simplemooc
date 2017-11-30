
from django.conf.urls import include, url
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^', include('simplemooc.core.urls', namespace='core')),
    url(r'^courses/', include('simplemooc.courses.urls', namespace='courses')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    #document_root=settings.MEDIA_ROOT = caminho absoluto
    #settings.MEDIA_URL = caminho relativo
    #este método funciona apenas de "debug mode"
    #indica qual é o caminho absoluto e relativo para estas midias
    #https://docs.djangoproject.com/en/dev/howto/static-files/
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

