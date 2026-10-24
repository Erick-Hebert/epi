from django.test import TestCase
from django.urls import reverse
from nucleo.models import Colaborador, Emprestimo, Equipamentos, TipoEquipamento


class EquipamentoRegistroTests(TestCase):
    def setUp(self):
        self.tipo = TipoEquipamento.objects.create(nome='Capacete', descricao='Proteção', categoria='CABECA')
        self.registro = Equipamentos.objects.create(tipo=self.tipo, codigo_patrimonio='EPI-001')
        self.lista = reverse('equipamentos-registros-inicial', args=[self.tipo.id])
        self.salvar = reverse('equipamentos-registros-salvar', args=[self.tipo.id])

    def test_paginas_e_pesquisa(self):
        for nome, id in [('equipamentos-registros-inicial', self.tipo.id),
                         ('equipamentos-registros-criar', self.tipo.id),
                         ('equipamentos-registros-editar', self.registro.id),
                         ('equipamentos-registros-excluir', self.registro.id)]:
            self.assertEqual(self.client.get(reverse(nome, args=[id])).status_code, 200)
        self.assertContains(self.client.get(self.lista, {'pesquisa': '001'}), 'EPI-001')
        self.assertNotContains(self.client.get(self.lista, {'pesquisa': '999'}), 'EPI-001')

    def test_criar_e_editar(self):
        resposta = self.client.post(self.salvar, {'codigo_patrimonio': ' EPI-002 ', 'situacao': 'DISPONIVEL'})
        self.assertRedirects(resposta, self.lista)
        novo = Equipamentos.objects.get(codigo_patrimonio='EPI-002')
        self.assertEqual(novo.tipo, self.tipo)
        resposta = self.client.post(reverse('equipamentos-registros-editar', args=[novo.id]), {
            'codigo_patrimonio': 'EPI-003', 'situacao': 'INATIVO',
        })
        self.assertRedirects(resposta, self.lista)
        novo.refresh_from_db()
        self.assertEqual((novo.codigo_patrimonio, novo.situacao), ('EPI-003', 'INATIVO'))

    def test_validacoes(self):
        for codigo, situacao in [('epi-001', 'DISPONIVEL'), ('   ', 'DISPONIVEL'),
                                 ('EPI-002', 'INVALIDA'), ('x' * 31, 'DISPONIVEL')]:
            resposta = self.client.post(self.salvar, {'codigo_patrimonio': codigo, 'situacao': situacao})
            self.assertEqual(resposta.status_code, 200)
            self.assertTrue(resposta.context['form'].errors)
        self.assertEqual(Equipamentos.objects.count(), 1)
        resposta = self.client.post(reverse('equipamentos-registros-editar', args=[self.registro.id]), {
            'codigo_patrimonio': 'EPI-001', 'situacao': 'DISPONIVEL',
        })
        self.assertRedirects(resposta, self.lista)

    def test_exclusao_requer_post(self):
        url = reverse('equipamentos-registros-excluir', args=[self.registro.id])
        self.client.get(url)
        self.assertTrue(Equipamentos.objects.filter(pk=self.registro.id).exists())
        self.assertRedirects(self.client.post(url), self.lista)
        self.assertFalse(Equipamentos.objects.filter(pk=self.registro.id).exists())
        self.assertEqual(self.client.get(self.salvar).status_code, 405)

    def test_preserva_historico(self):
        pessoa = Colaborador.objects.create(nome='Ana', telefone='71999999999')
        Emprestimo.objects.create(colaborador=pessoa, equipamento=self.registro,
                                 data_emprestimo='2026-10-23', data_devolucao_prevista='2026-10-30',
                                 condicao_equipamento='Bom')
        resposta = self.client.post(reverse('equipamentos-registros-excluir', args=[self.registro.id]), follow=True)
        self.assertContains(resposta, 'possui empréstimos vinculados')
        self.assertTrue(Equipamentos.objects.filter(pk=self.registro.id).exists())

    def test_tipo_inexistente(self):
        self.assertEqual(self.client.get(reverse('equipamentos-registros-criar', args=[9999])).status_code, 404)
