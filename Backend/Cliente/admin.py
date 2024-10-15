from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from django_tenants.utils import get_public_schema_name



from .models import Domain, Cliente

class PublicTenantOnlyMixin:
        """Allow Access to Public Tenant Only."""
        def _only_public_tenant_access(self, request):
                return True if request.tenant.schema_name == get_public_schema_name() else False
        
        def has_view_permission(self,request, view=None):
                return self._only_public_tenant_access( request)
        
        def has_add_permission(self,request, view=None):
                return self._only_public_tenant_access(request)
        
        def has_change_permission(self,request, view=None):
                return self._only_public_tenant_access( request)
        
        def has_delete_permission(self,request, view=None):
                return self._only_public_tenant_access( request)
        
        def has_view_or_change_permission(self,request, view=None):
                return self._only_public_tenant_access( request)


class DomainInline(PublicTenantOnlyMixin,admin.TabularInline):

    model = Domain
    max_num = 1

@admin.register(Cliente)
class TenantAdmin(PublicTenantOnlyMixin,TenantAdminMixin, admin.ModelAdmin):
        list_display = (
        "razao_social",
        "is_active",
        "pago_ate",
        )
        inlines = [DomainInline]
