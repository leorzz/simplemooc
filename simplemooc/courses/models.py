# -*- coding: utf 8 -*-
from django.db import models
from django.conf import settings

# Custom manager
class CourseManager(models.Manager):
    
    # Filtro do batabase
    def search(self, query):
        return self.get_queryset().filter(
            #name__icontains=query, description__icontains=query # and
            #models.Q(name__icontains=query) & models.Q(description__icontains=query) # end
            models.Q(name__icontains=query) | models.Q(description__icontains=query) # or
        )
        
        
# https://docs.djangoproject.com/en/1.11/ref/models/instances/
class Course(models.Model):
    
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descricao',blank=True)
    about = models.TextField('Sobre o curso', blank=True)
    start_date = models.DateField('Data de Início', null=True, blank=True)
    image = models.ImageField(upload_to='courses/images', verbose_name='Imagem', null=True, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    objects = CourseManager()
    
    # The __str__() method is called whenever you call str() on an object
    # Mostra o atributo nome do curso ao invés do objeto.
    def __str__(self):
        return self.name
        
    @models.permalink
    def get_absolute_url(self):
        #from django.core.urlresolvers import reverse # ja esta incluido
        return ('courses:details', (), ({'slug': self.slug}))
        
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name'] # cres
        #ordering = ['-name'] # decres
        

class Enrollment(models.Model):
    STATUS_CHOICES = (
            (0, 'Pendente'),
            (1, 'Aprovado'),
            (2, 'Cancelado'),
        )
    
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL, verbose_name='Usuário',
            related_name='enrollments'
        )
    course = models.ForeignKey(
            Course, verbose_name='Curso', related_name='enrollments'
        )
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=1, blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def active(self):
        self.status = 1
        self.save()
    
    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user','course'),) # Usado para indicar unicidade. Apenas poderá existir um 'Enrollment' com par user e course
                 