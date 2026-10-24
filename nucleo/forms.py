from django import forms
from nucleo.models import Equipamentos


class EquipamentoRegistroForm(forms.ModelForm):
    class Meta:
        model = Equipamentos
        fields = ['codigo_patrimonio', 'situacao']
        labels = {
            'codigo_patrimonio': 'Código de patrimônio',
            'situacao': 'Situação',
        }
        widgets = {
            'codigo_patrimonio': forms.TextInput(attrs={
                'placeholder': 'Ex.: EPI-001',
            }),
        }

    def clean_codigo_patrimonio(self):
        codigo = self.cleaned_data['codigo_patrimonio'].strip()
        registros = Equipamentos.objects.filter(codigo_patrimonio__iexact=codigo)
        if self.instance.pk:
            registros = registros.exclude(pk=self.instance.pk)
        if registros.exists():
            raise forms.ValidationError('Já existe um equipamento com esse código de patrimônio.')
        return codigo
