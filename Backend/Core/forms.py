from django import forms
from .models import Review,Fornecedor, TipoUnitario, Estilo,Tipo,SERVICO,LABORATORIO

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["nota", "comentario"]

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        self.fields['nota'].widget.attrs.update({'class': 'form-control'})
        self.fields['comentario'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite seu comentário...',
            'rows': 4
        })

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


class laboratorioForm(forms.ModelForm):
    class Meta:
        model = LABORATORIO
        fields = ['LABORATORIO']

