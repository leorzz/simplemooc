from django.shortcuts import render
from django.http import HttpResponse

from .models import Course

def index(request):
    courses = Course.objects.all() #Course=model , objects=manager do model , retorna todos os objs
    template_name = 'courses/index.html'
    context = { # dicionario que será passado para o render para subtituir valores no template
        'courses': courses,
    }
    return render(request, template_name, context)    

