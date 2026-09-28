# =============================================================================
# notes/models.py — AS TABELAS DO BANCO
# Cada classe = uma tabela. Cada atributo = uma coluna. O id é criado sozinho.
# 🔑 Mexeu aqui → python manage.py makemigrations → python manage.py migrate
# 📖 README_1B.md → Parte 1 → "1. Model" e Parte 2 (relações)
# =============================================================================
from django.db import models


# -----------------------------------------------------------------------------
# Tag — o lado "outro" da relação Many-to-many
# Vem ANTES de Note porque a Note usa o nome Tag.
# (Se viesse depois, daria para escrever entre aspas: ManyToManyField('Tag'))
# -----------------------------------------------------------------------------
class Tag(models.Model):
    # CharField = texto curto → max_length é OBRIGATÓRIO
    # unique=True → não pode ter duas tags com o mesmo nome (por isso usamos get_or_create)
    name = models.CharField(max_length=100, unique=True)

    # Como a tag aparece quando vira texto (ex: na lista do /admin)
    def __str__(self):
        return self.name


# -----------------------------------------------------------------------------
# Note — a anotação
# -----------------------------------------------------------------------------
class Note(models.Model):
    # Sem null=True → campo OBRIGATÓRIO (não pode ser nulo)
    title = models.CharField(max_length=200)
    # TextField = texto longo sem limite · null=True → pode ficar vazio no banco
    content = models.TextField(null=True)
    # MANY-TO-MANY (A+): uma nota tem várias tags e uma tag está em várias notas.
    # O Django cria sozinho uma tabela escondida com os pares (note_id, tag_id).
    # blank=True → a nota pode ficar sem nenhuma tag (inclusive no /admin)
    # Usar: note.tags.all() · note.tags.add(tag) · note.tags.clear() · tag.note_set.all()
    # 📖 README_1B → Parte 2 → "MANY-TO-MANY"
    #
    # (Se fosse MANY-TO-ONE, uma nota com UMA só categoria, seria:
    #    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    #  📖 README_1B → Parte 2 → "⭐ MANY-TO-ONE — PASSO A PASSO")
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"{self.id}. {self.title}"
