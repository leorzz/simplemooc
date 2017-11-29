from django.contrib import admin

# Register your models here.

from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'start_date', 'created_at'] #Campos apresentados no admin de courses
    search_fields = ['name', 'slug'] # acrescenta um campo de pesquisa utilizando as colunas name e slug
    prepopulated_fields = {'slug': ('name',)} # preenche automaticamente o campos atalho baseado em uma lista

admin.site.register(Course, CourseAdmin)