from django.shortcuts import render
from .models import Comunicado

# Create your views here.
def index(request):
    comunicados = Comunicado.objects.all()

    return render(
        request, 
        'comunicados/index.html',
        context={
            'comunicados': comunicados,
        },)