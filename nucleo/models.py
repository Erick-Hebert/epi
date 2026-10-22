from django.db import models
from django.utils import timezone

class Colaborador(models.Model):
    nome = models.CharField(max_length=30, null=False, blank=False)
    telefone = models.CharField(max_length=30)

    def __str__(self):
        return self.nome

class Equipamentos(models.Model):
    nome = models.CharField(max_length=30, null=False, blank=False)
    codigo_patrimonio = models.CharField(max_length=30, null=False)
    quantidade = models.PositiveIntegerField(default=0, null=False, blank=False)
    descricao = models.CharField(max_length=100)
    categoria = models.CharField(max_length=30, null=False, blank=False) # CABEÇA, FACE, AUDITIVO, RESPIRATORIO, TRONCO, MEMBROS SUPERIORES, MEMBROS INFERIORES, QUEDAS
    situacao = models.CharField(max_length=30, null=False, blank=False) # DISPONIVEL, EMPRESTADO, INATIVO

    def __str__(self):
        return self.nome
    
    
class Emprestimo(models.Model):
    STATUS_EMPRESTADO = 'EMPRESTADO'
    STATUS_DEVOLVIDO = 'DEVOLVIDO'
    STATUS_ATRASADO = 'ATRASADO'
    STATUS_CHOICES = [
        (STATUS_EMPRESTADO, 'Emprestado'),
        (STATUS_DEVOLVIDO, 'Devolvido'),
        (STATUS_ATRASADO, 'Atrasado'),
    ]

    colaborador = models.ForeignKey(Colaborador, on_delete=models.PROTECT, related_name='emprestimos')
    equipamento = models.ForeignKey(Equipamentos, on_delete=models.PROTECT, related_name='emprestimos')
    data_emprestimo = models.DateField(default=timezone.localdate)
    data_prevista_devolucao = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_EMPRESTADO)

    class Meta:
        ordering = ['-data_emprestimo', '-id']

    def __str__(self):
        return f'{self.equipamento} - {self.colaborador}'