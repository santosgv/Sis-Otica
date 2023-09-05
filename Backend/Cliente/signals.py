from django.dispatch import receiver
from django_tenants.signals import  post_schema_sync
from django.db.models.signals import pre_save
from django_tenants.models import TenantMixin
from django.utils import timezone
from .models import Cliente
from django_tenants.utils import tenant_context
from .Autenticacao.USUARIO import USUARIO
from django.core.mail import send_mail
from decouple import config
from .tasks import Envia_email_com_super_usuario,desativar_clientes

@receiver(post_schema_sync, sender=TenantMixin)
def created_user_client(sender, **kwargs):
    client = kwargs['tenant']
    with tenant_context(client):
        super_user = USUARIO.objects.create_superuser(
            username=client.schema_name,
            first_name=client.nome,
            password=client.schema_name,
            FUNCAO='G'
        )
        super_user.save()
        print('Foi chamado')
        return 'Super Usuario Criado'