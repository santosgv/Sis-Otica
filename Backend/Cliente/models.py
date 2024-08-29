from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now
from Autenticacao.models import USUARIO
from django_tenants.models import DomainMixin, TenantMixin
from django.utils import timezone

class Cliente(TenantMixin):
    Usuario = models.ForeignKey(USUARIO, on_delete=models.SET_NULL, null=True)
    razao_social=models.CharField(max_length=255)
    pago_ate = models.DateField(default=now)
    on_trial = models.BooleanField(default=True, blank=True)
    descricao = models.TextField(blank=True)
    email = models.EmailField(null=True)
    unidade= models.CharField(max_length=6)

    is_active = models.BooleanField(default=False, blank=True)
    created_on = models.DateField(auto_now_add=True)


    auto_create_schema = True

    """
    USE THIS WITH CAUTION!
    Set this flag to true on a parent class if you want the schema to be
    automatically deleted if the tenant row gets deleted.
    """
    auto_drop_schema = True


    class Meta:
        ordering = ('-on_trial', '-pago_ate')

    def __str__(self):
        return f"{self.razao_social}"

    def is_active_now(self):
        #pago_ate = self.pago_ate.date()
        return self.pago_ate > timezone.now().date()


class Domain(DomainMixin):
    pass