import json
import os
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.conf import settings

def config_view(request, tenant_id):
    try:
        current_schema = request.tenant.schema_name
    except AttributeError:
        return HttpResponseForbidden("Tenant context missing. Check domain configuration.")

    expected_schema = f"tenant_{tenant_id}"

    if current_schema != expected_schema:
        return HttpResponseForbidden("You are not allowed to access this config.")

    config_path = os.path.join(settings.BASE_DIR, 'configs', f'tenant_{tenant_id}_config.json')

    if not os.path.exists(config_path):
        return HttpResponseNotFound("Config not found.")

    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON format.", status=500)

    return JsonResponse(data)


def custom_page_view(request, tenant_id):
    try:
        current_schema = request.tenant.schema_name
    except AttributeError:
        return HttpResponseForbidden("Tenant context missing. Check domain configuration.")

    expected_schema = f'tenant_{tenant_id}'

    if current_schema != expected_schema:
        return HttpResponseForbidden("Unauthorized access to another tenant’s page.")

    config_path = os.path.join(settings.BASE_DIR, 'configs', f'tenant_{tenant_id}_config.json')
    
    if not os.path.exists(config_path):
        return HttpResponseNotFound("Config not found.")

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON config file.", status=500)

    if config.get("enable_custom_page", False):
        page_title = config.get("page_title", "Welcome Page")
        return HttpResponse(f"<h1>{page_title}</h1>")
    else:
        return HttpResponseForbidden("403 Feature disabled for this tenant.")
   
print("✅ config_view and custom_page_view are defined.")
