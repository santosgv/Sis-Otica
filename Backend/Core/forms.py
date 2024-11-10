from django import forms
from .models import Fornecedor, TipoUnitario, Estilo,Tipo,SERVICO,Lentes

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome']

class TipoUnitarioForm(forms.ModelForm):
    class Meta:
        model = TipoUnitario
        fields = ['nome']

class EstiloForm(forms.ModelForm):
    class Meta:
        model = Estilo
        fields = ['nome']

class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['nome']

class ServicoForm(forms.ModelForm):
    class Meta:
        model = SERVICO
        fields = ['SERVICO']

class LentesForm(forms.ModelForm):
    class Meta:
        model = Lentes
        fields = ['nome','codigo','valor_custo']