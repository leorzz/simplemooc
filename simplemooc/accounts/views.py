from django.shortcuts import render, redirect, get_object_or_404 #  render adiciona a variaveis como context
from django.contrib.auth.forms import (UserCreationForm, PasswordChangeForm, SetPasswordForm) # modelform
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model

from simplemooc.core.utils import generate_hash_key

# Importa a classe criada RegisterForm onde foi adicionado o campo email
from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset


User = get_user_model()

# Template do painel do usuário (5:57)
# O decorator é uma função que será executada toda vez que a func dashboard for executado passando esta como parametro.
# Vai verificar se o usuario esta logado. 
#Se não estiver ele fará um redirect para a pagina de login colocando o parametro next
from django.contrib.auth.decorators import login_required
@login_required 
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    return render(request, template_name)

@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            form = EditAccountForm(instance=request.user)
            context['success'] = True
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)



@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)


# Override method get_context_data on class LoginView
# This assumes that the GET parameter will have the next url where user should be redirected in param next. 
# So, request should be of form localhost.com/login?next=/accounts/
# Este metodo foi sobrescrito para incluir a variavel next, que vem da url, no contexto
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
def get_context_data(self, **kwargs):
    context = super(LoginView, self).get_context_data(**kwargs)
    context['next'] = self.request.REQUEST.get('next')
    current_site = get_current_site(self.request)
    context.update({
        self.redirect_field_name: self.get_redirect_url(),
        'site': current_site,
        'site_name': current_site.name,
    })
    if self.extra_context is not None:
        context.update(self.extra_context)
    return context

#def get_context_data(self, **kwargs):
#    context = super(LoginView, self).get_context_data(**kwargs)
#    context['next'] = self.request.REQUEST.get('next')
#    return context



# https://github.com/django/django/blob/master/django/contrib/auth/forms.py
def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            user1 = authenticate(
                    username=user.username,passowrd=form.cleaned_data['password1']
                )
            #login(request,user1)
            #print('====>',user.is_authenticated)
            #return redirect('core:home')
            return redirect(settings.LOGIN_URL)
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)
    
    
    
def password_reset(request):
    template_name = 'accounts/password_reset.html'
    context = {}
    form = PasswordResetForm(request.POST or None) # Se o POST estiver vazio então prenche com none. 
                                        # O mesmo que chamar PasswordResetForm() assim ele não é automaticamente validado
    if form.is_valid():
        form.save()
        context['sucess'] = True
    context['form'] = form
    return render(request, template_name, context)
    


def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)