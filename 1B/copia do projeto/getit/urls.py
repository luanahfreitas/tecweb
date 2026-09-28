"""
URL configuration for getit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# =============================================================================
# getit/urls.py — ROTAS DO PROJETO (🔹 só reconhecer)
# Primeiro arquivo de rotas lido (ROOT_URLCONF). Só distribui:
#   /admin/  → painel do Django
#   o resto  → notes/urls.py (é LÁ que se adicionam rotas novas)
# 📖 README_1B.md → Parte 0 → "Caminho de uma requisição"
# =============================================================================
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),        # localhost:8000/admin (login: createsuperuser)
    path('', include('notes.urls')),      # todo o resto → notes/urls.py
]
