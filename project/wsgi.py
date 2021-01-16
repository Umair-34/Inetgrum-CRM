import logging
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
log = logging.getLogger(__name__)

application = get_wsgi_application()
