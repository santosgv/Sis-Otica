from django.http import HttpResponse
from django_tenants.middleware.main import TenantMainMiddleware
from django_tenants.utils import get_tenant_model,remove_www

class TenantActiveMiddleware(TenantMainMiddleware):
    def get_tenant(self, domain_model, hostname):
        tenant = super().get_tenant(domain_model, hostname)
        if not tenant.is_active:
            raise self.TENANT_NOT_FOUND_EXCEPTION("Tenant is inactive")
        return tenant
    def process_request(self, request):
        # Get the current tenant
        tenant = request.tenant

        # Get the Tenant model
        TenantModel = get_tenant_model()

        # Check if the tenant is active
        if not TenantModel.objects.filter(schema_name=tenant.schema_name, is_active=True).exists():
            return HttpResponse("Cliente esta Inativo.", status=403)

        # Continue with the request if the tenant is active
        response = super().process_request(request)
        return response
