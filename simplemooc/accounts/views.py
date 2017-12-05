from django.shortcuts import render, redirect #  render adiciona a variaveis como context
from django.contrib.auth.forms import UserCreationForm # modelform
from django.conf import settings

# Importa a classe criada RegisterForm onde foi adicionado o campo email
from .forms import RegisterForm

# https://github.com/django/django/blob/master/django/contrib/auth/forms.py
def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    
    print(str(request.user.is_authenticated()))
    print(request.user.is_anonymous())
        
    return render(request, template_name, context)


