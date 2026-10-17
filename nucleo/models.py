from django.db import models

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