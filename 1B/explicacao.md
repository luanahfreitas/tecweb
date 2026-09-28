# Projeto 1B — Get-it em Django

> ## 🚨 AVISO — FALAR COM A PROFESSORA ANTES DA PROVA
> O Projeto 1B está rodando na **porta 8000** (orientação da professora por causa de um erro).

Guia de consulta para a prova. Cada parte segue a ordem do enunciado.

📖 Enunciado: https://barbaratieko.github.io/tecweb/projetos/projeto1/projeto1b/
📖 Handout Django: https://barbaratieko.github.io/tecweb/aulas/04-django/
📖 Documentação Django: https://docs.djangoproject.com/en/stable/

## 📑 Sumário

- **[Como rodar (versão da prova)](#como-rodar-versão-da-prova)**
- **[Parte 0 — A base do Django](#parte-0--a-base-do-django)**
  - [O que é o Django](#o-que-é-o-django)
  - [🔑 O 1A traduzido para o Django](#-o-1a-traduzido-para-o-django)
  - [Estrutura de pastas: projeto × app](#estrutura-de-pastas-projeto--app)
  - [🔸 Caminho de uma requisição](#-caminho-de-uma-requisição)
  - [Onde fica a porta 8000?](#onde-fica-a-porta-8000)
  - [Comandos básicos](#comandos-básicos)
  - [✅ Na prova](#-na-prova)
  - [⚠ Pegadinhas](#-pegadinhas)
- **[Parte 1 — Tarefa 1: CRUD em Django](#parte-1--tarefa-1-crud-em-django)**
  - [O que a tarefa pedia](#o-que-a-tarefa-pedia)
  - [1. Model — notes/models.py](#1-model--notesmodelspy)
  - [2. ORM — mexer no banco sem SQL](#2-orm--mexer-no-banco-sem-sql)
  - [3. Views — notes/views.py](#3-views--notesviewspy)
  - [4. Rotas — notes/urls.py](#4-rotas--notesurlspy)
  - [5. Templates — notes/templates/notes/](#5-templates--notestemplatesnotes)
  - [Fluxo completo](#fluxo-completo)
  - [✅ Na prova](#-na-prova-1)
  - [⚠ Pegadinhas](#-pegadinhas-1)
- **[Parte 2 — Tarefa 2: Tags e relações entre tabelas](#parte-2--tarefa-2-tags-e-relações-entre-tabelas)**
  - [O que a tarefa pedia](#o-que-a-tarefa-pedia-1)
  - [🔑 Qual relação usar?](#-qual-relação-usar)
- **[⭐ MANY-TO-ONE (ForeignKey) — PASSO A PASSO](#-many-to-one-foreignkey--passo-a-passo)**
  - [Passo 1 — Model do lado "um" (notes/models.py)](#passo-1--model-do-lado-um-notesmodelspy)
  - [Passo 2 — ForeignKey no lado "muitos"](#passo-2--foreignkey-no-lado-muitos)
  - [Passo 3 — Migrations](#passo-3--migrations)
  - [Passo 4 — Admin (opcional, ajuda a testar)](#passo-4--admin-opcional-ajuda-a-testar)
  - [Passo 5 — Página do lado "um" (cadastrar + listar pastas)](#passo-5--página-do-lado-um-cadastrar--listar-pastas)
  - [Passo 6 — Página do lado "muitos" com select (menu suspenso)](#passo-6--página-do-lado-muitos-com-select-menu-suspenso)
  - [Passo 7 — Ligar e ler a relação](#passo-7--ligar-e-ler-a-relação)
  - [✅ Checklist Many-to-one](#-checklist-many-to-one)
- **[MANY-TO-MANY (ManyToManyField) — o meu projeto (tags)](#many-to-many-manytomanyfield--o-meu-projeto-tags)**
  - [Model](#model)
  - [View index — criar nota com tags](#view-index--criar-nota-com-tags)
  - [View edit — trocar as tags](#view-edit--trocar-as-tags)
  - [Métodos](#métodos)
  - [Páginas de tags](#páginas-de-tags)
  - [Templates](#templates)
  - [Comparação lado a lado](#comparação-lado-a-lado)
  - [⚠ Pegadinhas](#-pegadinhas-2)
- **[Parte 3 — Tarefa 3: PostgreSQL com Docker (🔹 só reconhecer)](#parte-3--tarefa-3-postgresql-com-docker--só-reconhecer)**
  - [O que a tarefa pedia](#o-que-a-tarefa-pedia-2)
  - [Conceitos](#conceitos)
  - [Comando usado para ligar o banco](#comando-usado-para-ligar-o-banco)
  - [settings.py (commit "Tarefa 3 - PostgreSQL")](#settingspy-commit-tarefa-3---postgresql)
- **[Parte 4 — Tarefa 4: Deploy no Render (🔹 só reconhecer)](#parte-4--tarefa-4-deploy-no-render--só-reconhecer)**
  - [O que a tarefa pedia](#o-que-a-tarefa-pedia-3)
  - [A ideia](#a-ideia)
  - [requirements.txt — o que entrou](#requirementstxt--o-que-entrou)
  - [settings.py (commit "Deploy")](#settingspy-commit-deploy)
  - [No painel do Render (típico)](#no-painel-do-render-típico)
  - [⚠ Limitações do plano gratuito do Render](#-limitações-do-plano-gratuito-do-render)
  - [Resumo para explicar](#resumo-para-explicar)

---

## Como rodar (versão da prova)

```bash
cd "projeto 1B"              # aspas por causa do espaço no nome
source env/bin/activate      # ativa o ambiente virtual (Mac)
python manage.py runserver
```

- Abrir **http://localhost:8000** (porta **8000**, não 8080 como no 1A)
- Mudou arquivo `.py`? O `runserver` **reinicia sozinho** (diferente do 1A)
- Parar o servidor: **Ctrl+C**
- Comandos completos (venv, migrações, deploy...) → README de atalhos

> ⚠ Não renomear nem mover a pasta `projeto 1B`: o ambiente virtual `env` guarda o caminho onde foi criado.

### Diferença entre a pasta da prova e o repositório

Só o `getit/settings.py` muda (pedido da professora):

| | Repositório (deploy) | Pasta da prova |
|---|---|---|
| `DEBUG` | `False` | `True` → erros aparecem completos no navegador e no terminal |
| Banco | PostgreSQL do Render | SQLite local (`db.sqlite3`) |

`makemigrations` / `migrate` na prova alteram só o `db.sqlite3` local.

---

# Parte 0 — A base do Django

📖 Handout Django partes 1 e 2: https://barbaratieko.github.io/tecweb/aulas/04-django/parte1/
📖 Docs URLs: https://docs.djangoproject.com/en/stable/topics/http/urls/

## O que é o Django

No 1A o servidor foi escrito na mão (socket, rota, resposta, SQL).
O Django é um **framework**: já faz tudo isso, e você só escreve o que é específico do site.

## 🔑 O 1A traduzido para o Django

| No 1A (na mão) | No 1B (Django) | Arquivo |
|---|---|---|
| `if/elif` do `servidor.py` | lista de `path(...)` | `urls.py` |
| funções que recebem `request` (string) | funções que recebem `request` (objeto) | `views.py` |
| `extract_route` + `split('/')[-1]` para o id | `<int:note_id>` na rota → chega pronto como parâmetro | `urls.py` |
| montar `params` a partir do corpo do POST | `request.POST.get('titulo')` | `views.py` |
| `request.startswith('POST')` | `request.method == 'POST'` | `views.py` |
| `load_template(...).format(...)` + `build_response(body=...)` | `render(request, 'template.html', {...})` | `views.py` |
| `build_response(code=303, ..., headers='Location: /')` | `redirect('index')` | `views.py` |
| buracos `{nome}` no HTML | `{{ nome }}`, `{% for %}`, `{% url %}`... | `templates/` |
| `database.py` com SQL à mão | **models** (classes) + **ORM** (`Note.objects.all()`) | `models.py` |
| `CREATE TABLE` / apagar `banco.db` | **migrations** (`makemigrations` + `migrate`) | `migrations/` |
| `python servidor.py` (porta 8080) | `python manage.py runserver` (porta 8000) | `manage.py` |

## Estrutura de pastas: projeto × app

```
projeto 1B/
├── manage.py            ← "controle remoto": todos os comandos passam por ele
├── requirements.txt     ← bibliotecas para instalar
├── db.sqlite3           ← banco local (prova)
├── env/                 ← ambiente virtual
├── getit/               ← o PROJETO (configurações gerais)
│   ├── settings.py      ← apps instalados, banco, DEBUG, hosts...
│   └── urls.py          ← rotas principais: manda tudo para o app notes
└── notes/               ← o APP (o seu código de verdade)
    ├── models.py        ← tabelas (Note, Tag)
    ├── views.py         ← funções de cada página
    ├── urls.py          ← rotas do app
    ├── admin.py         ← registra os models no /admin
    ├── migrations/      ← histórico de mudanças no banco (gerado pelo Django)
    ├── templates/notes/ ← HTMLs
    └── static/notes/    ← CSS, JS, imagens
```

> Quase tudo o que se escreve na prova fica dentro de `notes/`.

### 🔹 Só reconhecer

- `getit/settings.py` → `INSTALLED_APPS` tem `"notes.apps.NotesConfig"` (é assim que o Django sabe que o app existe)
- `getit/urls.py`, `asgi.py`, `wsgi.py`, `manage.py`, `apps.py`, `tests.py`

## 🔸 Caminho de uma requisição

Exemplo: abrir `localhost:8000/edit/3/`

**1. `getit/urls.py`** (projeto) — decide para onde mandar:

```python
urlpatterns = [
    path("admin/", admin.site.urls),        # /admin/ → painel do Django
    path('', include('notes.urls')),        # todo o resto → notes/urls.py
]
```

**2. `notes/urls.py`** (app) — procura o `path` que bate:

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<int:note_id>/', views.delete, name='delete'),
    path('edit/<int:note_id>/', views.edit, name='edit'),
    path('tags/', views.tags, name='tags'),
    path('tags/<int:tag_id>/', views.tag_detail, name='tag_detail'),
]
```

`<int:note_id>` pega o `3`, converte para número e entrega para a view.

**3.** Chama `views.edit(request, note_id=3)`

**4.** A view busca a nota e devolve `render(...)` → o Django manda o HTML.

### Anatomia de um `path`

```python
path('edit/<int:note_id>/', views.edit, name='edit')
#     ↑ rota               ↑ função     ↑ apelido (usado no {% url 'edit' note.id %})
```

| Parte | Para que serve |
|---|---|
| rota | o que vem depois de `localhost:8000/` (termina com `/`) |
| `<int:nome>` | pedaço variável; vira parâmetro da view com esse **mesmo nome** |
| função da view | `views.nome_da_funcao` (sem parênteses!) |
| `name` | apelido para gerar links nos templates e usar no `redirect` |

## Onde fica a porta 8000?

**Em nenhum arquivo do projeto.** No 1A a porta estava no `servidor.py` (`SERVER_PORT = 8080`).
No Django, quem define é o comando `runserver`, usando o padrão escrito no código do próprio Django:

```
env/lib/python3.12/site-packages/django/core/management/commands/runserver.py
    default_addr = "127.0.0.1"    ← o localhost
    default_port = "8000"         ← a porta
```

(Nunca editar nada dentro de `env/`: é o código das bibliotecas instaladas.)

| Situação | Resultado |
|---|---|
| `python manage.py runserver` | sempre `localhost:8000` |
| `python manage.py runserver 8080` | `localhost:8080` |
| 8000 já ocupada (outro runserver aberto) | `Error: That port is already in use.` → Ctrl+C no outro terminal ou usar outra porta |

1A (8080) e 1B (8000) podem rodar **ao mesmo tempo** em dois terminais.

**`ALLOWED_HOSTS`** (`getit/settings.py`) tem `'localhost'`, mas **não define** a porta nem o endereço:
é só a lista de endereços pelos quais o Django aceita ser acessado (segurança do deploy).
Com `DEBUG = True`, `localhost` já é aceito automaticamente.

## Comandos básicos

| Comando | O que faz |
|---|---|
| `python manage.py runserver` | liga o servidor em `localhost:8000` |
| `python manage.py makemigrations` | lê o `models.py` e gera arquivo de migração com as mudanças |
| `python manage.py migrate` | aplica as migrações no banco (cria/altera tabelas) |
| `python manage.py createsuperuser` | cria login para o `/admin` |

## ✅ Na prova

- Escrever linhas `path(...)` no **`notes/urls.py`**
- Rodar `makemigrations` e `migrate` depois de mexer no `models.py`
- `settings.py` e `getit/urls.py` → só reconhecer

## ⚠ Pegadinhas

1. **Rota termina com `/`**: `path('perguntas/', ...)`. Acessar sem a barra redireciona para a com barra.
2. **Nome no `<int:note_id>` = nome do parâmetro da view** (`def edit(request, note_id)`). Diferente → erro.
3. **`views.funcao` sem parênteses** no `path` (é a função, não a chamada).
4. **`name` repetido ou errado** → `{% url %}` e `redirect` quebram (`NoReverseMatch`).
5. Porta **8000**, não 8080.
6. Terminal: `cd "projeto 1B"` **com aspas**.

---

# Parte 1 — Tarefa 1: CRUD em Django

📖 Handout Django parte 3 (banco): https://barbaratieko.github.io/tecweb/aulas/04-django/parte3/
📖 Handout Django parte 4 (admin): https://barbaratieko.github.io/tecweb/aulas/04-django/parte4/
📖 Handout Django parte 5 (templates): https://barbaratieko.github.io/tecweb/aulas/04-django/parte5/
📖 Handout Django parte 6 (formulários/POST): https://barbaratieko.github.io/tecweb/aulas/04-django/parte6/
📖 Docs campos: https://docs.djangoproject.com/en/stable/ref/models/fields/
📖 Docs ORM: https://docs.djangoproject.com/en/stable/topics/db/queries/
📖 Docs tags de template: https://docs.djangoproject.com/en/stable/ref/templates/builtins/

## O que a tarefa pedia

Refazer no Django o **CRUD** do 1A com o mesmo CSS:
**C**riar · **R**ead (listar) · **U**pdate (editar) · **D**elete (apagar).

(As linhas de **tags** do código ficam na Parte 2.)

---

## 1. Model — `notes/models.py`

Uma classe faz tudo: define o formato da nota **e** vira a tabela do banco.

```python
from django.db import models

class Note(models.Model):                       # herdar de models.Model = virar tabela
    title = models.CharField(max_length=200)    # obrigatório (sem null=True)
    content = models.TextField(null=True)       # pode ficar vazio

    def __str__(self):                          # como aparece no /admin (opcional)
        return f"{self.id}. {self.title}"
```

- **`id` é criado sozinho** (não escrever)
- Cada atributo = uma coluna

| Campo | Guarda | Detalhe |
|---|---|---|
| `CharField(max_length=N)` | texto curto | `max_length` **obrigatório** |
| `TextField()` | texto longo, sem limite | |
| `BooleanField()` | verdadeiro/falso | |
| `IntegerField()` | número inteiro | |
| `ForeignKey(...)` / `ManyToManyField(...)` | ligação com outra tabela | Parte 2 |

| Opção | Significado |
|---|---|
| (nada) | campo **obrigatório** (não pode ser nulo) |
| `null=True` | pode ficar vazio **no banco** |
| `blank=True` | pode ficar vazio **em formulários** (ex: no /admin) |
| `unique=True` | não pode repetir |
| `default=valor` | valor padrão |

### Migrations (o "CREATE TABLE" automático)

```bash
python manage.py makemigrations    # lê o models.py → gera arquivo de migração
python manage.py migrate           # aplica no banco
```

> 🔑 **Mexeu no `models.py` → `makemigrations` → `migrate`.** Sempre os dois.

| Arquivo em `migrations/` | O que mudou |
|---|---|
| `0001_initial.py` | criou `Note` só com `title` |
| `0002_note_content.py` | adicionou `content` |
| `0003_tag_note_tags.py` | criou `Tag` + ligação com `Note` (Parte 2) |

Nunca editar esses arquivos. O `migrate` altera a tabela **sem perder dados**
(no 1A precisava apagar o `banco.db`).

### Admin — `notes/admin.py`

```python
from django.contrib import admin
from .models import Note, Tag

admin.site.register(Note)       # aparece em localhost:8000/admin
admin.site.register(Tag)
```

Login com `python manage.py createsuperuser`.

---

## 2. ORM — mexer no banco sem SQL

| O que quer | ORM (Django) | No 1A |
|---|---|---|
| todas | `Note.objects.all()` | `db.get_all()` |
| uma pelo id | `Note.objects.get(id=3)` | `db.get(3)` |
| criar | `Note.objects.create(title=..., content=...)` | `db.add(Note(...))` |
| alterar | `nota.title = 'novo'` + `nota.save()` | `db.update(nota)` |
| apagar | `nota.delete()` | `db.delete(3)` |
| filtrar | `Note.objects.filter(title='Mercado')` | — |
| ordenar | `Note.objects.all().order_by('title')` (`'-title'` = decrescente) | `ORDER BY` |

`.create()` e `.save()` já salvam (sem `commit`).

---

## 3. Views — `notes/views.py`

```python
from django.shortcuts import render, redirect
from .models import Note, Tag
```

### 🔑 Tradução 1A → Django

| 1A | Django |
|---|---|
| `request.startswith('POST')` | `request.method == 'POST'` |
| montar `params` (split `&`, `unquote_plus`...) | `request.POST.get('titulo')` (`'titulo'` = `name` do HTML) |
| `load_template(...).format(...)` + `build_response(body=...)` | `render(request, 'notes/x.html', {...})` |
| `build_response(code=303, ..., headers='Location: /')` | `redirect('index')` (`'index'` = **`name`** do path) |
| `int(route.split('/')[-1])` | parâmetro `note_id` (vem do `<int:note_id>`, já é número) |

### `render` — usado em toda página

```python
render(request, 'notes/index.html', {'notes': notes})
#      ↑ sempre  ↑ template          ↑ contexto: cada CHAVE vira variável no template
```

Chave `'notes'` → no HTML: `{{ notes }}` / `{% for note in notes %}`

### `index` — listar (GET) e criar (POST)

```python
def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        note = Note.objects.create(title=title, content=content)
        # (tags → Parte 2)
        return redirect('index')

    notes = Note.objects.all()
    return render(request, 'notes/index.html', {'notes': notes})
```

### `delete` — apagar (direto, sem confirmação)

```python
def delete(request, note_id):          # note_id vem do <int:note_id>
    note = Note.objects.get(id=note_id)
    note.delete()
    return redirect('index')
```

### `edit` — GET mostra, POST salva

```python
def edit(request, note_id):
    note = Note.objects.get(id=note_id)          # busca 1 vez: as duas metades usam
    if request.method == 'POST':
        note.title = request.POST.get('titulo')
        note.content = request.POST.get('detalhes')
        note.save()
        # (tags → Parte 2)
        return redirect('index')
    else:
        return render(request, 'notes/edit.html', {'note': note})
```

### ✅ Molde de view com formulário (Django)

```python
def minha_view(request):
    if request.method == 'POST':
        campo = request.POST.get('name_do_input')
        Modelo.objects.create(campo=campo)
        return redirect('name_do_path')
    itens = Modelo.objects.all()
    return render(request, 'notes/pagina.html', {'itens': itens})
```

---

## 4. Rotas — `notes/urls.py`

```python
path('', views.index, name='index'),
path('delete/<int:note_id>/', views.delete, name='delete'),
path('edit/<int:note_id>/', views.edit, name='edit'),
```

(Anatomia do `path` → Parte 0.)

---

## 5. Templates — `notes/templates/notes/`

Pasta com `notes` duas vezes: o Django procura em `templates/` de **todos** os apps;
a subpasta com o nome do app evita conflito. Por isso no `render`: `'notes/index.html'`.
(Mesma lógica em `notes/static/notes/`.)

| Marcação | Serve para | Exemplo |
|---|---|---|
| `{{ variavel }}` | **mostrar** valor | `{{ note.title }}` |
| `{% comando %}` | **fazer** algo | `{% for %}`, `{% if %}`, `{% url %}`, `{% static %}` |

### Tags de template mais usadas

| Tag | O que faz |
|---|---|
| `{% extends "notes/base.html" %}` | usa o base como molde (**1ª linha**) |
| `{% block content %}...{% endblock %}` | conteúdo que entra no buraco do base |
| `{% load static %}` | libera o `{% static %}` (no topo de cada template que usa) |
| `{% static 'notes/getit.css' %}` | caminho do arquivo estático → `/static/notes/getit.css` |
| `{% url 'edit' note.id %}` | link pelo **`name`** do path → `/edit/3/` |
| `{% csrf_token %}` | **obrigatório em todo `<form method="post">`** |
| `{% for x in lista %}...{% endfor %}` | loop |
| `{% if cond %}...{% else %}...{% endif %}` | condição |

### `base.html` — molde comum (head, CSS, barra do topo)

```html
{% load static %}
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Get-it</title>
    <link rel="stylesheet" href="{% static 'notes/getit.css' %}" />
  </head>
  <body>
    <div class="appbar">
      <img src="{% static 'notes/img/logo-getit.png' %}" class="logo" />
      <a href="{% url 'tags' %}">Tags</a>
    </div>
    <main class="container">
      {% block content %} {% endblock %}     <!-- cada página preenche aqui -->
    </main>
    <script src="{% static 'notes/getit.js' %}"></script>
  </body>
</html>
```

> `{% static %}` sempre gera caminho com `/` no começo → sem a pegadinha de rota com barra do 1A.

### `index.html`

```html
{% extends "notes/base.html" %}
{% load static %}

{% block content %}
<form class="form-card" method="post">          <!-- sem action → POST / → index -->
  {% csrf_token %}
  <input class="form-card-title" type="text" name="titulo" placeholder="Título" />
  <textarea class="autoresize" name="detalhes" placeholder="Detalhes"></textarea>
  <button class="btn" type="submit">Salvar</button>
</form>

<div class="card-container">
  {% for note in notes %}                      <!-- notes = chave do render -->
  <div class="card">
    <h3 class="card-title">{{ note.title }}</h3>
    <a class="card-edit" href="{% url 'edit' note.id %}">
      <img src="{% static 'notes/img/edit.png' %}" alt="Editar" />
    </a>
    <a class="card-delete" href="{% url 'delete' note.id %}">
      <img src="{% static 'notes/img/lixeira.png' %}" alt="Excluir" />
    </a>
    <p>{{ note.content }}</p>
  </div>
  {% endfor %}
</div>
{% endblock %}
```

### `edit.html`

```html
{% extends "notes/base.html" %}

{% block content %}
<form class="edit-card" method="post">          <!-- sem action → POST /edit/3/ -->
  {% csrf_token %}
  <input class="edit-card-title" type="text" name="titulo" value="{{ note.title }}" />
  <textarea class="edit-card-content" name="detalhes">{{ note.content }}</textarea>
  <a class="btn btn-secondary" href="{% url 'index' %}">Voltar</a>
  <button class="btn" type="submit">Salvar</button>
</form>
{% endblock %}
```

---

## Fluxo completo

| Ação | Requisição | View | Resposta |
|---|---|---|---|
| Abrir home | `GET /` | `index` (GET) | `render` com a lista |
| Criar | `POST /` | `index` (POST) → `create` | `redirect('index')` |
| Lápis | `GET /edit/3/` | `edit` (GET) | `render` do form preenchido |
| Salvar | `POST /edit/3/` | `edit` (POST) → `save` | `redirect('index')` |
| Lixeira | `GET /delete/3/` | `delete` | `redirect('index')` |

## ✅ Na prova

Praticamente tudo desta parte: model + migrations, view com duas metades
(`request.POST.get`, `create`, `redirect`), `render` com dicionário,
template com `{% extends %}`, `{% csrf_token %}`, `{% for %}` e `{{ }}`.

## ⚠ Pegadinhas

1. **Sem `{% csrf_token %}`** no form POST → **403 Forbidden**.
2. **Mexeu no model e não rodou `makemigrations` + `migrate`** → `no such table` / `no such column`.
3. **`name` do HTML ≠ `request.POST.get(...)`** → vem `None` (não dá erro na hora; quebra no `create` se o campo for obrigatório).
4. **`redirect` e `{% url %}` usam o `name` do path**, não a rota → nome errado = `NoReverseMatch`.
5. **`{% extends %}` não é a 1ª linha** → erro de template.
6. **Esqueceu `{% load static %}`** → erro `Invalid block tag 'static'`.
7. **`Note.objects.get(id=999)`** com id inexistente → `DoesNotExist` (página amarela com `DEBUG = True`).
8. **Chave do dicionário do `render` ≠ nome usado no template** → não dá erro, só aparece vazio.

---

# Parte 2 — Tarefa 2: Tags e relações entre tabelas

📖 Enunciado tarefa 2: https://barbaratieko.github.io/tecweb/projetos/projeto1/projeto1b/tarefa02/
📖 Enunciado Many-to-many (A+): https://barbaratieko.github.io/tecweb/projetos/projeto1/projeto1b/tags-many-to-many/
📖 Exemplo many-to-one da professora: https://github.com/BarbaraTieko/Django-many-to-one-example
📖 Docs Many-to-one: https://docs.djangoproject.com/en/stable/topics/db/examples/many_to_one/
📖 Docs Many-to-many: https://docs.djangoproject.com/en/stable/topics/db/examples/many_to_many/
📖 `<select>`: https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/select

## O que a tarefa pedia

Tags nas notas + página com todas as tags + página com as notas de uma tag.
**A+**: fazer com **Many-to-many**.

---

## 🔑 Qual relação usar?

A pergunta é sempre: **quantos de um lado se ligam a quantos do outro?**

| O enunciado diz... | Relação | Campo | Onde fica |
|---|---|---|---|
| "uma X tem **várias** Y, mas uma Y tem **só uma** X" | **Many-to-one** | `ForeignKey` | no model do lado **"muitos"** (Y) |
| "várias dos **dois** lados" | **Many-to-many** | `ManyToManyField` | em **um** dos dois |

> 🧠 **A `ForeignKey` fica no lado que só pode escolher UMA.**
> "Uma nota fica em uma pasta" → a **nota** escolhe uma pasta → `pasta` fica na **Note**.

### Como o banco guarda

**Many-to-one** → uma coluna `<nome>_id` no lado "muitos":

```
Pasta                 Note
id | nome             id | title     | pasta_id
1  | Faculdade        1  | Prova     | 1
2  | Casa             2  | Trabalho  | 1
                      3  | Mercado   | 2
```

**Many-to-many** → uma tabela escondida com os pares (o Django cria sozinho):

```
Note                  Tag                   notes_note_tags
id | title            id | name             note_id | tag_id
1  | Prova            1  | faculdade        1       | 1
2  | Mercado          2  | urgente          1       | 2
                                            2       | 2
```

---

# ⭐ MANY-TO-ONE (`ForeignKey`) — PASSO A PASSO

> Exemplo: **Pasta** (lado "um") e **Note** (lado "muitos").
> Uma pasta tem várias notas; cada nota tem uma pasta só.
> ✅ Todo o código desta seção foi testado no Django 6.1 com o projeto 1B.

## Passo 1 — Model do lado "um" (`notes/models.py`)

```python
class Pasta(models.Model):
    nome = models.CharField(max_length=100)       # obrigatório (sem null=True)

    def __str__(self):                            # como aparece no /admin
        return self.nome
```

> ⚠ Tem que vir **ANTES** da classe que aponta para ela.
> (Ou usar o nome entre aspas: `models.ForeignKey('Pasta', ...)`.)

## Passo 2 — `ForeignKey` no lado "muitos"

```python
class Note(models.Model):
    title = models.CharField(max_length=200)
    pasta = models.ForeignKey(Pasta, on_delete=models.CASCADE)
    #       ↑ para qual model     ↑ OBRIGATÓRIO
```

| `on_delete=` | Ao apagar a pasta, as notas dela... |
|---|---|
| `models.CASCADE` | **são apagadas junto** (padrão da professora) |
| `models.SET_NULL` | ficam sem pasta (**precisa** `null=True` no campo) |
| `models.PROTECT` | impedem apagar a pasta |

## Passo 3 — Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### ⚠ Se o model do lado "muitos" JÁ TEM LINHAS no banco

O `makemigrations` para e pergunta:

```
It is impossible to add a non-nullable field 'pasta' to note without specifying a default.
This is because the database needs something to populate existing rows.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.
Select an option:
```

**O que fazer (testado):**

| Situação | Resposta |
|---|---|
| **Já existe** uma pasta cadastrada (ex: id 1) | digitar `1` (opção) → Enter → digitar `1` (id da pasta) → Enter |
| **Não existe** nenhuma pasta ainda (ex: model criado agora) | digitar `2` (sair), colocar `null=True` na ForeignKey e rodar `makemigrations` de novo |

```python
pasta = models.ForeignKey(Pasta, on_delete=models.CASCADE, null=True)
```

> ❌ **Opção 1 com um id que NÃO existe** → o `makemigrations` passa, mas o `migrate` quebra com
> `IntegrityError: ... has an invalid foreign key: notes_note.pasta_id contains a value '1' that does not have a corresponding value in notes_pasta.id`
>
> **Como consertar:** apagar o arquivo de migração novo que ficou pendente (o último em `migrations/`,
> que aparece com `[ ]` em `python manage.py showmigrations notes`), colocar `null=True` e rodar
> `makemigrations` + `migrate` de novo.

## Passo 4 — Admin (opcional, ajuda a testar)

```python
# notes/admin.py
from .models import Note, Tag, Pasta
admin.site.register(Pasta)
```

## Passo 5 — Página do lado "um" (cadastrar + listar pastas)

**`notes/urls.py`**
```python
path('pastas/', views.pastas, name='pastas'),
```

**`notes/views.py`**
```python
from .models import Note, Tag, Pasta

def pastas(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        Pasta.objects.create(nome=nome)
        return redirect('pastas')                    # volta para a mesma página
    todas = Pasta.objects.all()
    return render(request, 'notes/pastas.html', {'pastas': todas})
```

**`notes/templates/notes/pastas.html`** (HTML válido, sem CSS)
```html
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Pastas</title></head>
<body>
  <h1>Pastas</h1>
  <form method="post">
    {% csrf_token %}
    <label for="nome">Nome</label>
    <input type="text" id="nome" name="nome" />
    <button type="submit">Salvar</button>
  </form>
  <ul>
    {% for pasta in pastas %}
      <li>{{ pasta.nome }}</li>
    {% endfor %}
  </ul>
</body>
</html>
```

## Passo 6 — Página do lado "muitos" com `<select>` (menu suspenso)

**`notes/urls.py`**
```python
path('notas-pasta/', views.notas_pasta, name='notas_pasta'),
```

**`notes/views.py`**
```python
def notas_pasta(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        pasta_id = request.POST.get('pasta')                  # chega o ID escolhido: '2'
        Note.objects.create(title=titulo, pasta_id=pasta_id)  # liga pela coluna pasta_id
        return redirect('notas_pasta')
    notas = Note.objects.all()
    pastas = Pasta.objects.all()                              # ← para montar o <select>
    return render(request, 'notes/notas_pasta.html', {'notas': notas, 'pastas': pastas})
```

**`notes/templates/notes/notas_pasta.html`**
```html
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Notas por pasta</title></head>
<body>
  <form method="post">
    {% csrf_token %}
    <input type="text" name="titulo" placeholder="Título" />
    <select name="pasta">                                    <!-- name → request.POST.get('pasta') -->
      {% for pasta in pastas %}
        <option value="{{ pasta.id }}">{{ pasta.nome }}</option>
        <!--           ↑ ENVIADO (id)   ↑ MOSTRADO (nome) -->
      {% endfor %}
    </select>
    <button type="submit">Salvar</button>
  </form>
  <ul>
    {% for nota in notas %}
      <li>{{ nota.title }} (pasta: {{ nota.pasta.nome }})</li>
    {% endfor %}
  </ul>
</body>
</html>
```

Resultado testado: escolher "Casa" e salvar "Mercado" → lista mostra `Mercado (pasta: Casa)`.

### Como o `<select>` funciona

| Parte | Papel |
|---|---|
| `<select name="pasta">` | o `name` é a chave no `request.POST` |
| `<option value="{{ pasta.id }}">` | o que é **enviado** → tem que ser o **id** |
| `{{ pasta.nome }}` entre as tags | o que a pessoa **vê** |
| `{% for pasta in pastas %}` | precisa que a view mande `'pastas'` no `render` |

## Passo 7 — Ligar e ler a relação

**Ligar (criar com pasta):**

```python
Note.objects.create(title=t, pasta_id=pasta_id)   # jeito 1: pelo id (número/texto do form)

pasta = Pasta.objects.get(id=pasta_id)
Note.objects.create(title=t, pasta=pasta)         # jeito 2: pelo objeto
```

> `pasta_id=` recebe o **número**. `pasta=` recebe o **objeto**. Não misturar.

**Ler:**

| Quer | Python | Template |
|---|---|---|
| pasta de uma nota | `nota.pasta` / `nota.pasta.nome` | `{{ nota.pasta.nome }}` |
| id da pasta de uma nota | `nota.pasta_id` | `{{ nota.pasta_id }}` |
| notas de uma pasta | `pasta.note_set.all()` | `{% for n in pasta.note_set.all %}` |
| notas de uma pasta (outro jeito) | `Note.objects.filter(pasta=pasta)` | — |

> `note_set` = nome do model do lado "muitos" em **minúsculo** + `_set`.

## ✅ Checklist Many-to-one

- [ ] Model do lado "um" criado (antes do outro)
- [ ] `ForeignKey(ModeloUm, on_delete=models.CASCADE)` no lado "muitos"
- [ ] `makemigrations` (atenção à pergunta do default) + `migrate`
- [ ] View do form manda a **lista do lado "um"** no `render`
- [ ] `<select name="...">` com `<option value="{{ x.id }}">{{ x.nome }}</option>`
- [ ] View lê `request.POST.get('name_do_select')` e cria com `campo_id=...`
- [ ] `{% csrf_token %}` no form
- [ ] Testar: criar, ver na lista com `{{ obj.campo.nome }}`

---

# MANY-TO-MANY (`ManyToManyField`) — o meu projeto (tags)

## Model

```python
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)   # sem nomes repetidos

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True)
    tags = models.ManyToManyField(Tag, blank=True)         # blank=True: nota pode ficar sem tag
```

## View `index` — criar nota com tags

```python
tags_input = request.POST.get('tags', '')          # "faculdade, urgente"

note = Note.objects.create(title=title, content=content)    # 1º: criar a nota

tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]   # ['faculdade', 'urgente']
for name in tag_names:
    tag, created = Tag.objects.get_or_create(name=name)   # busca ou cria → devolve (obj, True/False)
    note.tags.add(tag)                                     # 2º: ligar
```

## View `edit` — trocar as tags

```python
note.tags.clear()                  # desliga todas (não apaga as tags)
# ...mesmo loop do index com get_or_create + add
```

## Métodos

| Método | O que faz |
|---|---|
| `note.tags.all()` | tags da nota |
| `note.tags.add(tag)` | liga |
| `note.tags.remove(tag)` | desliga uma |
| `note.tags.clear()` | desliga todas |
| `tag.note_set.all()` | notas dessa tag (inverso) |
| `Note.objects.filter(tags=tag)` | notas dessa tag |
| `Tag.objects.get_or_create(name=x)` | busca ou cria → `(objeto, criado?)` |

## Páginas de tags

```python
# urls.py
path('tags/', views.tags, name='tags'),
path('tags/<int:tag_id>/', views.tag_detail, name='tag_detail'),

# views.py
def tags(request):
    all_tags = Tag.objects.all()
    return render(request, 'notes/tags.html', {'tags': all_tags})

def tag_detail(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    notes = Note.objects.filter(tags=tag)
    return render(request, 'notes/tag_detail.html', {'tag': tag, 'notes': notes})
```

## Templates

```html
<!-- index.html: tags de cada card (SEM parênteses no .all) -->
{% for tag in note.tags.all %}
  <a href="{% url 'tag_detail' tag.id %}" class="tag-badge">#{{ tag.name }}</a>
{% endfor %}

<!-- edit.html: campo preenchido "tag1, tag2" (vírgula menos na última) -->
<input type="text" name="tags"
  value="{% for tag in note.tags.all %}{{ tag.name }}{% if not forloop.last %}, {% endif %}{% endfor %}" />

<!-- base.html: link na barra do topo -->
<a href="{% url 'tags' %}">Tags</a>
```

---

## Comparação lado a lado

| | Many-to-one (`ForeignKey`) | Many-to-many (`ManyToManyField`) |
|---|---|---|
| Exemplo | nota → **uma** pasta | nota ↔ **várias** tags |
| Campo | `pasta = models.ForeignKey(Pasta, on_delete=models.CASCADE)` | `tags = models.ManyToManyField(Tag, blank=True)` |
| Onde fica | lado "muitos" | qualquer um |
| No banco | coluna `pasta_id` | tabela escondida |
| Ligar | **no `create`**: `pasta=obj` ou `pasta_id=id` | **depois do `create`**: `nota.tags.add(tag)` |
| Ler direto | `nota.pasta` (1 objeto) | `nota.tags.all()` (vários) |
| Ler inverso | `pasta.note_set.all()` | `tag.note_set.all()` |
| No form | `<select>` com ids | texto separado por vírgula |

---

## ⚠ Pegadinhas

1. **Sem `on_delete`** na `ForeignKey` → erro em qualquer comando.
2. **ForeignKey em model com linhas** → `makemigrations` pergunta o default (ver Passo 3).
3. **Opção 1 com id que não existe** → `migrate` quebra com `IntegrityError` (ver Passo 3).
4. **`<option value="{{ pasta.nome }}">`** → a view recebe o nome, não o id → erro. **`value` = id.**
5. **View não mandou a lista para o `render`** → `<select>` vazio, sem erro.
6. **`note.tags.add()` antes de a nota existir** → erro. Primeiro `create`, depois `add`.
7. **Parênteses no template** (`note.tags.all()`) → erro. No template é `note.tags.all`.
8. **`get_or_create` devolve 2 valores** → sempre `tag, created = ...`.
9. **Nome inverso**: minúsculo + `_set` → `note_set`.
10. **`redirect` no Django dá 302** (não 303 como no 1A) — funciona igual: o navegador faz GET.
11. **Model do lado "um" depois do outro no arquivo** → `NameError`. Colocar antes ou usar aspas.

---

# Parte 3 — Tarefa 3: PostgreSQL com Docker (🔹 só reconhecer)

📖 Handout Containers e Bancos de Dados: https://barbaratieko.github.io/tecweb/aulas/05-bd/
📖 Guia WSL/Docker: https://barbaratieko.github.io/tecweb/aulas/05-bd/guia-wsl/
📖 Docs Django bancos: https://docs.djangoproject.com/en/stable/ref/databases/

> Na prova a pasta `projeto 1B` usa **SQLite**. Nada desta parte é mexido.

## O que a tarefa pedia

Trocar o SQLite por **PostgreSQL** rodando num **container Docker**.

## Conceitos

| | O que é |
|---|---|
| **SQLite** | banco que mora num **arquivo** (`db.sqlite3`). Simples, para desenvolver |
| **PostgreSQL** | **servidor** de banco: programa separado que recebe conexões (porta padrão **5432**). Usado em produção |
| **Docker** | roda programas em **containers** (caixas isoladas). Não precisa instalar o Postgres no Mac |

## Comando usado para ligar o banco

```bash
docker run --rm --name pg-docker \
  -e POSTGRES_PASSWORD=escolhaumasenha \
  -d \
  -p 5432:5432 \
  -v "$HOME/docker/volumes/postgres:/var/lib/postgresql/data" \
  postgres
```

| Pedaço | Significado |
|---|---|
| `docker run ... postgres` | cria e liga um container da imagem oficial `postgres` |
| `--rm` | apaga o container quando parar (dados ficam salvos pelo `-v`) |
| `--name pg-docker` | nome do container |
| `-e POSTGRES_PASSWORD=...` | senha do administrador do banco |
| `-d` | roda em segundo plano |
| `-p 5432:5432` | porta do Mac ↔ porta do container |
| `-v pasta_mac:pasta_container` | guarda os dados no Mac (não perde ao parar) |

## `settings.py` (commit "Tarefa 3 - PostgreSQL")

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',   # antes: django.db.backends.sqlite3
        'NAME': 'getit',          # banco
        'USER': 'getituser',      # usuário
        'PASSWORD': 'getitsenha', # senha
        'HOST': 'localhost',      # container, pela porta mapeada
        'PORT': '5432',
    }
}
```

+ `psycopg2` no `requirements.txt` (conexão Django ↔ PostgreSQL) + `python manage.py migrate` para criar as tabelas no banco novo.

> 🔑 **Models, views e templates não mudaram nada.** Com o ORM, trocar de banco é só mudar o `DATABASES`.

---

# Parte 4 — Tarefa 4: Deploy no Render (🔹 só reconhecer)

📖 Handout Deploy: https://barbaratieko.github.io/tecweb/aulas/06-deploy/
📖 Projeto exemplo de deploy da professora: https://github.com/BarbaraTieko/tecweb-projeto-exemplo
📖 Docs Django deploy checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

🌐 **Meu site:** https://tecweb-2026-2-projeto1b-so8f.onrender.com

## O que a tarefa pedia

Publicar o site e colocar o link no `README.md` do repositório.

## A ideia

`runserver` é só para desenvolver. No deploy, o **Render** pega o código do GitHub, instala as
dependências e roda o site num servidor dele, com um PostgreSQL também dele.

## `requirements.txt` — o que entrou

| Biblioteca | Para quê |
|---|---|
| `gunicorn` | servidor de produção (substitui o `runserver`) |
| `whitenoise` | serve CSS/JS/imagens em produção |
| `dj-database-url` | lê o banco num formato de **link** |
| `psycopg2` | conexão com PostgreSQL |

## `settings.py` (commit "Deploy")

```python
import dj_database_url

DEBUG = False       # público: não mostrar erros detalhados (página amarela expõe o código)
ALLOWED_HOSTS = ['tecweb-2026-2-projeto1b-so8f.onrender.com', 'localhost', '127.0.0.1', '0.0.0.0']

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',      # logo depois do Security
    # ...
]

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://USUARIO:SENHA@SERVIDOR.render.com/BANCO',   # link do Render
        conn_max_age=600,
        ssl_require=not DEBUG
    )
}

STATIC_ROOT = BASE_DIR / 'staticfiles'   # onde o collectstatic junta os estáticos
```

| Configuração | Por quê |
|---|---|
| `DEBUG = False` | segurança. (Na pasta da prova: `True`, para ver os erros) |
| `ALLOWED_HOSTS` | endereços aceitos. Com `DEBUG = False`, endereço fora da lista → erro **400** |
| WhiteNoise + `STATIC_ROOT` | em produção o Django não serve CSS sozinho → `collectstatic` junta tudo em `staticfiles/` e o WhiteNoise entrega |
| `dj_database_url` | banco como **um link** (`postgresql://usuario:senha@servidor/banco`), formato do Render |

## No painel do Render (típico)

| Campo | Comando |
|---|---|
| Build | `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate` |
| Start | `gunicorn getit.wsgi` (usa o `getit/wsgi.py`, a "porta de entrada" para servidores de produção) |

## ⚠ Limitações do plano gratuito do Render

- O site **"dorme"** sem acesso → primeiro carregamento demora (~1 min)
- O **PostgreSQL gratuito expira 30 dias após criado** (o meu: criado 15/09 → ~15/10)
- Não afeta a prova (SQLite local)

## Resumo para explicar

- **Tarefa 3**: SQLite → PostgreSQL mudando **só o `DATABASES`** (ORM) + `migrate`
- **Tarefa 4**: `DEBUG = False`, `ALLOWED_HOSTS`, WhiteNoise, `dj_database_url`, `gunicorn`, link no README