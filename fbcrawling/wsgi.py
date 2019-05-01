"""
WSGI config for fbcrawling project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv


project_folder = os.path.expanduser('/media/no7kai/Data/Django/dOne/fbcrawling')
load_dotenv(os.path.join(project_folder, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fbcrawling.settings')

application = get_wsgi_application()
