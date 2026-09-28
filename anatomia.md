# Anatomia — cada pedaço das funções e tags

Para cada linha: **o que é cada parte** e **se o nome é livre** (você escolhe) ou **fixo** (tem que ser exatamente assim).

> 🔑 **Regra de ouro:** nomes livres têm que ser **iguais em todos os lugares onde aparecem**.
> Ex: o `name="titulo"` do HTML tem que ser o mesmo do `request.POST.get('titulo')`.

---

## 📑 Sumário

- **[🔗 O que tem que ser igual a quê](#-o-que-tem-que-ser-igual-a-quê)**
  - [Django (1B)](#django-1b)
  - [Projeto 1A](#projeto-1a)
- **[🩺 Erros: o que significam e o que não bateu](#-erros-o-que-significam-e-o-que-não-bateu)**
  - [Como ler a página amarela do Django](#como-ler-a-página-amarela-do-django)
- **[Django — Python](#django--python)**
  - [render](#render)
  - [redirect](#redirect)
  - [request.method](#requestmethod)
  - [request.POST.get](#requestpostget)
  - [request.POST.getlist](#requestpostgetlist)
  - [request.GET.get](#requestgetget)
  - [path](#path)
  - [include](#include)
  - [def da view](#def-da-view)
  - [class do model](#class-do-model)
  - [Campos do model](#campos-do-model)
  - [ForeignKey](#foreignkey)
  - [ManyToManyField](#manytomanyfield)
  - [Model.objects (ORM)](#modelobjects-orm)
  - [get_or_create](#get_or_create)
  - [Métodos de relação](#métodos-de-relação)
  - [admin.site.register](#adminsiteregister)
  - [imports](#imports)
- **[Django — Templates](#django--templates)**
  - [{{ variavel }}](#-variavel-)
  - [Filtros](#filtros)
  - [{% extends %} e {% block %}](#-extends--e--block-)
  - [{% load static %} e {% static %}](#-load-static--e--static-)
  - [{% url %}](#-url-)
  - [{% csrf_token %}](#-csrf_token-)
  - [{% for %}](#-for-)
  - [{% if %}](#-if-)
  - [{% now %}](#-now-)
  - [Comentários](#comentários)
- **[HTML](#html)**
  - [Estrutura da página](#estrutura-da-página)
  - [Atributos que aparecem em quase toda tag](#atributos-que-aparecem-em-quase-toda-tag)
  - [form](#form)
  - [input](#input)
  - [textarea](#textarea)
  - [select e option](#select-e-option)
  - [label](#label)
  - [button](#button)
  - [a (link)](#a-link)
  - [img](#img)
  - [Títulos, texto e listas](#títulos-texto-e-listas)
  - [link (CSS) e script (JS)](#link-css-e-script-js)
- **[Projeto 1A — Python](#projeto-1a--python)**
  - [load_template + .format](#load_template--format)
  - [build_response](#build_response)
  - [extract_route + split](#extract_route--split)
  - [request.startswith](#requeststartswith)
  - [unquote_plus e o params](#unquote_plus-e-o-params)
  - [sqlite3 no database.py](#sqlite3-no-databasepy)
  - [f-string](#f-string)
  - [random](#random)
  - [datetime e locale](#datetime-e-locale)

---

# 🔗 O que tem que ser igual a quê

> Quase todo erro de formulário/rota é **um nome que não bateu** entre dois arquivos.
> Nomes livres: você escolhe, mas **todos os lugares da mesma linha da tabela precisam ser idênticos**
> (maiúsculas, acentos, `_`, plural/singular).

## Django (1B)

| # | Isto... | ...tem que ser igual a isto | Se não bater |
|---|---|---|---|
| 1 | `name="enunciado"` no `<input>`/`<textarea>`/`<select>` (HTML) | `request.POST.get('enunciado')` (view) | vem `None` → `NOT NULL constraint failed` ao salvar |
| 2 | chave do `render`: `{'perguntas': todas}` (view) | `{% for p in perguntas %}` / `{{ perguntas }}` (template) | **sem erro**, só aparece vazio |
| 3 | `views.perguntas` no `path` (urls.py) | `def perguntas(request):` (views.py) | `AttributeError: module 'notes.views' has no attribute ...` |
| 4 | `name='perguntas'` no `path` (urls.py) | `redirect('perguntas')` (view) e `{% url 'perguntas' %}` (template) | `NoReverseMatch` |
| 5 | `<int:note_id>` no `path` | `def edit(request, note_id):` | `TypeError: edit() got an unexpected keyword argument` |
| 6 | rota no `path`: `'perguntas'` | a URL que você abre: `localhost:8000/perguntas` | página amarela **Page not found (404)** com a lista de rotas |
| 7 | `'notes/perguntas.html'` no `render` | arquivo em `notes/templates/notes/perguntas.html` | `TemplateDoesNotExist` |
| 8 | nome do campo no model: `enunciado = ...` | `create(enunciado=...)`, `filter(enunciado=...)`, `{{ p.enunciado }}` | `TypeError: Pergunta() got unexpected keyword arguments` / template vazio |
| 9 | nome da classe: `class Pergunta` | `from .models import Pergunta`, `Pergunta.objects`, `admin.site.register(Pergunta)` | `NameError: name 'Pergunta' is not defined` |
| 10 | classe `Pergunta` | inverso: `categoria.pergunta_set` (minúsculo + `_set`) · tabela `notes_pergunta` | `AttributeError` |
| 11 | ForeignKey `categoria = ...` | coluna `categoria_id` → `create(categoria_id=id)` ou `create(categoria=objeto)` | erro de tipo / campo inexistente |
| 12 | `<select name="categoria">` | `request.POST.get('categoria')` | `None` |
| 13 | `<option value="{{ c.id }}">` | o que vai no `categoria_id=` (**id**, não nome) | erro ao salvar |
| 14 | `{% block content %}` no `base.html` | `{% block content %}` na página filha | conteúdo não aparece |
| 15 | variável do `{% for p in ... %}` | usos dentro do for: `{{ p.enunciado }}` | aparece vazio |
| 16 | `<label for="enunciado">` | `id="enunciado"` do campo | só visual (clicar no texto não foca) |

### Exemplo completo com as ligações

```python
# models.py
class Pergunta(models.Model):                 # (9)
    enunciado = models.TextField()            # (8)
    resposta_correta = models.BooleanField()  # (8)

# urls.py
path('perguntas', views.perguntas, name='perguntas'),
#     (6)              (3)              (4)

# views.py
from .models import Pergunta                                   # (9)

def perguntas(request):                                        # (3)
    if request.method == 'POST':
        enunciado = request.POST.get('enunciado')              # (1)
        resposta = request.POST.get('resposta')                # (1)
        Pergunta.objects.create(enunciado=enunciado,           # (8)
                                resposta_correta=resposta == 'Verdadeiro')
        return redirect('perguntas')                           # (4)
    return render(request, 'notes/perguntas.html',             # (7)
                  {'perguntas': Pergunta.objects.all()})       # (2)
```
```html
<!-- notes/templates/notes/perguntas.html  (7) -->
<form method="post">
  {% csrf_token %}
  <input type="text" name="enunciado" />       <!-- (1) -->
  <input type="text" name="resposta" />        <!-- (1) -->
  <button type="submit">Salvar</button>
</form>
<ul>
  {% for p in perguntas %}                     <!-- (2) e (15) -->
    <li>{{ p.enunciado }} - {{ p.resposta_correta }}</li>   <!-- (8) e (15) -->
  {% endfor %}
</ul>
```

## Projeto 1A

| Isto... | ...tem que ser igual a isto | Se não bater |
|---|---|---|
| buraco `{cor}` no template | `.format(cor=...)` | `KeyError: 'cor'` (servidor cai) |
| `name="titulo"` no HTML | `params['titulo']` / `params.get('titulo')` | `KeyError` / `None` |
| `'hoje/agora'` no `elif route == ...` | URL aberta, **sem a barra do começo** | cai no 404 |
| nome no `from views import ..., hoje_agora` | `def hoje_agora(request):` e a chamada no `elif` | `ImportError` / `NameError` |
| `load_template('data.html')` | arquivo `templates/data.html` | `FileNotFoundError` |
| `action="/edit/{id}"` do form | rota tratada no `servidor.py` | 404 |

---

# 🩺 Erros: o que significam e o que não bateu

| Mensagem (2ª linha da página amarela) | Significa | Conferir |
|---|---|---|
| `NOT NULL constraint failed: notes_pergunta.enunciado` | tentou salvar `None` num campo obrigatório | `name` do HTML × `request.POST.get(...)` (1). **Campo em branco chega `''`, não `None`** → `None` = nome não bateu |
| `no such table: notes_categoria` | a tabela não existe no banco | rodar `makemigrations` + `migrate` (na pasta certa!) |
| `no such column: notes_pergunta.categoria_id` | campo novo sem migração | `makemigrations` + `migrate` |
| `NoReverseMatch: Reverse for 'x' not found` | `redirect`/`{% url %}` com name que não existe | `name=` do `path` (4) |
| `module 'notes.views' has no attribute 'x'` | o `path` aponta para função que não existe | `views.x` × `def x` (3) |
| `TemplateDoesNotExist` | template não achado | caminho no `render` × pasta (7) |
| `got an unexpected keyword argument` | parâmetro da rota ≠ parâmetro da view, ou campo inexistente no `create` | (5) ou (8) |
| `NameError: name 'X' is not defined` | faltou import | (9) |
| `Page not found (404)` (amarela, com lista de rotas) | nenhuma rota bateu | rota do `path` × URL, barra no final (6) |
| `Forbidden (403) CSRF verification failed` | form POST sem token | `{% csrf_token %}` dentro do `<form>` |
| `“Verdadeiro” value must be either True or False.` | texto num `BooleanField` | converter: `== 'Verdadeiro'` |
| `IntegrityError: NOT NULL constraint failed: ..._id` | ForeignKey vazia | `<select>` sem opções / nada cadastrado no lado "um" |
| `Invalid block tag ... 'static'` | faltou `{% load static %}` | topo do template |
| **Aparece `{ categoria.nome }` escrito na tela** | chave **simples** | no Django é `{{ }}` (chave simples é do 1A) |
| **Lista vazia, sem erro** | chave do `render` ≠ nome no template | (2) e (15) |

## Como ler a página amarela do Django

| Onde | O que mostra |
|---|---|
| **Título** (`IntegrityError at /perguntas`) | tipo do erro + a rota |
| **2ª linha** | **a mensagem** → procurar na tabela acima |
| `Request Method` | GET (abriu a página) ou POST (enviou form) |
| `Raised during` | qual view (`notes.views.perguntas`) |
| **Error during template rendering** | erro no HTML: mostra o arquivo e a **linha destacada** |
| **Traceback** | caminho do erro: procurar a linha que é **arquivo seu** (`notes/views.py`), não do `env/` |
| `▶ Local vars` | valores das variáveis naquele ponto (ex: `enunciado = None`) |
| **Request information → POST** (no final da página) | **cada `name` que o formulário mandou, com o valor** → compara com o `request.POST.get(...)` |

> 🔑 **Erro de formulário?** Desce até **Request information → POST** e compara os nomes com a view.
> Se o campo nem aparece ali: está sem `name` ou fora do `<form>`.

---

# Django — Python

## `render`

```python
return render(request, 'notes/index.html', {'notes': notes})
```

| Parte | O que é | Livre? |
|---|---|---|
| `return` | devolve a resposta para o Django mandar ao navegador | fixo |
| `render` | função do Django: junta template + dados e gera o HTML | fixo (`from django.shortcuts import render`) |
| `request` | a requisição que a view recebeu. **Sempre** o 1º argumento | fixo |
| `'notes/index.html'` | caminho do template **a partir de** `notes/templates/` | livre (tem que existir) |
| `{...}` | **contexto**: dicionário com o que o template pode usar | — |
| `'notes'` (chave) | **nome da variável no template** → `{{ notes }}`, `{% for note in notes %}` | **livre** |
| `notes` (valor) | a variável Python com os dados (ex: `Note.objects.all()`) | livre |

```python
# várias variáveis:
return render(request, 'notes/filmes.html', {'filmes': lista, 'generos': Genero.objects.all(), 'total': 3})
# sem variáveis:
return render(request, 'notes/sobre.html')
```

> Chave do dicionário ≠ nome no template → **não dá erro**, só aparece vazio.
> Template não existe → `TemplateDoesNotExist`.

## `redirect`

```python
return redirect('index')
```

| Parte | O que é | Livre? |
|---|---|---|
| `redirect` | manda o navegador ir para outra página (resposta 302 → navegador faz GET) | fixo (`from django.shortcuts import redirect`) |
| `'index'` | o **`name`** de um `path` do `urls.py` (não a rota!) | tem que existir no `urls.py` |

```python
redirect('perguntas')                  # vai para o path com name='perguntas'
redirect('edit', note_id=3)            # path com parâmetro → /edit/3/
```

> Usar depois de **todo POST** que salva/altera algo. Name errado → `NoReverseMatch`.

## `request.method`

```python
if request.method == 'POST':
```

| Parte | O que é | Livre? |
|---|---|---|
| `request.method` | método da requisição: `'GET'` ou `'POST'` | fixo |
| `== 'POST'` | "o form foi enviado?" (maiúsculo!) | fixo |

GET = abriu a página / clicou em link · POST = enviou `<form method="post">`.

## `request.POST.get`

```python
enunciado = request.POST.get('pergunta')
```

| Parte | O que é | Livre? |
|---|---|---|
| `enunciado` | variável Python que guarda o valor | **livre** |
| `request.POST` | dicionário com os dados do form enviado por POST | fixo |
| `.get(...)` | pega um valor; se não existir, devolve `None` (não dá erro) | fixo |
| `'pergunta'` | **o `name` do campo no HTML** (`<input name="pergunta">`) | tem que ser **igual ao `name`** |

```python
request.POST.get('tags', '')           # 2º argumento = valor padrão se não vier ('' em vez de None)
request.POST['titulo']                 # também funciona, mas dá ERRO (KeyError) se não vier
```

> ⚠ **Sempre texto.** Número → `int(...)`. Verdadeiro/Falso → `== 'Verdadeiro'`.
> `name` diferente → vem `None`.

## `request.POST.getlist`

```python
ids = request.POST.getlist('plataformas')     # ['1', '3']
```

Para **vários valores com o mesmo `name`** (checkboxes, `<select multiple>`). O `.get` pegaria só o último.

## `request.GET.get`

```python
busca = request.GET.get('q', '')
```

Igual ao `POST.get`, mas para dados na **URL**: `/filmes/?q=tit` → `'tit'`. Vem de `<form method="get">` (sem `csrf_token`).

## `path`

```python
path('perguntas/', views.perguntas, name='perguntas'),
```

| Parte | O que é | Livre? |
|---|---|---|
| `path(...)` | uma rota, dentro da lista `urlpatterns` | fixo |
| `'perguntas/'` | o que vem depois de `localhost:8000/`. Sem barra no começo; costume: barra no fim | **livre** (o enunciado diz qual) |
| `views.perguntas` | a **função** que atende essa rota — **sem parênteses** | tem que ser **igual ao `def`** no `views.py` |
| `name='perguntas'` | apelido da rota para `{% url %}` e `redirect` | **livre**, mas único |
| `,` no final | é um item de lista → vírgula | fixo |

```python
path('edit/<int:note_id>/', views.edit, name='edit'),
#          ↑ pedaço variável: <tipo:nome>
```

| `<int:note_id>` | O que é |
|---|---|
| `int` | tipo: só aceita número e já converte (`'3'` → `3`) · `str` = texto |
| `note_id` | nome do parâmetro → **tem que ser igual** em `def edit(request, note_id)` |

> ⚠ `views.peguntas` (erro de digitação) → `AttributeError: module 'notes.views' has no attribute 'peguntas'`.
> `'perguntas'` (sem barra) e `'perguntas/'` são rotas **diferentes**; com barra, `/perguntas` redireciona sozinho para `/perguntas/`.

## `include`

```python
path('', include('notes.urls')),       # getit/urls.py
```

Manda todas as rotas para o `urls.py` do app `notes`. Não mexer.

## `def` da view

```python
def edit(request, note_id):
```

| Parte | O que é | Livre? |
|---|---|---|
| `def` | cria uma função | fixo |
| `edit` | nome da função → usado no `path` como `views.edit` | **livre** |
| `request` | a requisição (sempre o 1º) | fixo por costume |
| `note_id` | vem do `<int:note_id>` do `path` | igual ao do `path` |

## `class` do model

```python
class Pergunta(models.Model):
    enunciado = models.TextField()

    def __str__(self):
        return self.enunciado
```

| Parte | O que é | Livre? |
|---|---|---|
| `class Pergunta` | nome do model = nome da tabela. Maiúscula, singular | **livre** (o enunciado diz qual) |
| `(models.Model)` | "isto é uma tabela do Django" | fixo |
| `enunciado =` | nome da coluna | **livre** (o enunciado diz qual) |
| `models.TextField()` | tipo da coluna | ver tabela abaixo |
| `def __str__(self)` | como o objeto aparece como texto (no /admin, no `{{ pergunta }}`) | opcional |

## Campos do model

```python
titulo = models.CharField(max_length=200, null=True, blank=True, unique=True, default='x')
```

| Tipo | Guarda | Obrigatório passar |
|---|---|---|
| `CharField` | texto curto | `max_length=` |
| `TextField` | texto longo (sem limite) | — |
| `IntegerField` | inteiro | — |
| `FloatField` | decimal | — |
| `BooleanField` | True/False | — |
| `DateField` / `DateTimeField` | data / data e hora | — |

| Opção | Significado |
|---|---|
| (nenhuma) | **obrigatório / não pode ser nulo** |
| `null=True` | pode ser vazio **no banco** |
| `blank=True` | pode ser vazio **em formulários** (/admin) |
| `unique=True` | não pode repetir |
| `default=valor` | valor padrão |
| `max_length=N` | tamanho máximo (CharField) |

## `ForeignKey`

```python
categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
```

| Parte | O que é | Livre? |
|---|---|---|
| `categoria` | nome do campo (vira coluna `categoria_id`) | **livre** |
| `models.ForeignKey` | relação **many-to-one**: cada objeto aponta para **um** do outro model | fixo |
| `Categoria` | o model do lado "um" (tem que estar **antes** no arquivo, ou `'Categoria'` entre aspas) | nome do model |
| `on_delete=` | o que fazer ao apagar a categoria — **obrigatório** | fixo |
| `models.CASCADE` | apaga os que apontavam para ela junto | `CASCADE` / `SET_NULL` (+`null=True`) / `PROTECT` |

📖 README_1B → Parte 2 → ⭐ MANY-TO-ONE

## `ManyToManyField`

```python
tags = models.ManyToManyField(Tag, blank=True)
```

| Parte | O que é |
|---|---|
| `tags` | nome do campo (plural por costume) |
| `ManyToManyField` | relação **many-to-many** (tabela escondida) |
| `Tag` | o outro model |
| `blank=True` | pode ficar sem nenhuma (no /admin) |

## `Model.objects` (ORM)

```python
Note.objects.create(title=title, content=content)
```

| Parte | O que é |
|---|---|
| `Note` | o model |
| `.objects` | o "gerente" do model: tudo que mexe na tabela começa aqui (fixo) |
| `.create(...)` | cria **e salva** uma linha |
| `title=title` | **esquerda** = nome do campo no model (fixo) · **direita** = variável com o valor (livre) |

| Código | Devolve | SQL equivalente |
|---|---|---|
| `Note.objects.all()` | todos (lista) | `SELECT *` |
| `Note.objects.get(id=3)` | **um** objeto (erro se não existir) | `WHERE id = 3` |
| `Note.objects.filter(title='x')` | lista (pode ser vazia) | `WHERE title = 'x'` |
| `.filter(title__icontains='x')` | título **contém** x (ignora maiúscula) | `LIKE` |
| `.filter(nota__gte=7)` | ≥ 7 (`gt` >, `lt` <, `lte` ≤) | |
| `.order_by('title')` / `('-title')` | ordena crescente / decrescente | `ORDER BY` |
| `Note.objects.count()` | número de linhas | `COUNT` |
| `nota.title = 'x'` + `nota.save()` | altera e salva | `UPDATE` |
| `nota.delete()` | apaga | `DELETE` |

## `get_or_create`

```python
tag, created = Tag.objects.get_or_create(name=name)
```

| Parte | O que é |
|---|---|
| `tag` | o objeto (achado ou criado) |
| `created` | `True` se criou agora, `False` se já existia |
| `, ` à esquerda | desempacota os **dois** valores devolvidos (obrigatório) |
| `name=name` | campo = valor a buscar/criar |

## Métodos de relação

```python
note.tags.add(tag)
```

| Código | Faz |
|---|---|
| `note.tags.all()` | todas as tags da nota |
| `note.tags.add(tag)` | liga uma |
| `note.tags.set([1, 2])` | troca tudo por essa lista (aceita ids) |
| `note.tags.remove(tag)` / `.clear()` | desliga uma / todas |
| `pergunta.categoria` | (ForeignKey) o objeto do lado "um" |
| `pergunta.categoria_id` | (ForeignKey) só o id |
| `categoria.pergunta_set.all()` | inverso: model em **minúsculo** + `_set` |

## `admin.site.register`

```python
admin.site.register(Pergunta)
```
Mostra o model em `localhost:8000/admin`. Precisa `from .models import Pergunta`.

## imports

```python
from django.shortcuts import render, redirect     # funções do Django
from .models import Note, Tag                      # . = "deste app" · lista os models usados
from . import views                                # (urls.py) importa o views.py deste app
from django.db import models                       # (models.py)
```

> Model novo usado na view e não importado → `NameError: name 'Pergunta' is not defined`.

---

# Django — Templates

## `{{ variavel }}`

```html
<h3>{{ note.title }}</h3>
```

| Parte | O que é |
|---|---|
| `{{ }}` | **mostra** um valor |
| `note` | variável (do `render` ou do `{% for %}`) |
| `.title` | atributo (campo do model) |

`{{ pergunta.categoria.nome }}` → segue a ForeignKey. Variável que não existe → mostra **nada** (sem erro).

## Filtros

```html
{{ filmes|length }}     {{ agora|date:"d/m/Y H:i" }}     {{ texto|upper }}     {{ x|default:"nada" }}
```
`|` aplica uma transformação ao valor.

## `{% extends %}` e `{% block %}`

```html
{% extends "notes/base.html" %}
{% block content %} ... {% endblock %}
```

| Parte | O que é |
|---|---|
| `{% extends "..." %}` | usa outro template como molde. **1ª tag do arquivo** |
| `{% block content %}` | o conteúdo entra no buraco `content` do `base.html`. `content` = nome do block (tem que ser igual ao do base) |
| `{% endblock %}` | fecha o block |

## `{% load static %}` e `{% static %}`

```html
{% load static %}
<link rel="stylesheet" href="{% static 'notes/getit.css' %}" />
```

| Parte | O que é |
|---|---|
| `{% load static %}` | libera o `{% static %}`. Topo de **cada** template que usa |
| `{% static '...' %}` | gera `/static/notes/getit.css` · caminho a partir de `notes/static/` |

## `{% url %}`

```html
<a href="{% url 'edit' note.id %}">
```

| Parte | O que é |
|---|---|
| `url` | gera o link a partir do `name` do `path` |
| `'edit'` | o `name` (entre aspas) |
| `note.id` | valor do pedaço variável (`<int:note_id>`) → `/edit/3/` |

## `{% csrf_token %}`

```html
<form method="post">
  {% csrf_token %}
```
Código de segurança escondido. **Obrigatório** em todo `<form method="post">`, logo depois do `<form>`. Sem ele → **403**.

## `{% for %}`

```html
{% for pergunta in perguntas %}
  <li>{{ pergunta.enunciado }}</li>
{% empty %}
  <li>Nenhuma.</li>
{% endfor %}
```

| Parte | O que é | Livre? |
|---|---|---|
| `pergunta` | variável de cada volta | **livre** |
| `perguntas` | a lista (chave do `render`) | igual à chave |
| `{% empty %}` | aparece se a lista estiver vazia (opcional) | — |
| `forloop.last` / `forloop.first` / `forloop.counter` | última volta? / primeira? / número da volta (1, 2...) | fixo |

## `{% if %}`

```html
{% if pergunta.resposta_correta %}Verdadeiro{% else %}Falso{% endif %}
{% if genero.id == filme.genero_id %}selected{% endif %}
{% if not forloop.last %}, {% endif %}
```
`==`, `!=`, `>`, `<`, `and`, `or`, `not`. Espaços em volta do `==`.

## `{% now %}`

```html
{% now "d/m/Y H:i" %}      → 28/09/2026 17:20
```

## Comentários

```html
{# uma linha #}
{% comment %} várias
linhas {% endcomment %}
```
> `<!-- -->` **não** esconde tags do Django (elas rodam mesmo assim).

---

# HTML

## Estrutura da página

```html
<!DOCTYPE html>                          <!-- "é HTML5" -->
<html>                                   <!-- tudo fica dentro -->
  <head>                                 <!-- informações, NÃO aparecem -->
    <meta charset="UTF-8" />             <!-- acentos certos -->
    <title>Título da aba</title>
  </head>
  <body>                                 <!-- tudo que APARECE -->
    <h1>Título</h1>
  </body>
</html>
```

## Atributos que aparecem em quase toda tag

```html
<input class="form-card-title" id="titulo" style="color: red;" />
```

| Atributo | Para que serve | Afeta o Python? |
|---|---|---|
| `class="..."` | liga ao CSS (`.form-card-title { }` no getit.css). Várias: `class="btn btn-secondary"` | **não** |
| `id="..."` | identificador único na página (usado por `<label for>`, CSS `#id`, JS) | **não** |
| `style="..."` | CSS direto na tag: `propriedade: valor;` separados por `;` | **não** |
| `name="..."` | (campos de form) **chave enviada no POST** | **SIM** → `request.POST.get('name')` |

> 🔑 **Só o `name` chega no Python.** `class`, `id` e `style` são visual/organização.

## `form`

```html
<form class="form-card" method="post" action="/perguntas/">
```

| Atributo | O que é |
|---|---|
| `method="post"` | envia como POST (dados no corpo). Sem ele = GET (dados na URL) |
| `action="..."` | **para qual rota** envia. Sem `action` → a **mesma** página |
| `class` | visual |

Tudo que tiver `name` **dentro** do `<form>` é enviado ao clicar no botão submit.

## `input`

```html
<input class="form-card-title" type="text" id="titulo" name="titulo" placeholder="Título" />
```

| Parte | O que é | Afeta o Python? |
|---|---|---|
| `<input ... />` | campo de uma linha. Não tem tag de fechamento (`/>`) | — |
| `class="form-card-title"` | estilo do getit.css | não |
| `type="text"` | tipo do campo (ver tabela) | não |
| `id="titulo"` | identificador (para `<label for="titulo">`) | não |
| `name="titulo"` | **chave no POST** | **sim** → `request.POST.get('titulo')` |
| `placeholder="Título"` | texto cinza de dica (some ao digitar; **não é enviado**) | não |
| `value="{{ note.title }}"` | texto que **já vem preenchido** (e é enviado se não mudar) | sim (é o valor) |
| `required` | navegador não deixa enviar vazio | não |
| `style="border:none; ..."` | CSS direto (no seu: sem borda, fonte Roboto 14px, cinza, margem embaixo) | não |

| `type=` | Campo |
|---|---|
| `text` | texto |
| `number` | número (`min="0" max="10"`) — chega como texto no Python! |
| `checkbox` | caixinha (marcada → envia `'on'` ou o `value`; desmarcada → **não envia nada**) |
| `radio` | escolha única entre opções com o mesmo `name` |
| `hidden` | escondido (ex: mandar um id sem mostrar) |
| `date` / `email` / `password` | data / e-mail / senha |
| `submit` | botão de enviar |

## `textarea`

```html
<textarea class="autoresize" id="detalhes" name="detalhes" placeholder="Detalhes"></textarea>
```

| Parte | O que é |
|---|---|
| `<textarea></textarea>` | campo de **várias linhas**. Tem abertura e fechamento |
| `class="autoresize"` | o getit.js aumenta a altura ao digitar |
| `name="detalhes"` | **chave no POST** → `request.POST.get('detalhes')` |
| texto **entre** as tags | valor inicial: `<textarea name="detalhes">{{ note.content }}</textarea>` (**não tem `value`**) |

## `select` e `option`

```html
<select name="categoria">
  <option value="1">Ciências</option>
  <option value="2" selected>História</option>
</select>
```

| Parte | O que é |
|---|---|
| `<select name="categoria">` | menu suspenso. `name` = chave no POST |
| `<option value="1">` | `value` = o que é **enviado** (use o **id**) |
| `Ciências` (entre as tags) | o que a pessoa **vê** |
| `selected` | opção que já vem escolhida |
| `<select multiple>` | permite várias → `getlist` |

## `label`

```html
<label for="titulo">Título</label>
<input id="titulo" name="titulo" />
```
Texto do campo. `for` = `id` do campo (clicar no texto foca o campo). Não é enviado.

## `button`

```html
<button class="btn" type="submit">Salvar</button>
```
`type="submit"` → envia o form em que está. Texto entre as tags = o que aparece.

## `a` (link)

```html
<a class="card-edit" href="/edit/3/" title="Editar">texto ou imagem</a>
```

| Atributo | O que é |
|---|---|
| `href` | para onde vai. **Link = sempre GET** |
| `title` | dica ao passar o mouse |
| conteúdo | o que é clicável (texto ou `<img>`) |

## `img`

```html
<img src="/img/lixeira.png" alt="Apagar" class="logo" />
```
`src` = caminho da imagem · `alt` = texto alternativo (se não carregar / leitores de tela).

## Títulos, texto e listas

| Tag | O que é |
|---|---|
| `<h1>`...`<h6>` | títulos (h1 maior). "Cabeçalho h1" = isso, **não** o `<head>` |
| `<p>` | parágrafo |
| `<span>` | pedaço de texto na mesma linha (para estilizar) |
| `<div>` | caixa/bloco para agrupar (layout) |
| `<ul>` + `<li>` | lista com marcadores (cada item é um `<li>`) |
| `<ol>` + `<li>` | lista numerada |
| `<table>` `<tr>` `<th>` `<td>` | tabela · linha · célula de título · célula |
| `<br>` | quebra de linha |

## `link` (CSS) e `script` (JS)

```html
<link rel="stylesheet" href="/getit.css" />          <!-- no <head> -->
<script src="/getit.js"></script>                     <!-- no fim do <body> -->
```
`rel="stylesheet"` = "é CSS" · `href`/`src` = caminho do arquivo.

---

# Projeto 1A — Python

## `load_template` + `.format`

```python
body = load_template('index.html').format(notes=notes, error=error_html, cor=cor)
```

| Parte | O que é | Livre? |
|---|---|---|
| `body` | variável com o HTML pronto | livre |
| `load_template('index.html')` | lê `templates/index.html` como texto | nome do arquivo |
| `.format(...)` | troca cada `{nome}` do texto pelo valor | fixo |
| `notes=notes` | **esquerda** = nome do buraco `{notes}` no HTML · **direita** = variável Python | esquerda **igual ao buraco** |

> Buraco sem valor no `.format` → `KeyError`. Chave `{ }` que não é buraco → dobrar `{{ }}`.

## `build_response`

```python
return build_response(body=body, code=404, reason='Not Found', headers='Location: /')
```

| Parâmetro | Padrão | O que é |
|---|---|---|
| `body` | `''` | conteúdo (HTML) |
| `code` | `200` | código de status (200, 303, 404) |
| `reason` | `'OK'` | texto do status ('See Other', 'Not Found') |
| `headers` | `''` | cabeçalhos extras (`'Location: /'` para o 303) |

Devolve **bytes**. Parâmetros com nome → a ordem não importa.

## `extract_route` + `split`

```python
route = extract_route(request)          # 'nota/3'
note_id = int(route.split('/')[-1])     # 3
```

| Parte | Resultado |
|---|---|
| `route.split('/')` | corta nas barras → `['nota', '3']` |
| `[-1]` | último item → `'3'` |
| `int(...)` | texto → número → `3` |

## `request.startswith`

```python
if request.startswith('POST'):
```
No 1A o `request` é **texto**; começa com o método (`'GET /...'` ou `'POST /...'`).

## `unquote_plus` e o `params`

```python
request = request.replace('\r', '')      # tira caracteres \r
corpo = request.split('\n\n')[1]         # depois da linha em branco = corpo: 'titulo=Oi&detalhes=Tudo+bem'
params = {}
for chave_valor in corpo.split('&'):     # ['titulo=Oi', 'detalhes=Tudo+bem']
    chave, valor = chave_valor.split('=')           # 'detalhes', 'Tudo+bem'
    params[chave] = unquote_plus(valor)             # 'Tudo bem'
```
`params['titulo']` → a chave é o `name` do HTML. 📖 README_1A → Parte 3.

## `sqlite3` no `database.py`

```python
self.conn.execute("DELETE FROM note WHERE id = " + str(note_id) + ";")
self.conn.commit()
```

| Parte | O que é |
|---|---|
| `self.conn` | conexão com o `banco.db` (criada no `__init__`) |
| `.execute("...")` | roda um comando SQL (texto) |
| `str(note_id)` | número → texto para grudar na string |
| `.commit()` | **salva** (obrigatório ao alterar) |
| `cursor.fetchone()` | primeira linha do resultado (ou `None`) |
| `for linha in cursor` | percorre as linhas · `linha[0]` = 1ª coluna do SELECT |

## f-string

```python
f'<li>{nota.title}</li>'                  # → '<li>Mercado</li>'
```
`f` antes das aspas → o que está entre `{}` é trocado pelo valor **na hora** (diferente do `.format`, que troca depois).

## `random`

```python
import random
random.choice(['a', 'b', 'c'])           # item aleatório da lista
random.randint(1, 100)                   # inteiro entre 1 e 100 (inclui os dois)
```

## `datetime` e `locale`

```python
import locale, datetime
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')    # nomes de dia/mês em português
hoje = datetime.datetime.now()                      # agora (data + hora)
texto = hoje.strftime('%A, %d de %B de %Y, %H:%M') # formata como texto
```

| `strftime` | Vira |
|---|---|
| `%A` / `%a` | segunda-feira / seg |
| `%d` | 28 |
| `%B` / `%m` | setembro / 09 |
| `%Y` | 2026 |
| `%H:%M:%S` | 16:54:03 |