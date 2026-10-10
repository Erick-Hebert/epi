from django.shortcuts import render, redirect
from nucleo.models import Colaborador

def home(req):
    colaboradores = Colaborador.objects.all()
    return render(req, 'nucleo/index.html', {
        'colaboradores': colaboradores,
    })

def tela_criar(req):
    return render(req, 'nucleo/forms/criar.html')

def salvar(req):
    nome = req.POST.get('nome')

    if nome is None:
        return redirect('nucleo-criar')

    telefone = req.POST.get('telefone')

    colaborador = Colaborador.objects.create(
        nome=nome,
        telefone=telefone
    )
    return redirect('nucleo-inicial')

