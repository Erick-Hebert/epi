from django.shortcuts import render
from nucleo.models import Colaborador

def home(req):
    colaboradores = Colaborador.objects.all()
    print(f'Colaboradores: {colaboradores}')
    return render(req, 'nucleo/index.html')
