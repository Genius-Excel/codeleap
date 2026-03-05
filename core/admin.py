from django.contrib import admin
from django.apps import apps
models = apps.get_app_config('core').get_models()

# Register all models
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass