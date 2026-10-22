from .models import Colaborador, Equipamentos, TipoEquipamento

TipoEquipamento.objects.create(
   nome='Paulimera',
   quantidade=2,
   descricao='Muito legal',
   categoria='FACE'
   )