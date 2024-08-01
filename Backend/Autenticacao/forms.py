from django import forms
from .models import USUARIO, Desconto, Comissao

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = USUARIO
        fields = ['salario_bruto', 'valor_hora','comissao_percentual', 'data_contratacao']
        widgets = {
            'data_contratacao': forms.DateInput(attrs={'type': 'date'}),
        }

class DescontoForm(forms.ModelForm):
    class Meta:
        model = Desconto
        fields = ['colaborador', 'tipo', 'percentual']

class ComissaoForm(forms.ModelForm):
    class Meta:
        model = Comissao
        fields = ['colaborador', 'valor_vendas', 'horas_extras','data_referencia']
        widgets = {
            'data_referencia': forms.DateInput(attrs={'type': 'date'}),
        }