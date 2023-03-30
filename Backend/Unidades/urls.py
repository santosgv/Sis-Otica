
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from Unidades import views

app_name = 'Unidades'

urlpatterns = [

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)