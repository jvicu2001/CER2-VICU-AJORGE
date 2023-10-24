from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Comunicado, Entidad

# Create your views here.
def index(request):
    return redirect(listado, 0)

def listado(request: HttpRequest):
    entidad_id = int(request.GET.get('id', 0))

    comunicados = Comunicado.objects.filter(entidad_id=entidad_id) if entidad_id else Comunicado.objects.all()
    entidades = Entidad.objects.all()

    return render(
        request, 
        'comunicados/listado.html',
        context={
            'comunicados': comunicados,
            'entidades': entidades,
            'id_entidad_actual': entidad_id
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