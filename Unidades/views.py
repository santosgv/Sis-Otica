from django.shortcuts import render
from Autenticacao.models import ORDEN

def home(request):
    OS = ORDEN.objects.all()
    return render(request,'home.html',{'OS':OS})
