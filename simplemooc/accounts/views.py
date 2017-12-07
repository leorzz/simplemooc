from django.shortcuts import render, redirect #  render adiciona a variaveis como context
from django.contrib.auth.forms import UserCreationForm # modelform
from django.conf import settings

# Importa a classe criada RegisterForm onde foi adicionado o campo email
from .forms import RegisterForm



# Template do painel do usuário (5:57)
# O decorator é uma função que será executada toda vez que a func dashboard for executado passando esta como parametro.
# Vai verificar se o usuario esta logado. 
#Se não estiver ele fará um redirect para a pagina de login colocando o parametro next
from django.contrib.auth.decorators import login_required
@login_required 
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    return render(request, template_name)




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



from django.contrib.auth import authenticate, login
def mylogin(request):
    template_name = 'accounts/login.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
            else:
                # Return a 'disabled account' error message
                pass
        else:
            # Return an 'invalid login' error message.
            pass            
