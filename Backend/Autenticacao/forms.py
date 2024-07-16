from django import forms
from .models import Colaborador, Desconto, Comissao

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['usuario', 'salario_bruto', 'comissao_percentual', 'data_contratacao']

class DescontoForm(forms.ModelForm):
    class Meta:
        model = Desconto
        fields = ['colaborador', 'tipo', 'percentual']

class ComissaoForm(forms.ModelForm):
    class Meta:
        model = Comissao
        fields = ['colaborador', 'valor_vendas', 'data_referencia']