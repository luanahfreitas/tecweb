# getit/asgi.py — igual ao wsgi.py, para servidores assíncronos. Não usamos. (🔹 só reconhecer)
"""
ASGI config for getit project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "getit.settings")

application = get_asgi_application()
