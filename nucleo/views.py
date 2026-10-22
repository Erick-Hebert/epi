from django.shortcuts import render, redirect, get_object_or_404
from nucleo.models import Colaborador, Equipamentos
from django.contrib import messages

def home(req):
    pesquisa = req.GET.get('pesquisa', '').strip()
    colaboradores = Colaborador.objects.all()
    if pesquisa:
        colaboradores = colaboradores.filter(nome__icontains=pesquisa)
    return render(req, 'nucleo/index.html', {
        'colaboradores': colaboradores,
        'pesquisa': pesquisa,
    })

def tela_criar(req):
    return render(req, 'nucleo/forms/criar.html')

def salvar(req):
    nome = req.POST.get('nome')

    if nome is None:
        return redirect('nucleo-criar')

    telefone = req.POST.get('telefone')

    Colaborador.objects.create(
        nome=nome,
        telefone=telefone
    )
    messages.success(req, "Cadastrado com sucesso!")
    return redirect('nucleo-inicial')


def editar(req, id):
    colaborador = get_object_or_404(Colaborador, id=id)

    if req.method == 'POST':
        nome = req.POST.get('nome')
        if nome:
            colaborador.nome = nome
            colaborador.telefone = req.POST.get('telefone')
            colaborador.save()
            messages.success(req, "Editado com sucesso!")
            return redirect('nucleo-inicial')

    return render(req, 'nucleo/forms/editar.html', {
        'colaborador': colaborador,
    })

def excluir(req, id):
    colaborador = get_object_or_404(Colaborador, id=id)

    if req.method == 'POST':
        colaborador.delete()
        messages.success(req, "Deletado com sucesso!")
        return redirect('nucleo-inicial')

    return render(req, 'nucleo/forms/excluir.html', {
        'colaborador': colaborador,
    })

# TERMINAR
def equipamentos(req):
    pesquisa = req.GET.get('pesquisa', '').strip()
    equipamentos = Equipamentos.objects.all()
    
    if pesquisa:
        colaboradores = colaboradores.filter(nome__icontains=pesquisa)
    return render(req, 'nucleo/equipamentos.html', {
        'equipamentos': equipamentos,
        'pesquisa': pesquisa,
    })

def criar_equipamento(req):
    return render(req, 'nucleo/forms/equipamentos/criar_equipamento.html')

def salvar_equipamento(req):
    return redirect('equipamentos-inicial')

def editar_equipamento(req):
    return render(req, 'nucleo/forms/equipamentos/editar_equipamento.html')

def excluir_equipamento(req):
    return render(req, 'nucleo/forms/equipamentos/excluir_equipamento.html')