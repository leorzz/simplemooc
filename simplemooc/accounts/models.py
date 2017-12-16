from django.db import models
from django.core import validators
import re
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin,
    UserManager)
from django.conf import settings
    
# Aula: Custom user model
# Em settings deverá ser adicionado o AUTH_USER_MODEL para indicar este novo model
class User(AbstractBaseUser, PermissionsMixin):
    
    #Custom
    username = models.CharField(
        'Nome do Usuário', max_length=30, unique=True,
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), 
        'Este campo apenas pode conter letras, digitos ou @.+-_', 'invalid')]
    )
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    
    # Manter compatibilidade com o Admin
    # Ver https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False) # pode acessar a area admin
    
    # 'auto_now_add' tells Django that when you add a new row, you want the current date & time added. 
    # 'auto_now' tells Django to add the current date & time will be added EVERY time the record is saved.    
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username' # campo que vai ser a referencia no login e tb é unico
    REQUIRED_FIELDS = ['email'] # Utilizado na criação de superusuário.
    
    def __str__(self):                      # representação de string do usuário
        return self.name or self.username   # se nao tiver o name retorna o username
        
    def get_short_name(self):
        return self.username
        
    def get_full_name(self):
        return str(self) # metodo '__str__(self)' criado anteriormente
        
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
# Após isso vamos apagar o banco, recria-lo com o novo model, criar um uperuser
#>mv db.sqlite3 db.sqlite3.old
#>python manage.py makemigrations
#>python manage.py migrate
#>python manage.py showmigrations
# Nas versoes mis antigas do django "#>python manage.py syncdb"
#>python manage.py createsuperuser
#>sqlite3 db.sqlite3 
#sqlite> PRAGMA table_info(accounts_user); # ver as colunas da nova tabela
#sqlite> PRAGMA table_info(accounts_user); # ver o superuser criado


class PasswordReset(models.Model):
    
    # 'related_name' https://stackoverflow.com/questions/2642613/what-is-related-name-used-for-in-django
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='resets' # Se não for indicado o django cria o metodo passwordreset_set() (<model>_set())
        # from simplemooc.accounts.models import User
        # u = User.objects.all()[0]
        # u.resets.all() # if related_name is set
        # u.passwordreset_set.all()
    )
    
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    # O blank indica que este atributo não é obrigatori no caso da criação de um formulario
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True) 
    
    def __str__(self):
        return '{0} - {1}'.format(self.user, self.created_at)
        
    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']
        
        

