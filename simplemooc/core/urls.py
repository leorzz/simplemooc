from django.conf.urls import  include, url
from django.contrib import admin
admin.autodiscover()
import simplemooc.core.views

urlpatterns = [
    url(r'^$', simplemooc.core.views.home, name='home'),
    url(r'^contact/$',simplemooc.core.views.contact, name='contact'),
    url(r'^about/$',simplemooc.core.views.about, name='about'),
]


#urlpatterns = patterns('simplemooc.core.views',
#    url(r'^$','home', name='home'),
#    url(r'^contact/$','contact', name='contact'),
#    url(r'^about/$','about', name='about'),
#)
