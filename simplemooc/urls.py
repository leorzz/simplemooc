
from django.conf.urls import include, url
from django.conf.urls import url
from django.contrib import admin


urlpatterns = [
    url(r'^', include('simplemooc.core.urls', namespace='core')),
    url(r'^courses/', include('simplemooc.courses.urls', namespace='courses')),
    url(r'^admin/', admin.site.urls),
]



