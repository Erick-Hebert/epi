from django.shortcuts import render, redirect, get_object_or_404
from nucleo.models import Colaborador, Equipamentos, TipoEquipamento, Emprestimo
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
    #(TipoEquipamento.objects.get(nome='Paulimera')).delete()

    pesquisa = req.GET.get('pesquisa', '').strip()
    tipos_equipamento = TipoEquipamento.objects.all()
    
    if pesquisa:
        tipos_equipamento = tipos_equipamento.filter(nome__icontains=pesquisa)
    return render(req, 'nucleo/equipamentos.html', {
        'tipos_equipamento': tipos_equipamento,
        'pesquisa': pesquisa,
    })

def criar_equipamento(req):
    return render(req, 'nucleo/forms/equipamentos/criar_equipamento.html')

def salvar_equipamento(req):
    nome = req.POST.get('nome')

    if nome is None:
        return redirect('equipamentos-criar')

    categoria = req.POST.get('categoria')
    descricao = req.POST.get('descricao')

    TipoEquipamento.objects.create(
        nome=nome,
        categoria=categoria,
        descricao=descricao
    )
    messages.success(req, "Cadastrado com sucesso!")

    return redirect('equipamentos-inicial')

def editar_equipamento(req, id):
    equipamento = get_object_or_404(TipoEquipamento, id=id)
    
    if req.method == 'POST':
        nome = req.POST.get('nome')
        if nome:
            equipamento.nome = nome
            equipamento.descricao = req.POST.get('descricao')
            equipamento.categoria = req.POST.get('categoria')

            equipamento.save()
            messages.success(req, "Editado com sucesso!")
            return redirect('equipamentos-inicial')

    return render(req, 'nucleo/forms/equipamentos/editar_equipamento.html', {
        'equipamento': equipamento,
    })

def excluir_equipamento(req, id):
    equipamento = get_object_or_404(TipoEquipamento, id=id)
    
    if req.method == 'POST':
        equipamento.delete()
        messages.success(req, "Deletado com sucesso!")
        return redirect('equipamentos-inicial')

    return render(req, 'nucleo/forms/equipamentos/excluir_equipamento.html', {
        'equipamento': equipamento,
    })

    
def emprestimos(req):
    lista = Emprestimo.objects.all()

    return render(req, 'nucleo/emprestimo.html', {'emprestimo' : lista,})

def criar_emprestimo(req):
    equipamentos = Equipamentos.objects.filter(situacao='DISPONIVEL')
    colaboradores = Colaborador.objects.all()

    if req.method == 'POST':
        Emprestimo.objects.create(
            equipamento_id=req.POST['equipamento'],
            colaborador_id=req.POST['colaborador'],
            data_emprestimo=req.POST['data_emprestimo'],
            data_devolucao_prevista=req.POST['data_devolucao_prevista'],
            estado_equipamento=req.POST['status'],
            condicao_equipamento=req.POST['condicao'],
            data_devolucao=req.POST.get('data_devolucao') or None,
            observacao=req.POST.get('observacao', ''),
        )

        messages.success(req, 'Empréstimo cadastrado com sucesso!')
        return redirect('emprestimo-inicial')

    return render(req, 'nucleo/forms/emprestimo/criar_emprestimo.html', {
        'equipamentos': equipamentos,
        'colaboradores': colaboradores,
    })
    
def salvar_emprestimo(request):
    if request.method == 'POST':
        equipamento_id = request.POST.get('equipamento')
        nome_responsavel = request.POST.get('nome_responsavel')
        data_prevista = request.POST.get('data_prevista_devolucao')

        equipamento = get_object_or_404(
            Equipamentos.objects.select_for_update(),
            pk=equipamento_id
        )

        if equipamento.situacao != 'DISPONIVEL':
            messages.error(request, 'Equipamento indisponível para empréstimo.')
            return redirect('salvar_emprestimo')

        if not nome_responsavel or not data_prevista:
            messages.error(request, 'Preencha todos os campos.')
            return redirect('salvar_emprestimo')

        Emprestimo.objects.create(
            equipamento=equipamento,
            nome_responsavel=nome_responsavel,
            data_prevista_devolucao=data_prevista
        )

        equipamento.situacao = 'EM_USO'
        equipamento.save(update_fields=['situacao'])

        messages.success(request, 'Empréstimo registrado com sucesso!')
        return redirect('salvar_emprestimo')

    equipamentos = Equipamentos.objects.filter(
        situacao='DISPONIVEL'
    )

    return render(request, 'emprestimos/formulario.html', {
        'equipamentos': equipamentos
    })

def editar_emprestimo(req, id):
    emprestimo = get_object_or_404(Emprestimo, id=id)

    if req.method == 'POST':
        emprestimo.equipamento_id = req.POST['equipamento']
        emprestimo.colaborador_id = req.POST['colaborador']
        emprestimo.data_emprestimo = req.POST['data_emprestimo']
        emprestimo.data_devolucao_prevista = req.POST['data_devolucao_prevista']
        emprestimo.estado_equipamento = req.POST['status']
        emprestimo.condicao_equipamento = req.POST['condicao']
        emprestimo.data_devolucao = req.POST.get('data_devolucao') or None
        emprestimo.observacao = req.POST.get('observacao', '')

        emprestimo.save()
        messages.success(req, 'Empréstimo atualizado!')
        return redirect('emprestimo-inicial')

    return render(req, 'nucleo/forms/emprestimo/editar_emprestimo.html', {
        'emprestimo': emprestimo,
        'equipamentos': Equipamentos.objects.all(),
        'colaboradores': Colaborador.objects.all(),
    })
