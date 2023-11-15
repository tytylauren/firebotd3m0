"""
WSGI config for fbl_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for the 'fbl_backend' project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fbl_backend.settings')

# Get the WSGI application for the Django project.
application = get_wsgi_application()

# Additional WSGI middleware or configurations can be added here if needed.
# For example, you might add middleware for logging, security enhancements, or other WSGI-level features.

