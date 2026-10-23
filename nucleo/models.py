from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=30, null=False, blank=False)
    telefone = models.CharField(max_length=30)

    def __str__(self):
        return self.nome

# ----- EQUIPAMENTOS -----

# Esse salva o tipo do equipamento (Exemplo: registro centralizado de óculos de proteção Okley)
# Age como um registro central de um tipo de equipamento
class TipoEquipamento(models.Model):
    CATEGORIA_CHOICES = [
         ('CABECA', 'Cabeça'),
         ('FACE','Face'),
         ('AUDITIVO','Auditivo'),
         ('RESPIRATORIO', 'Respiratório'),
         ('TRONCO', 'Tronco'),
         ('MEMBROS_SUPERIORES', 'Membros superiores'),
         ('MEMBROS_INFERIORES', 'Membros inferiores'),
         ('QUEDAS', 'Quedas'),
    ]

    nome = models.CharField(max_length=30, null=False, blank=False)
    descricao = models.CharField(max_length=100)
    categoria = models.CharField(max_length=30, null=False, choices=CATEGORIA_CHOICES, blank=False)

    @property
    def quantidade_total(self):
        return self.equipamentos.count()

# Esse salva registro individuais de um equipamento de um tipo (Exemplo: um óculos de proteção okley)
# Age como o equipamento individual em sí, porém ele faz parte de um tipo
class Equipamentos(models.Model):
    SITUACAO_CHOICES = [
       ('DISPONIVEL', 'Disponível'),
       ('EM_USO', 'Em uso'),
       ('INATIVO', 'Inativo'),  
    ]

    tipo = models.ForeignKey(TipoEquipamento, on_delete=models.PROTECT, related_name='equipamentos', null=False, blank=False)
    codigo_patrimonio = models.CharField(max_length=30, null=False)
    situacao = models.CharField(max_length=30, null=False, choices=SITUACAO_CHOICES, default='DISPONIVEL', blank=False)

# ----- EQUIPAMENTOS -----

class Emprestimo(models.Model):
    CONDICAO_CHOICES = [
        ('EMPRESTADO', 'Emprestado'),
        ('FORNECIDO', 'Fornecido'),
        ('DEVOLVIDO', 'Devolvido'),
        ('DANIFICADO', 'Danificado'),
        ('PERDIDO', 'Perdido'),]
    OPCOES = ['DANIFICADO', 'PERDIDO', 'DEVOLVIDO']
    colaborador = models.ForeignKey(Colaborador,on_delete=models.PROTECT, related_name='emprestimos')
    equipamento = models.ForeignKey(Equipamentos,on_delete=models.PROTECT, related_name='emprestimos')
    data_emprestimo = models.DateField()
    data_devolucao_prevista = models.DateField()
    estado_equipamento = models.CharField(max_length=20, choices=CONDICAO_CHOICES, default='EMPRESTADO')
    condicao_equipamento = models.CharField(max_length=30, null=False, blank=False)
    data_devolucao = models.DateField(null=True, blank=True)
    observacao = models.CharField(max_length=30, blank=True)
        
    