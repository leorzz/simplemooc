# colocar na view apenas o necessário. Minimo possivel.

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Course
from .forms import ContactCourse # o ponto indica que o import é relatico ao proprio pacote

def index(request):
    courses = Course.objects.all() #Course=model , objects=manager do model , retorna todos os objs
    template_name = 'courses/index.html'
    context = { # dicionario que será passado para o render para subtituir valores no template
        'courses': courses,
    }
    return render(request, template_name, context)    

#def details(request, pk):
#    #course = Course.objects.get(pk=pk)
#    #caso não tenha valor retorna uma página http=404
#    course = get_object_or_404(Course, pk=pk)
#    context = {
#        'course': course
#    }
#    template_name = 'courses/details.html'
#    return render(request, template_name, context)

def details(request, slug):
    #course = Course.objects.get(pk=pk)
    #caso não tenha valor retorna uma página http=404
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True # adiciona is_valid no contexto para ser utilizado no template
            #print(form.cleaned_data)
            #print(form.cleaned_data['name']) # para acessar um campo sempre com o dicionario cleaned_data. Retorna de acordo com o tipo.
            form = ContactCourse() # limpa o formulario
    else:
        form = ContactCourse()
    
    context['form'] = form
    context['course'] = course
    
    template_name = 'courses/details.html'
    return render(request, template_name, context)