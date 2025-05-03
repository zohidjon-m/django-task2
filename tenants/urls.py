from django.urls import path
from tenants.views import config_view, custom_page_view
import tenants.views
print("DEBUG views:", dir(tenants.views))


urlpatterns = [
    path('api/config/<str:tenant_id>/', config_view),
    path('<str:tenant_id>/page/', custom_page_view),
]

