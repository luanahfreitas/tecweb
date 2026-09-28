# Create your models here.
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True)
    tags = models.ManyToManyField(Tag, blank=True)


    def __str__(self):
        return f"{self.id}. {self.title}"


# [SIMULADO 3.4] ✅ model Categoria com um campo nome obrigatório (sem null=True)
# 📖 README_SIMULADO → "Quando pedirem outro cadastro completo"
# ⚠ Categoria vem ANTES de Pergunta porque a ForeignKey da Pergunta usa o nome Categoria
class Categoria(models.Model):
    # ⚠ CharField() sem max_length funciona no Django 6.1 + SQLite (testado), mas o padrão
    #   dos handouts é com max_length (em outros bancos/versões dá erro). Sugestão:
    #   nome = models.CharField(max_length=100)
    #   (se mudar: makemigrations + migrate)
    nome = models.CharField()

# [SIMULADO 3.1] ✅ model Pergunta: exatamente os 2 campos pedidos (o id é automático, não conta)
class Pergunta(models.Model):
    # ✅ TextField = "sem limite de caracteres" · null=False = "não pode ser nulo" (é o padrão)
    enunciado = models.TextField(null=False)
    # ✅ BooleanField = verdadeiro/falso
    resposta_correta = models.BooleanField(null=False)
    # [SIMULADO 3.5] ✅ many-to-one: a ForeignKey fica no lado "muitos" (a pergunta escolhe UMA categoria)
    # on_delete obrigatório · null=True porque já existiam perguntas e nenhuma categoria
    # (o makemigrations perguntou "Select an option" → escolhi 2 e coloquei null=True)
    # 📖 README_1B → Parte 2 → Passo 3
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)

