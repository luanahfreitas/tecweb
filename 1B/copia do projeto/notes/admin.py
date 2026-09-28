# =============================================================================
# notes/admin.py — registra os models no painel localhost:8000/admin
# Lá dá para ver/criar/editar/apagar sem escrever página nenhuma (ótimo para testar).
# Login: python manage.py createsuperuser
# Model novo? → importar aqui e registrar também.
# 📖 README_1B.md → Parte 1 → "Admin"
# =============================================================================
from django.contrib import admin
from .models import Note, Tag      # o ponto = "deste mesmo app"


admin.site.register(Note)
admin.site.register(Tag)
