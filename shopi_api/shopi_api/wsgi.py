"""
WSGI config for shopi_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import dotenv

from django.core.wsgi import get_wsgi_application
dotenv.read_dotenv(os.path.dirname(os.path.dirname(__file__),))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopi_api.settings')

application = get_wsgi_application()
