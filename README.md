
# Django Multi-Tenant Mini App – Task 2

This project simulates a production-style multi-tenant application using PostgreSQL schema-based tenant isolation via `django-tenants`. It includes tenant-specific configuration and feature toggles.

---

## 🏗 Project Structure

- **`models.py`**: Defines the `Client` and `Domain` models using `TenantMixin` and `DomainMixin`.
- **`views.py`**: Implements the config API and feature toggle view, enforcing schema-level tenant isolation.
- **`urls.py`**: Maps API and feature toggle endpoints.
- **`configs/`**: Contains per-tenant JSON config files (e.g., `tenant_a_config.json`, `tenant_b_config.json`).
- **`tests.py`**: Contains unit tests covering config access, feature toggles, and edge cases.

---

## 🔌 Endpoints

### 1. GET `/api/config/<tenant_id>/`

Returns the JSON config for the specified tenant. Access is allowed **only if** the current request schema matches the tenant.

#### ✅ Sample Success Response (`tenant_id = a`)
```json
{
  "tenant_id": "a",
  "enable_custom_page": true,
  "page_title": "Welcome to Tenant A"
}
```

#### ❌ Error Cases
- Wrong schema → `403 Forbidden`
- Config missing → `404 Not Found`
- Bad JSON → `500 Server Error`

---

### 2. GET `/<tenant_id>/page/`

Displays a custom HTML page if the tenant's config has `"enable_custom_page": true`. Otherwise returns `403`.

#### ✅ Success Example
Returns:
```html
<h1>Welcome to Tenant A</h1>
```

---

## ⚙ Setup Instructions

### 1. Clone and Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure `DATABASES` in `settings.py` for PostgreSQL
Make sure your settings look like:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'your_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Apply Migrations and Create Schemas
```bash
python manage.py makemigrations
python manage.py migrate_schemas --shared
```

### 4. Create Tenants
Create at least two `Client` objects with different `schema_name` and corresponding `Domain` entries.

---

## 🧪 Running Tests
```bash
python manage.py test tenants
```

Covers:
- Config access (valid/invalid schema)
- Feature toggles (enabled/disabled)
- Missing or bad config handling

---

## 📁 Sample Configs

Located in `/configs/` directory:

### tenant_a_config.json
```json
{
  "tenant_id": "a",
  "enable_custom_page": true,
  "page_title": "Welcome to Tenant A"
}
```

### tenant_b_config.json
```json
{
  "tenant_id": "b",
  "enable_custom_page": false,
  "page_title": "Access Denied"
}
```

---

## 📎 Notes
- Follows schema-based tenant isolation using `django-tenants`
- All data/config access is protected against cross-tenant leaks
- Easy to extend for more tenants or features

---

## ✅ Submission Checklist

- [x] PostgreSQL + `django-tenants`
- [x] Multi-schema isolation
- [x] Config API + feature toggle view
- [x] Unit tests included
- [x] Two JSON configs in `configs/`
- [x] README with setup & usage
