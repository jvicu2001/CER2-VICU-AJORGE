from django.shortcuts import render
from .models import Comunicado, Entidad

# Create your views here.
def index(request):
    comunicados = Comunicado.objects.all()
    entidades = Entidad.objects.all()

    return render(
        request, 
        'comunicados/index.html',
        context={
            'comunicados': comunicados,
            'entidades': entidades
        },)

def comunicado(request, id):
    comunicado = Comunicado.objects.filter(id=id).first

    return render(
        request,
        'comunicados/comunicado.html',
        context={
            'comunicado': comunicado
        }
    )