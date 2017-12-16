# colocar na view apenas o necessário. Minimo possivel.

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment
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
    
    
@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,  # Filtro=Usuario que esta logado no sistema
            course=course     # Propriedade do model Enrollment
        )   # Este metodo retorna uma tupla. A inscrição(pega ou cria) e um bool
            # se foi criado ou nao
            
    if created:
        enrollment.active() # Metodo criado anteriormente
        messages.success(request, 'Você foi inscrito no curso com sucesso.')
    else:
        messages.info(request, 'Você ja está inscrito no curso.')
    
    from django.contrib.messages import get_messages
    storage = get_messages(request)
    for m in storage:
        print('========>',m)
    
    return redirect('accounts:dashboard')
        
    