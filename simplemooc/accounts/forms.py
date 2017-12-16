from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User # Model default do django

# Indicar o nosso custom user
# https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#referencing-the-user-model
from django.contrib.auth import get_user_model
User = get_user_model()

from simplemooc.core.mail import send_mail_template
from simplemooc.core.utils import generate_hash_key
from .models import PasswordReset

class PasswordResetForm(forms.Form):
    
    email = forms.EmailField(label='E-mail')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError('Nenhum usuário encontrado com este email')
            
    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'accounts/password_reset_mail.html'
        subject = 'Criar nova senha no Simple Mooc'
        context = {
            'reset': reset,
        }
        send_mail_template(subject, template_name, context, [user.email])

            
            

# Esta classe foi cirada para adicionar o campo email
# Ela extende a classe UserCreationForm e adiciona o amail
class RegisterForm(forms.ModelForm):
    
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)
    

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação não esta correta')
        return password2


    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1']) # set_password para criptografar a senha
        if commit:
            user.save()
        return user

    
    class Meta:
        model = User
        fields = ['username', 'email']
        
        
        
        
        
        
        
class EditAccountForm(forms.ModelForm): # ModelForm: formulario especifico do modelo. Pega os campos do modelo(model) e gera o formulario
    
    # Email unico no cadastro
    # from django.contrib.auth.models import User
    # Quando o djando faz a validação dos campos do form ele procura por metodos 'clean_<campo>'
    # Este metodo serve para testar, alterar ou extrair algo do campo email
    def clean_email(self):
        # instance: variavel do ModelForm que representa a instancia sendo alterada num determinado momento
        # Se não estiver sendo alterado entao o valor é 'none'
        email = self.cleaned_data['email']
        # filtra todos os usuários com email e exclui o usuário que esta sendo alterado
        queryset = User.objects.filter(
            email=email).exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError('Já existe usuário com este email')
        return email
        
    class Meta:
        model = User
        #fields = ['username', 'email', 'first_name', 'last_name'] # os campos do model (do django neste caso) que possam ser alterados
        fields = ['username', 'email', 'name']

