from django import forms
from .models import ContaFinanceira

class ContaFinanceiraForm(forms.ModelForm):
    class Meta:
        model = ContaFinanceira
        fields = [
            'nome', 'tipo', 'banco', 'agencia', 'numero_conta',
            'saldo_inicial', 'ativa'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Caixa Principal'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'banco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Banco do Brasil'}),
            'agencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1234-5'}),
            'numero_conta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 123456-7'}),
            'saldo_inicial': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ativa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nome': 'Nome da Conta',
            'tipo': 'Tipo',
            'banco': 'Banco',
            'agencia': 'Agência',
            'numero_conta': 'Número da Conta',
            'saldo_inicial': 'Saldo Inicial (R$)',
            'ativa': 'Conta ativa?',
        }