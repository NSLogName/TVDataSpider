# encoding: utf-8
"""
WSGI config for TVDataSpider project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TVDataSpider.settings")

application = get_wsgi_application()

from TVDataSpider.apschedulerJob import Scheduler
scheduler = Scheduler()
