import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gps_project.settings')

from django.conf import settings
print("✅ INSTALLED_APPS:")
for app in settings.INSTALLED_APPS:
    print(" -", app)
print("✅ BASE_DIR:", settings.BASE_DIR)