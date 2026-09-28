# notes/apps.py — configuração do app notes (🔹 só reconhecer)
# NotesConfig é o que aparece no INSTALLED_APPS do settings.py: "notes.apps.NotesConfig"
from django.apps import AppConfig


class NotesConfig(AppConfig):
    name = "notes"
