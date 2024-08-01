from django.dispatch import receiver
from django_tenants.signals import  post_schema_sync
from django_tenants.models import TenantMixin
from django.utils import timezone
from .models import Cliente,Domain
from django_tenants.utils import tenant_context
from Autenticacao.models import USUARIO
from django.core.mail import send_mail
from decouple import config


@receiver(post_schema_sync, sender=TenantMixin)
def created_user_client(sender, **kwargs):
    client = kwargs['tenant']
    with tenant_context(client):
        super_user = USUARIO.objects.create_superuser(
            username=client.schema_name,
            first_name=client.razao_social,
            password=client.schema_name,
            FUNCAO='G'
        )
        super_user.save()
        subject = 'Novo Cliente Criado'
        message = f'''O Cliente {client.razao_social} foi criado com sucesso!
        Nome do Banco : {client.schema_name}
        Usuario Administrador : {client.schema_name}
        Senha Administrador : {client.schema_name}
        valido ate : {client.pago_ate}
        Descricao : {client.descricao}
        E-mail : {client.email}
        '''
        from_email = config('EMAIL_HOST_USER')
        recipient_list = ['santosgomesv@gmail.com',client.email]
        #send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return 'Super Usuario Criado'