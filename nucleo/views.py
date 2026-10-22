from django.shortcuts import render, redirect, get_object_or_404
from nucleo.models import Colaborador, Equipamentos, Emprestimo
from nucleo.forms import EmprestimoForm
from django.contrib import messages
from django.db.models import ProtectedError


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

    colaborador = Colaborador.objects.create(
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
def equipments(req):
    pesquisa = req.GET.get('pesquisa', '').strip()
    equipamentos = Equipamentos.objects.all()
    
    if pesquisa:
        colaboradores = colaboradores.filter(nome__icontains=pesquisa)
    return render(req, 'nucleo/equipments.html', {
        'equipamentos': equipamentos,
        'pesquisa': pesquisa,
    })

    
def controle_epi(req):
    equipamento = req.GET.get('equipamento', '').strip()
    colaborador = req.GET.get('colaborador', '').strip()
    status = req.GET.get('status', '').strip()

    emprestimos = Emprestimo.objects.select_related('colaborador', 'equipamento')

    # Filtro do tipo AND: cada campo preenchido restringe ainda mais o resultado
    if equipamento:
        emprestimos = emprestimos.filter(equipamento__nome__icontains=equipamento)
    if colaborador:
        emprestimos = emprestimos.filter(colaborador__nome__icontains=colaborador)
    if status in dict(Emprestimo.STATUS_CHOICES):
        emprestimos = emprestimos.filter(status=status)

    return render(req, 'nucleo/controle_epi.html', {
        'emprestimos': emprestimos,
        'equipamento': equipamento,
        'colaborador': colaborador,
        'status': status,
        'status_choices': Emprestimo.STATUS_CHOICES,
    })


def emprestimo_criar(req):
    form = EmprestimoForm(req.POST or None)
    if req.method == 'POST' and form.is_valid():
        form.save()
        messages.success(req, "Cadastrado com sucesso!")
        return redirect('epi-controle')
    return render(req, 'nucleo/forms/emprestimo.html', {'form': form, 'titulo': 'Novo empréstimo'})


def emprestimo_editar(req, id):
    emprestimo = get_object_or_404(Emprestimo, id=id)
    form = EmprestimoForm(req.POST or None, instance=emprestimo)
    if req.method == 'POST' and form.is_valid():
        form.save()
        messages.success(req, "Editado com sucesso!")
        return redirect('epi-controle')
    return render(req, 'nucleo/forms/emprestimo.html', {'form': form, 'titulo': 'Editar empréstimo'})