"""
WSGI config for dosMetro project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os,sys

sys.path.append('/home/server/env/dosificacion')

os.environ['DJANGO_SETTINGS_MODULE'] = "dosMetro.settings"
os.environ.setdefault("LANG", "en_US.UTF-8")
os.environ.setdefault("LC_ALL", "en_US.UTF-8")

#activate_this = 'pathToVirtualenv/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
