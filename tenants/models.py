from django_tenants.models import TenantMixin, DomainMixin
from django.db import models



class Client(TenantMixin):
    
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # required
    auto_create_schema = True

class Domain(DomainMixin):
    pass
