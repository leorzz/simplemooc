from django.conf.urls import  include, url
import simplemooc.accounts.views as views_accounts
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import LoginView

# https://cursos.alura.com.br/forum/topico-login-django-1-10-46906
urlpatterns = [
    #url(r'^login/?$', login, kwargs={'template_name': 'accounts/login.html'}, name="login"),
    url(r'^$', views_accounts.dashboard, name='dashboard'),
    url(r'^register/$', views_accounts.register, name='register'),
    
    url(r'^password_reset/$', views_accounts.password_reset, name='password_reset'),
    
    url(r'^password_reset_confirm/(?P<key>\w+)/$', views_accounts.password_reset_confirm, name='password_reset_confirm'),
    
    url(r'^edit/$', views_accounts.edit, name='edit'),
    url(r'^edit_password/$', views_accounts.edit_password, name='edit_password'),
    url(r'^login/$', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    url(r'^logout/$',logout_then_login,{'login_url': 'accounts:login'}, name="logout"),
]
