from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Esta classe foi cirada para adicionar o campo email
# Ela extende a classe UserCreationForm e adiciona o amail
class RegisterForm(UserCreationForm):
    
    email = forms.EmailField(label='E-mail')

    # Email unico no cadastro (4:50)
    # from django.contrib.auth.models import User
    # Quando o djando faz a validação dos campos do form ele procura por metodos 'clean_<campo>'
    # Este metodo serve para testar, alterar ou extrair algo do campo email
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists(): # filtro que retorna uma lista (queryset) de usuários + a operação exists
            raise forms.ValidationError('Este email já esta sendo utilizado.')
        return email # retorna para o model

    
    # https://github.com/django/django/blob/1.11.7/django/contrib/auth/forms.py
    # linha 109
    #def save(self, commit=True):
    #    user = super(UserCreationForm, self).save(commit=False)
    #    user.set_password(self.cleaned_data["password1"])
    #    if commit:
    #        user.save()
    #return user   
    
    # Sobrescrevendo o metodo acima
    # Custom Form de Cadastro (7:55)
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        # cleaned_data = dic que contem os valores do form ja tranformados em obj python
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
        
    
    

        