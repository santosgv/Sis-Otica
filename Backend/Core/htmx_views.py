from django.shortcuts import render,HttpResponse
from Core.models import ORDEN



def search(request):
    search = request.GET.get('search')
    Os = ORDEN.objects.filter(id=search).all()
    return render(request,'parcial/os_parcial.html',{'Ordem_servicos':Os})
