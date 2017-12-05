from django.conf.urls import  include, url
import django.contrib.auth.views
import simplemooc.accounts.views as views_accounts

urlpatterns = [
    url(r'^login/$', django.contrib.auth.views.login, {'template_name': 'accounts/login.html'}, name='login'),
    
    # O dic vai virar parametros nomeados para a view logout do django
    url(r'^logout/$', django.contrib.auth.views.logout, {'next_page': 'core:home'}, name='logout'),
    
    url(r'^register/$', views_accounts.register, name='register'),
]
