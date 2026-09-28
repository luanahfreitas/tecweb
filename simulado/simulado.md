# Simulado — "quando pedirem X, eu fiz assim"

📖 Enunciado: https://barbaratieko.github.io/tecweb/simulado/251_tecweb_ai_disponibilizar.pdf



---

## 🔎 Busca rápida: "se o professor pedir..."

| Se pedir... | Projeto | Vá para |
|---|---|---|
| uma **página/rota nova** com HTML próprio | 1A | [Quando pedirem uma página nova](#-quando-pedirem-uma-página-nova-com-um-valor-do-python-11) |
| mostrar **data/hora** | 1A | [idem](#-quando-pedirem-uma-página-nova-com-um-valor-do-python-11) |
| algo que **muda a cada carregamento** (cor, frase) **sem JS** | 1A | [Quando pedirem para mudar o fundo](#-quando-pedirem-para-mudar-o-fundo-a-cada-carregamento-sem-js-12) |
| um **model novo** com campos e regras (não nulo, sem limite) | 1B | [Quando pedirem um model novo](#-quando-pedirem-um-model-novo-31) |
| um **formulário** que salva no banco | 1B | [Quando pedirem um formulário](#-quando-pedirem-um-formulário-que-salva-no-banco-32) |
| converter **"Verdadeiro/Falso"** em booleano | 1B | [idem](#-quando-pedirem-um-formulário-que-salva-no-banco-32) |
| **listar** o que foi cadastrado (`<ul>`) | 1B | [Quando pedirem para listar](#-quando-pedirem-para-listar-o-que-foi-cadastrado-33) |
| **outro model + página** com form e lista | 1B | [Quando pedirem outro cadastro](#-quando-pedirem-outro-cadastro-completo-model--form--lista-34) |
| **ligar dois models** (um para muitos) com **dropdown** | 1B | [Quando pedirem o dropdown](#-quando-pedirem-para-ligar-dois-models-com-um-dropdown-35) |

---

# PROJETO 1A

> Rodar de dentro da pasta: `cd "projeto 1A"` → `python servidor.py`.
> Mudou `.py` → **Ctrl+C e rodar de novo**. Porta: conferir `SERVER_PORT` (no meu: 8000).

## ✅ Quando pedirem uma página nova com um valor do Python (1.1)

> **Pedido:** rota `/hoje/agora` · HTML novo e válido (`html`, `head`, `body`) · `<h1>` "Avaliação Intermediária" ·
> `<h2>` com data e hora (`datetime.datetime.now()`) · função nova no `views.py`.
> **Commit:** `Adicionando data de hoje`

**Eu resolvi assim** — os 3 passos da rota nova (📖 README_1A → Parte 0):

**1. `templates/data.html`** (arquivo novo) — com um **buraco** `{data}` onde o Python coloca o valor:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Hoje</title>
  </head>
  <body>
    <h1>Avaliação Intermediária</h1>
    <h2>{data}</h2>
  </body>
</html>
```

**2. `views.py`** — imports no topo + função no final:

```python
import locale
import datetime
```
```python
def hoje_agora(request):
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')                 # português (código do enunciado)
    hoje = datetime.datetime.now()
    data_em_extenso = hoje.strftime('%A, %d de %B de %Y, %H:%M')    # + %H:%M = hora

    body = load_template('data.html').format(data=data_em_extenso)  # preenche o buraco {data}
    return build_response(body=body)
```

**3. `servidor.py`** — import + `elif` **antes do `else`** (`==` porque a rota é fixa):

```python
from views import index, delete, edit, confirm_delete, not_found, favorite, hoje_agora
```
```python
    elif route == 'hoje/agora':
        response = hoje_agora(request)
    else:
        response = not_found(request)
```

**Resultado:** `segunda-feira, 28 de setembro de 2026, 16:54`

| `strftime` | Vira |
|---|---|
| `%A` `%d` `%B` `%Y` | segunda-feira · 28 · setembro · 2026 |
| `%H:%M` | 16:54 |
| `%d/%m/%Y` | 28/09/2026 |

**Cuidados:** nenhuma outra chave `{ }` no HTML (quebra o `.format`) · CSS com barra: `href="/getit.css"` ·
se der `locale.Error`, trocar `'pt_BR.UTF-8'` por `'pt_BR'`.

---

## ✅ Quando pedirem para mudar o fundo a cada carregamento, sem JS (1.2)

> **Pedido:** fundo muda de cor a cada carregamento · **sem JavaScript** · mexer em `index.html` e `views.py` · mínimo 6 cores.
> **Commit:** `Adicionando cor ao fundo da página`

**O raciocínio:** sem JS o navegador não sorteia nada → **o Python sorteia**. Cada carregamento = novo `GET /` =
a função que monta a home roda de novo = sorteio novo. No meu projeto quem monta a home é o **`render_index`**.

**Eu resolvi assim:**

**1. `views.py`** — `import random` no topo, e no `render_index` trocar a linha do `body`:

```python
    cores = ['#DAF7A6', '#FFC300', '#FF5733', '#C70039', '#900C3F', '#581845']
    cor = random.choice(cores)

    body = load_template('index.html').format(notes=notes, error=error_html, cor=cor)
```

**2. `templates/index.html`** — buraco na tag `<body>`:

```html
  <body style="background-color: {cor};">
```

**Por que `style=` na tag:** CSS direto, sem chaves extras (um `<style>` com `{ }` quebraria o `.format`).

**Erros que podem aparecer:** `KeyError: 'cor'` (faltou `cor=cor`) · `NameError: random` (faltou import) ·
VS Code sublinha `{cor}` em vermelho → **ignorar** (é só o editor).

> A mesma ideia serve para qualquer "coisa aleatória": frase (`random.choice`), número (`random.randint(1, 100)`), cor do texto (`style="color: {cor};"`).

---

# PROJETO 1B

> `cd "projeto 1B"` → `source env/bin/activate` → `python manage.py runserver`.
> Mexeu no `models.py` → **`makemigrations` + `migrate`**. Os outros `.py` recarregam sozinhos.

## ✅ Quando pedirem um model novo (3.1)

> **Pedido:** model `Pergunta` com `enunciado` (TextField, sem limite, não nulo) e `resposta_correta`
> (BooleanField, não nulo). Nenhum campo a mais. Fazer as migrações.
> **Commit:** `Criando modelo Pergunta`

**Eu resolvi assim** — `notes/models.py`:

```python
class Pergunta(models.Model):
    enunciado = models.TextField(null=False)
    resposta_correta = models.BooleanField(null=False)
```

```bash
python manage.py makemigrations
python manage.py migrate
```

| Pedido do enunciado | Como escrevi |
|---|---|
| "sem limite de caracteres" | `TextField` (não `CharField`) |
| "não pode ser nulo" | `null=False` (ou nada: é o padrão) |
| "verdadeiro ou falso" | `BooleanField` |
| "nenhum campo adicional" | só esses dois (o `id` é automático, não conta) |

> O nome do campo é `resposta_correta` (no PDF aparece "resposta correta" porque o `_` some na cópia do texto).

---

## ✅ Quando pedirem um formulário que salva no banco (3.2)

> **Pedido:** rota `perguntas` · formulário com enunciado e resposta · salvar no banco · usuário digita
> "Verdadeiro" ou "Falso" · depois de salvar, voltar para `/perguntas`. Sem CSS.
> **Commit:** `Formulário criado`

**Eu resolvi assim:**

**1. `notes/urls.py`:**
```python
path('perguntas', views.perguntas, name='perguntas'),
```

**2. `notes/views.py`** — `Pergunta` no import + função com as duas metades:
```python
from .models import Note, Tag, Pergunta

def perguntas(request):
    if request.method == 'POST':
        enunciado = request.POST.get('enunciado')          # 'enunciado' = name do input
        resposta = request.POST.get('resposta')            # texto: 'Verdadeiro' ou 'Falso'
        resposta_correta = resposta == 'Verdadeiro'        # texto → True/False
        Pergunta.objects.create(enunciado=enunciado, resposta_correta=resposta_correta)
        return redirect('perguntas')                       # volta para /perguntas
    return render(request, 'notes/perguntas.html')
```

**3. `notes/templates/notes/perguntas.html`:**
```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Perguntas</title>
  </head>
  <body>
    <form method="post">
      {% csrf_token %}
      <input type="text" name="enunciado" placeholder="enunciado" />
      <input type="text" name="resposta" placeholder="Verdadeiro ou Falso" />
      <button type="submit">Criar</button>
    </form>
  </body>
</html>
```

**Por que converter para True/False:** o form manda **texto** e o campo é `BooleanField`.
Salvar `'Verdadeiro'` direto dá `ValidationError: “Verdadeiro” value must be either True or False.`
O "assuma que o usuário escreverá certo" só dispensa tratar erro de digitação (ver Dúvida 3).

**Erro que eu tive:** `IntegrityError: NOT NULL constraint failed: notes_pergunta.enunciado`
→ o `name` do input não batia com o `request.POST.get(...)` (chegou `None`).
Conferir na página amarela: **Request information → POST** mostra os `name` enviados.

---

## ✅ Quando pedirem para listar o que foi cadastrado (3.3)

> **Pedido:** abaixo do formulário, `<ul>` com todas as perguntas (enunciado + resposta); nova pergunta aparece na lista.
> **Commit:** `Listagem implementada`

**Eu resolvi assim** — só a **metade GET** da view e o template mudam:

**1. `views.py`** — trocar o último `return` da função `perguntas`:
```python
    todas = Pergunta.objects.all()
    return render(request, 'notes/perguntas.html', {'perguntas': todas})
```

**2. `perguntas.html`** — depois do `</form>`:
```html
    <ul>
      {% for pergunta in perguntas %}
        <li>{{ pergunta.enunciado }} - {{ pergunta.resposta_correta }}</li>
      {% endfor %}
    </ul>
```

Mostra `True`/`False` (deixei assim). Em português seria `{% if pergunta.resposta_correta %}Verdadeiro{% else %}Falso{% endif %}`.

**"Nova pergunta aparece na lista"** vem de graça: o `redirect` depois do POST faz um GET, que busca todas de novo.
Não precisa de migração (o model não mudou).

> Lista vazia sem erro → a chave `'perguntas'` do `render` ≠ nome no `{% for ... in perguntas %}`.

---

## ✅ Quando pedirem outro cadastro completo: model + form + lista (3.4)

> **Pedido:** model `Categoria` com `nome` (CharField, obrigatório) · rota `categorias` com form e lista abaixo.
> **Commit:** `Cadastro de categorias`

**Eu resolvi assim** — é o **mesmo molde** da 3.1 + 3.2 + 3.3 juntas:

**1. `models.py`** (+ `makemigrations` + `migrate`):
```python
class Categoria(models.Model):
    nome = models.CharField(max_length=100)          # obrigatório = sem null=True
```

**2. `urls.py`:**
```python
path('categorias', views.categorias, name='categorias'),
```

**3. `views.py`** (`Categoria` no import):
```python
def categorias(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        Categoria.objects.create(nome=nome)
        return redirect('categorias')
    todas = Categoria.objects.all()
    return render(request, 'notes/categorias.html', {'categorias': todas})
```

**4. `notes/templates/notes/categorias.html`:**
```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Categorias</title>
  </head>
  <body>
    <form method="post">
      {% csrf_token %}
      <input type="text" name="nome" placeholder="Categoria" />
      <button type="submit">Criar</button>
    </form>

    <ul>
      {% for categoria in categorias %}
        <li>{{ categoria.nome }}</li>
      {% endfor %}
    </ul>
  </body>
</html>
```

**Erros que eu tive:**

| Erro | Causa | Solução |
|---|---|---|
| `no such table: notes_categoria` | criei o model e não migrei | `makemigrations` + `migrate` |
| aparecia `{ categoria.nome }` escrito na tela | chave **simples** | `{{ categoria.nome }}` (duas chaves) |
| `name="enunciado"` copiado do form de perguntas | nome não batia com `request.POST.get('nome')` | `name="nome"` |

> `CharField()` sem `max_length` funcionou no Django 6.1 + SQLite, mas o certo é colocar `max_length`.

---

## ✅ Quando pedirem para ligar dois models com um dropdown (3.5)

> **Pedido:** relação **um para muitos** (uma categoria tem várias perguntas; uma pergunta tem **uma** categoria) ·
> campo `categoria` com `<select>` no form de perguntas · mostra todas as categorias · salvar ligado à pergunta.
> **Commit:** `Categoria Finalizada`

📖 Passo a passo detalhado: README_1B → Parte 2 → ⭐ MANY-TO-ONE

**Eu resolvi assim:**

**1. `models.py`** — `ForeignKey` no lado **"muitos"** (a pergunta escolhe **uma** categoria), `Categoria` **antes** de `Pergunta` no arquivo:
```python
class Pergunta(models.Model):
    enunciado = models.TextField(null=False)
    resposta_correta = models.BooleanField(null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
```

**2. Migrações — o `makemigrations` PERGUNTOU:**
```
It is impossible to add a non-nullable field 'categoria' to pergunta without specifying a default...
 1) Provide a one-off default now ...
 2) Quit and manually define a default value in models.py.
Select an option:
```
Já existiam perguntas e **nenhuma categoria cadastrada** → escolhi **`2`**, coloquei **`null=True`** e rodei de novo:
```bash
python manage.py makemigrations
python manage.py migrate
```
(Opção 1 com um id que não existe → `makemigrations` passa, mas `migrate` quebra com `IntegrityError`.)

**3. `views.py`** — `Categoria` no import · ler o `<select>` · mandar a lista para o template:
```python
from .models import Note, Tag, Pergunta, Categoria

def perguntas(request):
    if request.method == 'POST':
        enunciado = request.POST.get('enunciado')
        resposta = request.POST.get('resposta')
        resposta_correta = resposta == 'Verdadeiro'
        categoria_id = request.POST.get('categoria')         # name do <select> → chega o ID ('2')
        Pergunta.objects.create(enunciado=enunciado,
                                resposta_correta=resposta_correta,
                                categoria_id=categoria_id)    # liga pelo id
        return redirect('perguntas')
    todas = Pergunta.objects.all()
    categorias = Categoria.objects.all()                     # ← para montar o <select>
    return render(request, 'notes/perguntas.html', {'perguntas': todas, 'categorias': categorias})
```

**4. `perguntas.html`** — o `<select>` dentro do form, antes do botão:
```html
      <select name="categoria">
        {% for categoria in categorias %}
          <option value="{{ categoria.id }}">{{ categoria.nome }}</option>
        {% endfor %}
      </select>
```

| Parte | Por quê |
|---|---|
| `name="categoria"` | = `request.POST.get('categoria')` |
| `value="{{ categoria.id }}"` | o que é **enviado** → tem que ser o **id** (a ForeignKey liga pelo id) |
| `{{ categoria.nome }}` entre as tags | o que a pessoa **vê** |
| `'categorias': categorias` no `render` | sem isso o menu fica **vazio** (sem erro) |

**Erro que eu tive:** escrevi `<option value={categoria.nome}>` →
chave simples (não é trocada) **e** nome no lugar do id. Certo: `value="{{ categoria.id }}"`.

✅ Testado: "Pedro Álvares Cabral chegou em 1500?" + Verdadeiro + História → salva com categoria **História**.

> Opcional: mostrar na lista com `{{ pergunta.categoria.nome }}` (as antigas ficam em branco: categoria `None`).

---

## ✅ Checklist final

- [ ] 1.1 `/hoje/agora` → `Adicionando data de hoje`
- [ ] 1.2 cor de fundo → `Adicionando cor ao fundo da página`
- [ ] 3.1 model `Pergunta` + migrações → `Criando modelo Pergunta`
- [ ] 3.2 formulário `/perguntas` → `Formulário criado`
- [ ] 3.3 lista `<ul>` → `Listagem implementada`
- [ ] 3.4 `Categoria` + `/categorias` → `Cadastro de categorias`
- [ ] 3.5 ForeignKey + `<select>` → `Categoria Finalizada`
- [ ] `git push` e conferir os commits no GitHub (`git log --oneline`)

---

# 💬 Dúvidas que eu tive

## 1. `locale.Error: unsupported locale setting`

É a linha `locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')` que falhou (o computador não tem o português
com esse nome). No Mac costuma funcionar; se não, trocar por `'pt_BR'`.

## 2. O VS Code sublinha o `{cor}` em vermelho e mostra "2 Problems"

**Pode ignorar.** O VS Code lê o `style="..."` como CSS e acha que `background-color: {cor};` é inválido.
Ele não sabe que o Python vai trocar `{cor}` por `#FF5733` antes de mandar para o navegador.
É **aviso do editor**, não erro no código. Para confirmar: reiniciar o servidor e recarregar a página.

## 3. Questão 3.2: como transformar "Verdadeiro"/"Falso" em `True`/`False`?

O usuário **digita** a resposta → chega **texto** (`'Verdadeiro'`). O campo `resposta_correta` é
`BooleanField` → só aceita `True`/`False`. **Tem que converter na view antes de salvar:**

```python
resposta = request.POST.get('resposta')          # texto: 'Verdadeiro' ou 'Falso'
resposta_correta = resposta == 'Verdadeiro'      # True se digitou Verdadeiro, senão False
Pergunta.objects.create(enunciado=enunciado, resposta_correta=resposta_correta)
```

`resposta == 'Verdadeiro'` é uma **comparação**: o resultado dela já é `True` ou `False`.

| Digitou | `resposta == 'Verdadeiro'` | Salva |
|---|---|---|
| `Verdadeiro` | `True` | `True` |
| `Falso` | `False` | `False` |

**Salvar o texto direto dá erro, mesmo escrito certo** (testado):

```
resposta_correta='Verdadeiro' → ValidationError: “Verdadeiro” value must be either True or False.
resposta_correta='Falso'      → ValidationError: “Falso” value must be either True or False.
```

**"Assuma que o usuário escreverá Verdadeiro ou Falso"** — o que isso muda:

| | Precisa? | Por quê |
|---|---|---|
| Converter texto → `True`/`False` | **Sim** | o campo é `BooleanField` e o form manda texto |
| Tratar digitação errada (`verdadeiro`, `V`, `sim`...) | **Não** | o enunciado mandou assumir que vem certo |

→ Por isso basta **uma linha** com `==`: quem não escreveu "Verdadeiro" escreveu "Falso".

**Mostrar de volta em português** (3.3, na lista):

```html
{% if pergunta.resposta_correta %}Verdadeiro{% else %}Falso{% endif %}
```

**Outros inputs possíveis** (se o enunciado pedir):

| Input | Conversão na view |
|---|---|
| `<input type="text" name="resposta">` (digitado) | `request.POST.get('resposta') == 'Verdadeiro'` |
| `<input type="checkbox" name="resposta">` | `request.POST.get('resposta') == 'on'` (desmarcado não envia nada) |
| `<select name="resposta"><option value="True">Verdadeiro</option><option value="False">Falso</option></select>` | `request.POST.get('resposta') == 'True'` |

📖 README_POSSIVEIS → B2 · README_ANATOMIA → `request.POST.get`