from django import forms
from nucleo.models import Emprestimo


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['equipamento', 'colaborador', 'data_emprestimo', 'data_prevista_devolucao', 'status']
        widgets = {
            'data_emprestimo': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_prevista_devolucao': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def clean(self):
        dados = super().clean()
        emprestimo = dados.get('data_emprestimo')
        previsao = dados.get('data_prevista_devolucao')
        if emprestimo and previsao and previsao < emprestimo:
            self.add_error('data_prevista_devolucao', 'A data prevista não pode ser anterior à data do empréstimo.')
        return dados
