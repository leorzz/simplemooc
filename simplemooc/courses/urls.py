from django.conf.urls import  include, url
import simplemooc.courses.views

urlpatterns = [
    url(r'^$', simplemooc.courses.views.index, name='index'),
]
