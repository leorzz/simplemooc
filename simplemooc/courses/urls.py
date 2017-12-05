from django.conf.urls import  include, url
import simplemooc.courses.views

urlpatterns = [
    url(r'^$', simplemooc.courses.views.index, name='index'),
    #url(r'^(?P<pk>\d+)/$', simplemooc.courses.views.details, name='details'), # utilizará o codigo na url
    url(r'^(?P<slug>[\w_-]+)/$', simplemooc.courses.views.details, name='details'), # utlizara o slug, \w+ = 1 ou mais letras
]
