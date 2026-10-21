from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hola_mundo(request):
    return HttpResponse("Hola Mundo, bienvenido a Progra III")

def edad(request):
    return HttpResponse("Vista edad funcionando")

def index(request):
    return render(request, 'index.html') #renderiza la plantilla index.html