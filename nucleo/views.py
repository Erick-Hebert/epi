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
    tipo_oculos = TipoEquipamento.objects.get(id=4)

    Equipamentos.objects.create(
        codigo_patrimonio='1201023',
        situacao='DISPONIVEL',
        tipo=tipo_oculos
    )

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

    return render(req, 'nucleo/forms/emprestimo/criar_emprestimo.html', {
        'equipamentos': equipamentos,
        'colaboradores': colaboradores,
    })
    
def salvar_emprestimo(request):
    if request.method == 'POST':
        equipamento_id = request.POST.get('equipamento')
        equipamento = Equipamentos.objects.get(id=equipamento_id)

        colaborador_id= request.POST.get('colaborador')
        colaborador_responsavel = Colaborador.objects.get(id=colaborador_id)

        data_emprestimo = request.POST.get('data_emprestimo')
        data_prevista = request.POST.get('data_devolucao_prevista')
        estado_equipamento = request.POST.get('estado_equipamento')
        condicao_equipamento = request.POST.get('condicao_equipamento')
        data_devolucao = request.POST.get('data_devolucao', '')
        observacao = request.POST.get('observacao', '')
        
        valores = {
            'equipamento': equipamento,
            'colaborador': colaborador_responsavel,
            'data_emprestimo': data_emprestimo ,
            'data_devolucao_prevista': data_prevista,
            'estado_equipamento': estado_equipamento,
            'condicao_equipamento': condicao_equipamento,
            'observacao': observacao,
        }

        if data_devolucao != '':
            valores['data_devolucao'] = data_devolucao

        equipamento = get_object_or_404(
            Equipamentos.objects.select_for_update(),
            pk=equipamento_id
        )

        if equipamento.situacao != 'DISPONIVEL':
            messages.error(request, 'Equipamento indisponível para empréstimo.')
            return redirect('emprestimo-inicial')

        if not colaborador_responsavel or not data_prevista:
            messages.error(request, 'Preencha todos os campos.')
            return redirect('emprestimo-inicial')

        

        Emprestimo.objects.create(**valores)

        equipamento.situacao = 'EM_USO'
        equipamento.save(update_fields=['situacao'])

        messages.success(request, 'Empréstimo registrado com sucesso!')
        return redirect('emprestimo-inicial')

    equipamentos = Equipamentos.objects.filter(
        situacao='DISPONIVEL'
    )

    return render(request, 'emprestimos/formulario.html', {
        'equipamentos': equipamentos
    })

def editar_emprestimo(req, id):
    # 1. Busca o empréstimo que será editado (Funciona tanto no GET quanto no POST)
    emprestimo = get_object_or_404(Emprestimo, id=id)

    # 2. Só processa os dados se o formulário foi enviado
    if req.method == 'POST':
        # Captura os IDs enviados pelo formulário
        equipamento_id = req.POST.get('equipamento')
        colaborador_id = req.POST.get('colaborador')

        # Busca os objetos no banco com segurança usando get_object_or_404
        equipamento = get_object_or_404(Equipamentos, id=equipamento_id)
        colaborador_responsavel = get_object_or_404(Colaborador, id=colaborador_id)

        # Captura os demais campos
        data_emprestimo = req.POST.get('data_emprestimo')
        data_prevista = req.POST.get('data_devolucao_prevista')
        estado_equipamento = req.POST.get('estado_equipamento')
        condicao_equipamento = req.POST.get('condicao_equipamento')
        data_devolucao = req.POST.get('data_devolucao', '').strip()
        observacao = req.POST.get('observacao', '')

        # Atualiza os campos do objeto (Removidas as vírgulas do final)
        emprestimo.equipamento = equipamento
        emprestimo.colaborador = colaborador_responsavel
        emprestimo.data_emprestimo = data_emprestimo
        emprestimo.data_devolucao_prevista = data_prevista
        emprestimo.estado_equipamento = estado_equipamento
        emprestimo.condicao_equipamento = condicao_equipamento
        emprestimo.observacao = observacao

        # Trata a data de devolução dinâmica (se estiver vazia no formulário, vira None)
        if data_devolucao:
            emprestimo.data_devolucao = data_devolucao
        else:
            emprestimo.data_devolucao = None

        # Salva as alterações no banco de dados
        emprestimo.save()
        
        messages.success(req, 'Empréstimo atualizado com sucesso!')
        return redirect('emprestimo-inicial')

    # 3. Se for uma requisição GET, apenas renderiza a página com o formulário limpo
    return render(req, 'nucleo/forms/emprestimo/editar_emprestimo.html', {
        'emprestimo': emprestimo,
        'equipamentos': Equipamentos.objects.all(),
        'colaboradores': Colaborador.objects.all(),
    })


# ----- REGISTROS DE EQUIPAMENTOS -----
def equipamentos_registros(req, id):
    equipamento = get_object_or_404(TipoEquipamento, id=id)
    equipamentos_registros = Equipamentos.objects.filter(tipo=id)
    pesquisa = req.GET.get('pesquisa', '').strip()

    # Pesquisa por código de patrimonio
    if pesquisa:
        equipamentos_registros = equipamentos_registros.filter(codigo_patrimonio__icontains=pesquisa)
    return render(req, 'nucleo/equipamentos_registros.html', {
        'tipos_equipamento': equipamento,
        'equipamentos_registros': equipamentos_registros,
        'pesquisa': pesquisa,
    })

def criar_equipamento_registro(req, id):
    pass

def salvar_equipamento_registro(req, id):
    pass

def excluir_equipamento_registro(req, id):
    pass

def editar_equipamento_registro(req, id):
    pass

# ----- REGISTROS DE EQUIPAMENTOS -----
