# Possíveis pedidos da prova — e como fazer


## 📑 Sumário

- **[PROJETO 1A](#projeto-1a)**
  - [Molde: rota nova no 1A](#molde-rota-nova-no-1a)
  - [A1. Página que mostra um valor calculado](#a1-página-que-mostra-um-valor-calculado)
  - [A2. Algo aleatório a cada carregamento (sem JS)](#a2-algo-aleatório-a-cada-carregamento-sem-js)
  - [A3. Contador de visitas](#a3-contador-de-visitas)
  - [A4. Rota com id: ver uma nota só](#a4-rota-com-id-ver-uma-nota-só)
  - [A5. Página com lista montada no Python](#a5-página-com-lista-montada-no-python)
  - [A6. Página nova com formulário (POST): busca](#a6-página-nova-com-formulário-post-busca)
  - [A7. Método novo no database.py: apagar tudo](#a7-método-novo-no-databasepy-apagar-tudo)
  - [A8. Mostrar algo novo na home](#a8-mostrar-algo-novo-na-home)
  - [Pegadinhas do 1A](#pegadinhas-do-1a)
- **[PROJETO 1B](#projeto-1b)**
  - [Molde: página nova no 1B](#molde-página-nova-no-1b)
  - [B1. Model com vários tipos de campo](#b1-model-com-vários-tipos-de-campo)
  - [B2. Verdadeiro/Falso digitado → BooleanField](#b2-verdadeirofalso-digitado--booleanfield)
  - [B3. Número (IntegerField) vindo do form](#b3-número-integerfield-vindo-do-form)
  - [B4. Many-to-one: select + página de detalhe do lado "um"](#b4-many-to-one-select--página-de-detalhe-do-lado-um)
  - [B5. Many-to-many com checkboxes](#b5-many-to-many-com-checkboxes)
  - [B6. Apagar item](#b6-apagar-item)
  - [B7. Editar item (com select já selecionado)](#b7-editar-item-com-select-já-selecionado)
  - [B8. Contar, ordenar, filtrar, buscar](#b8-contar-ordenar-filtrar-buscar)
  - [B9. Data/hora no Django](#b9-datahora-no-django)
  - [B10. Validação e campos obrigatórios](#b10-validação-e-campos-obrigatórios)
  - [Pegadinhas do 1B](#pegadinhas-do-1b)

---

# PROJETO 1A

📖 README_1A → Parte 0 (rota nova) e Parte 1 (templates + `.format()`)

## Molde: rota nova no 1A

**1. `templates/pagina.html`**
```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Título</title>
  </head>
  <body>
    <h1>{valor}</h1>
  </body>
</html>
```

**2. `views.py`**
```python
def minha_pagina(request):
    valor = ...                                            # calcular no Python
    body = load_template('pagina.html').format(valor=valor)
    return build_response(body=body)
```

**3. `servidor.py`**
```python
from views import ..., minha_pagina              # import

    elif route == 'minha/rota':                  # ANTES do else · sem barra no começo
        response = minha_pagina(request)
```

**4.** Reiniciar o servidor · testar em aba anônima · commit.

---

## A1. Página que mostra um valor calculado

Ex: "Mostre quantas anotações existem" em `/contador`.

```python
def contador(request):
    total = len(db.get_all())                   # len = tamanho da lista
    body = load_template('contador.html').format(total=total)
    return build_response(body=body)
```
```html
<h1>Você tem {total} anotações</h1>
```
```python
    elif route == 'contador':
        response = contador(request)
```
✅ Testado: 2 notas → "Você tem 2 anotações".

Outras contas no mesmo molde: data/hora (Questão 1.1), soma, maior título (`max(notas, key=lambda n: len(n.title))`)...

---

## A2. Algo aleatório a cada carregamento (sem JS)

Mesma ideia da Questão 1.2: **o Python sorteia** e passa pelo `.format()`.

```python
import random                                  # topo do views.py

numero = random.randint(1, 100)                # inteiro de 1 a 100 (inclui os dois)
cor = random.choice(['#DAF7A6', '#FFC300'])    # item aleatório de uma lista
frase = random.choice(['Oi!', 'Bom dia!', 'Olá!'])
```

| Onde colocar o valor | Como |
|---|---|
| Texto | `<h2>{frase}</h2>` |
| Cor de fundo da página | `<body style="background-color: {cor};">` |
| Cor do texto | `<h1 style="color: {cor};">` |
| Tamanho | `<h1 style="font-size: {tamanho}px;">` |

> Se for na **home**: sortear dentro do `render_index` e passar no `.format()` junto com `notes` e `error`.

✅ Testado: `/sorteio` → "Número sorteado: 61".

---

## A3. Contador de visitas

Ex: "Mostre quantas vezes a página foi acessada". Variável **global** no `views.py` (zera ao reiniciar o servidor).

```python
contador_visitas = 0                           # FORA de qualquer função (topo do views.py)

def visitas(request):
    global contador_visitas                    # obrigatório para alterar a variável de fora
    contador_visitas += 1
    body = load_template('visitas.html').format(n=contador_visitas)
    return build_response(body=body)
```
✅ Testado: 1ª visita "1 vezes", 2ª "2 vezes".

> Sem o `global` → `UnboundLocalError`.

---

## A4. Rota com id: ver uma nota só

Ex: `/nota/3` mostra só a nota 3; id inexistente → 404.

```python
def ver_nota(request):
    route = extract_route(request)             # 'nota/3'
    note_id = int(route.split('/')[-1])        # 3
    nota = db.get(note_id)
    if nota is None:                           # não existe → 404 (evita o servidor cair)
        return not_found(request)
    body = load_template('ver_nota.html').format(title=nota.title, content=nota.content)
    return build_response(body=body)
```
```python
    elif route.startswith('nota/'):            # startswith: tem id
        response = ver_nota(request)
```
```html
<h1>{title}</h1>
<p>{content}</p>
<a href="/">Voltar</a>
```
✅ Testado: `/nota/1` mostra a nota · `/nota/999` → 404.

Para ter um link em cada card: no `components/note.html` adicionar `<a href="/nota/{id}">ver</a>`.

---

## A5. Página com lista montada no Python

Ex: `/titulos` com `<ul>` só dos títulos.

```python
def titulos(request):
    itens = ''
    for nota in db.get_all():
        itens += f'<li>{nota.title}</li>\n'    # monta o HTML de cada item
    body = load_template('titulos.html').format(itens=itens)
    return build_response(body=body)
```
```html
<ul>
{itens}
</ul>
```
✅ Testado.

> Mesma ideia do `render_index` (que monta os cards com `note.html`).

---

## A6. Página nova com formulário (POST): busca

Ex: `/buscar` com um campo; mostra as notas cujo título contém o texto.

```python
def buscar(request):
    resultado = ''
    if request.startswith('POST'):
        request = request.replace('\r', '')
        corpo = request.split('\n\n')[1]
        params = {}
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[chave] = unquote_plus(valor)
        termo = params.get('termo', '').lower()
        for nota in db.get_all():
            if termo in nota.title.lower():     # "contém", sem diferenciar maiúscula
                resultado += f'<li>{nota.title}</li>\n'
    body = load_template('buscar.html').format(resultado=resultado)
    return build_response(body=body)
```
```html
<form method="post">                            <!-- sem action → POST /buscar -->
  <input type="text" name="termo" />            <!-- name = chave do params -->
  <button type="submit">Buscar</button>
</form>
<ul>
{resultado}
</ul>
```
✅ Testado: termo "merc" → "Mercado hoje".

> Aqui **não** usa 303: a resposta do POST é a própria página com o resultado.
> Se o formulário **salvar** algo, aí sim termina em 303 (📖 README_1A → Parte 4 → molde).

---

## A7. Método novo no `database.py`: apagar tudo

```python
    def delete_all(self):                       # dentro da classe Database (4 espaços)
        self.conn.execute("DELETE FROM note;")  # sem WHERE = TODAS as linhas
        self.conn.commit()
```
```python
def apagar_tudo(request):
    db.delete_all()
    return build_response(code=303, reason='See Other', headers='Location: /')
```
```python
    elif route == 'apagar-tudo':
        response = apagar_tudo(request)
```
✅ Testado: depois de `/apagar-tudo`, contador → 0.

Padrão de método novo: altera → `execute` + `commit` · lê → `execute` + `for`/`fetchone` (📖 README_1A → Parte 2).

---

## A8. Mostrar algo novo na home

Ex: "Mostre o total de notas no topo da página principal".

1. `index.html`: criar o buraco onde quiser → `<p>Total: {total}</p>`
2. `render_index`: calcular e passar → `.format(notes=notes, error=error_html, total=len(db.get_all()))`

> O `index.html` é usado **só** no `render_index` → basta mudar esse `.format()`.
> Esqueceu de passar → `KeyError: 'total'`.

---

## Pegadinhas do 1A

1. **`elif` depois do `else`** ou **função fora do `from views import`** → rota nunca funciona
2. **Rota no `servidor.py` sem barra no começo**: `'hoje/agora'`, não `'/hoje/agora'`
3. **Chave `{ }` extra no template** (CSS) → `KeyError`/`ValueError` → dobrar `{{ }}` ou usar `style="..."`
4. **CSS em página com rota com barra** → `href="/getit.css"`
5. **Mudou `.py` e não reiniciou** → nada muda
6. **Erro na view derruba o servidor** → olhar o terminal (traceback) e reiniciar
7. **Rodar de fora da pasta** → outro `banco.db`
8. **Porta**: conferir `SERVER_PORT` (no meu, 8000 na pasta da prova)

---

# PROJETO 1B

📖 README_1B → Parte 1 (CRUD) e Parte 2 (relações, **many-to-one passo a passo**)

## Molde: página nova no 1B

```python
# notes/urls.py
path('itens/', views.itens, name='itens'),

# notes/views.py
def itens(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        Item.objects.create(nome=nome)
        return redirect('itens')                 # volta para a mesma página
    todos = Item.objects.all()
    return render(request, 'notes/itens.html', {'itens': todos})
```
```html
<!-- notes/templates/notes/itens.html -->
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Itens</title></head>
<body>
  <form method="post">
    {% csrf_token %}
    <input type="text" name="nome" />
    <button type="submit">Salvar</button>
  </form>
  <ul>
    {% for item in itens %}
      <li>{{ item.nome }}</li>
    {% endfor %}
  </ul>
</body>
</html>
```

Model novo? → `makemigrations` + `migrate` (+ `admin.site.register` se quiser ver no /admin).

---

## B1. Model com vários tipos de campo

```python
class Filme(models.Model):
    titulo = models.CharField(max_length=200)        # texto curto (max_length obrigatório)
    sinopse = models.TextField()                     # texto longo, sem limite
    nota = models.IntegerField()                     # inteiro
    assistido = models.BooleanField()                # True/False
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, null=True)   # many-to-one
    plataformas = models.ManyToManyField(Plataforma, blank=True)             # many-to-many
```

| Campo | Para | Detalhe |
|---|---|---|
| `CharField(max_length=N)` | texto curto | `max_length` obrigatório |
| `TextField()` | texto longo | "sem limite de caracteres" |
| `IntegerField()` | inteiro | |
| `FloatField()` | decimal | |
| `BooleanField()` | verdadeiro/falso | |
| `DateField()` / `DateTimeField()` | data / data e hora | `auto_now_add=True` = preenche na criação |
| `EmailField()` | e-mail | |

| Pedido do enunciado | Como |
|---|---|
| "não pode ser nulo" / "obrigatório" | **nada** (é o padrão) |
| "pode ficar vazio" | `null=True` (e `blank=True` para o admin) |
| "não pode repetir" | `unique=True` |
| "valor padrão X" | `default=X` |
| "não deve ter campo adicional" | só os campos pedidos (o `id` é automático, não conta) |

📖 https://docs.djangoproject.com/en/stable/ref/models/fields/

---

## B2. Verdadeiro/Falso digitado → `BooleanField`

O form manda **texto**; o model quer **True/False**. Converter na view:

```python
assistido = request.POST.get('assistido') == 'Verdadeiro'   # True se digitou Verdadeiro, senão False
```

Mostrar de volta em português no template:
```html
{% if filme.assistido %}Verdadeiro{% else %}Falso{% endif %}
```
✅ Testado: "Verdadeiro" → `True`, "Falso" → `False`.

**Alternativas de input:**

| Input | Na view |
|---|---|
| `<input type="checkbox" name="assistido">` | `request.POST.get('assistido') == 'on'` (desmarcado = não vem nada) |
| `<select name="assistido"><option value="True">Verdadeiro</option><option value="False">Falso</option></select>` | `request.POST.get('assistido') == 'True'` |

> Salvar o texto direto (`assistido='Falso'`) num `BooleanField` → erro
> `ValidationError: “Falso” value must be either True or False.` (testado)

---

## B3. Número (`IntegerField`) vindo do form

Tudo do `request.POST` chega como **texto** → converter:

```python
nota = int(request.POST.get('nota'))            # '8' → 8
preco = float(request.POST.get('preco'))        # '9.5' → 9.5
```
```html
<input type="number" name="nota" min="0" max="10" />
```

---

## B4. Many-to-one: select + página de detalhe do lado "um"

📖 **Passo a passo completo: README_1B → Parte 2 → ⭐ MANY-TO-ONE**

Resumo (testado):

```python
# criar com o id escolhido no <select name="genero">
genero_id = request.POST.get('genero')
Filme.objects.create(..., genero_id=genero_id)

# a view do form precisa mandar a lista para o select
return render(request, 'notes/filmes.html', {'filmes': ..., 'generos': Genero.objects.all()})
```
```html
<select name="genero">
  {% for genero in generos %}
    <option value="{{ genero.id }}">{{ genero.nome }}</option>
  {% endfor %}
</select>

{{ filme.genero.nome }}          <!-- mostrar o gênero de um filme -->
```

**Página de detalhe do lado "um"** (ex: `/generos/1/` com os filmes daquele gênero):

```python
path('generos/<int:genero_id>/', views.genero_detalhe, name='genero_detalhe'),

def genero_detalhe(request, genero_id):
    genero = Genero.objects.get(id=genero_id)
    filmes = genero.filme_set.all()            # ou Filme.objects.filter(genero=genero)
    return render(request, 'notes/genero_detalhe.html', {'genero': genero, 'filmes': filmes})
```
```html
<h1>Filmes de {{ genero.nome }}</h1>
<ul>
  {% for filme in filmes %}
    <li>{{ filme.titulo }}</li>
  {% empty %}
    <li>Nenhum filme.</li>                     <!-- aparece se a lista estiver vazia -->
  {% endfor %}
</ul>
```

Link + contagem na lista de gêneros:
```html
<li><a href="{% url 'genero_detalhe' genero.id %}">{{ genero.nome }}</a> ({{ genero.filme_set.count }} filmes)</li>
```
✅ Testado.

---

## B5. Many-to-many com checkboxes

Várias opções marcáveis, mesmo `name`:

```html
{% for p in plataformas %}
  <label><input type="checkbox" name="plataformas" value="{{ p.id }}" /> {{ p.nome }}</label>
{% endfor %}
```
```python
filme = Filme.objects.create(...)               # 1º cria
ids = request.POST.getlist('plataformas')       # getlist → TODOS os marcados: ['1', '2']
filme.plataformas.set(ids)                      # liga todos de uma vez (troca os anteriores)
```
```html
{% for p in filme.plataformas.all %}{{ p.nome }} {% endfor %}
```
✅ Testado: marcou Netflix e Prime → lista mostra "Netflix Prime".

> `request.POST.get(...)` com vários marcados → só pega **o último**. Usar **`getlist`**.
> Alternativa: `<select name="plataformas" multiple>` (mesma view).

---

## B6. Apagar item

```python
path('filmes/<int:filme_id>/apagar/', views.apagar_filme, name='apagar_filme'),

def apagar_filme(request, filme_id):
    Filme.objects.get(id=filme_id).delete()
    return redirect('filmes')
```
```html
<a href="{% url 'apagar_filme' filme.id %}">apagar</a>
```
✅ Testado.

> Apagar um gênero com `on_delete=models.CASCADE` apaga **os filmes dele junto**.

---

## B7. Editar item (com select já selecionado)

```python
path('filmes/<int:filme_id>/editar/', views.editar_filme, name='editar_filme'),

def editar_filme(request, filme_id):
    filme = Filme.objects.get(id=filme_id)
    if request.method == 'POST':
        filme.titulo = request.POST.get('titulo')
        filme.genero_id = request.POST.get('genero')
        filme.save()
        return redirect('filmes')
    return render(request, 'notes/editar_filme.html', {'filme': filme, 'generos': Genero.objects.all()})
```
```html
<form method="post">
  {% csrf_token %}
  <input type="text" name="titulo" value="{{ filme.titulo }}" />
  <select name="genero">
    {% for genero in generos %}
      <option value="{{ genero.id }}" {% if genero.id == filme.genero_id %}selected{% endif %}>{{ genero.nome }}</option>
    {% endfor %}
  </select>
  <button type="submit">Salvar</button>
</form>
```
✅ Testado: o gênero atual vem selecionado; salvar troca título e gênero.

---

## B8. Contar, ordenar, filtrar, buscar

| Pedido | View (Python) | Template |
|---|---|---|
| quantos existem | `Filme.objects.count()` | `{{ filmes\|length }}` · `{{ genero.filme_set.count }}` |
| ordem alfabética | `.order_by('titulo')` | |
| ordem decrescente | `.order_by('-nota')` (o `-` inverte) | |
| mais recentes primeiro | `.order_by('-id')` | |
| só os que... | `.filter(assistido=True)` · `.filter(nota__gte=7)` (≥7) | |
| título contém texto (sem maiúscula/minúscula) | `.filter(titulo__icontains=texto)` | |
| lista vazia | | `{% for %}...{% empty %}Nada{% endfor %}` |

**Busca com formulário GET** (o texto vai na URL: `/filmes/?q=tit`):

```html
<form method="get">                             <!-- GET: sem csrf_token -->
  <input type="text" name="q" value="{{ busca }}" />
  <button type="submit">Buscar</button>
</form>
```
```python
busca = request.GET.get('q', '')                # GET → request.GET (não POST)
lista = Filme.objects.filter(titulo__icontains=busca).order_by('-nota')
return render(request, 'notes/filmes.html', {'filmes': lista, 'busca': busca, 'total': Filme.objects.count()})
```
✅ Testado: `?q=tit` → só "Titanic"; lista ordenada por nota decrescente.

📖 https://docs.djangoproject.com/en/stable/topics/db/queries/

---

## B9. Data/hora no Django

**Sem Python** (tag de template):
```html
<h2>{% now "d/m/Y H:i" %}</h2>     <!-- → 28/09/2026 17:20 (testado) -->
```

**Pela view:**
```python
import datetime
agora = datetime.datetime.now()
return render(request, 'notes/x.html', {'agora': agora})
```
```html
{{ agora|date:"d/m/Y H:i" }}
```

📖 https://docs.djangoproject.com/en/stable/ref/templates/builtins/#date

---

## B10. Validação e campos obrigatórios

**No HTML** (o navegador não deixa enviar vazio):
```html
<input type="text" name="nome" required />
```

**Na view** (mostrar mensagem):
```python
if request.method == 'POST':
    nome = request.POST.get('nome', '').strip()
    if not nome:
        return render(request, 'notes/itens.html', {'itens': Item.objects.all(), 'erro': 'Preencha o nome'})
    Item.objects.create(nome=nome)
    return redirect('itens')
```
```html
{% if erro %}<p>{{ erro }}</p>{% endif %}
```

---

## Pegadinhas do 1B

1. **Sem `{% csrf_token %}`** em form POST → 403 (form GET não precisa)
2. **Mexeu no model e não migrou** → `no such table` / `no such column`
3. **`ForeignKey` sem `on_delete`** → erro
4. **`makemigrations` perguntou "Select an option"** → README_1B → Parte 2 → Passo 3
5. **`<select>` vazio** → a view não mandou a lista no `render`, ou não tem nada cadastrado
6. **Nenhuma categoria cadastrada e enviou o form com `<select>`** → chega `genero_id=''`:
   ForeignKey obrigatória → `IntegrityError: NOT NULL constraint failed` · com `null=True` → salva **sem** gênero.
   → cadastrar o lado "um" antes de testar
7. **Texto num `BooleanField`/`IntegerField`** → converter (`== 'Verdadeiro'`, `int(...)`)
8. **Vários checkboxes com `.get`** → só vem um → `getlist`
9. **`redirect`/`{% url %}` com name errado** → `NoReverseMatch`
10. **Parênteses no template** (`.all()`, `.count()`) → erro. No template: `.all`, `.count`
11. **Rota**: `http://localhost:8000/perguntas` sem barra → o Django redireciona para `/perguntas/` (GET funciona).
    O form sem `action` já envia para a URL certa.
12. **Porta**: se o 1A estiver na 8000, rodar o 1B com `python manage.py runserver 8001`