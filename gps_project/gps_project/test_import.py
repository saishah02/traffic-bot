import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gps_project.settings')

from django.conf import settings
print(settings.INSTALLED_APPS)