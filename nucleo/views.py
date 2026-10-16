from django.shortcuts import render, redirect, get_object_or_404
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


def editar(req, id):
    colaborador = get_object_or_404(Colaborador, id=id)

    if req.method == 'POST':
        nome = req.POST.get('nome')
        if nome:
            colaborador.nome = nome
            colaborador.telefone = req.POST.get('telefone')
            colaborador.save()
            return redirect('nucleo-inicial')

    return render(req, 'nucleo/forms/editar.html', {
        'colaborador': colaborador,
    })

def excluir(req, id):
    colaborador = get_object_or_404(Colaborador, id=id)

    if req.method == 'POST':
        colaborador.delete()
        return redirect('nucleo-inicial')

    return render(req, 'nucleo/forms/excluir.html', {
        'colaborador': colaborador,
    })
