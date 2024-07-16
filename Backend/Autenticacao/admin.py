from django.contrib import admin
from .models import Colaborador,Comissao,Desconto

admin.site.register(Colaborador)
admin.site.register(Desconto)
admin.site.register(Comissao)