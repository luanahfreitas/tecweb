# Projeto 1A — Get-it (servidor HTTP feito na mão)

Guia de consulta para a prova. Cada parte segue a ordem do enunciado.

📖 Enunciado: https://barbaratieko.github.io/tecweb/projetos/projeto1/projeto1a/

## 📑 Sumário

- **[Como rodar](#como-rodar)**
- **[Mapa dos arquivos](#mapa-dos-arquivos)**
- **[Parte 0 — A base: servidor.py e utils.py](#parte-0--a-base-servidorpy-e-utilspy)**
  - [Conceitos](#conceitos)
  - [servidor.py](#servidorpy)
  - [utils.py](#utilspy)
  - [✅ Rota nova: o que muda no servidor.py](#-rota-nova-o-que-muda-no-servidorpy)
  - [⚠ Pegadinhas](#-pegadinhas)
- **[Parte 1 — Estilo da página](#parte-1--estilo-da-página)**
  - [O que a tarefa pedia](#o-que-a-tarefa-pedia)
  - [Como o CSS e o JS chegam no navegador](#como-o-css-e-o-js-chegam-no-navegador)
  - [CSS básico](#css-básico)
  - [🔸 Templates e .format() (precisa entender)](#-templates-e-format-precisa-entender)
  - [⚠ Pegadinhas](#-pegadinhas-1)
- **[Parte 2 — Persistência de dados (SQLite)](#parte-2--persistência-de-dados-sqlite)**
  - [O que a tarefa pedia](#o-que-a-tarefa-pedia-1)
  - [Conceitos](#conceitos-1)
  - [database.py](#databasepy)
  - [Como o views.py usa](#como-o-viewspy-usa)
  - [✅ Na prova](#-na-prova)
  - [⚠ Pegadinhas e dicas](#-pegadinhas-e-dicas)
- **[Parte 3 — Apagar anotações](#parte-3--apagar-anotações)**
  - [O que a tarefa pedia](#o-que-a-tarefa-pedia-2)
  - [Conceitos-chave](#conceitos-chave)
  - [✅ Versão 1 — A que eu entreguei (conceito A, com confirmação)](#-versão-1--a-que-eu-entreguei-conceito-a-com-confirmação)
  - [Versão 2 — Com POST + input hidden (a outra opção do enunciado, sem confirmação)](#versão-2--com-post--input-hidden-a-outra-opção-do-enunciado-sem-confirmação)
  - [⚠ Pegadinhas](#-pegadinhas-2)
- **[Parte 4 — Editar anotações](#parte-4--editar-anotações)**
  - [O que a tarefa pedia](#o-que-a-tarefa-pedia-3)
  - [Fluxo](#fluxo)
  - [templates/components/note.html (link do lápis)](#templatescomponentsnotehtml-link-do-lápis)
  - [servidor.py](#servidorpy-1)
  - [views.py — função com duas metades](#viewspy--função-com-duas-metades)
  - [templates/edit.html (parte importante)](#templatesedithtml-parte-importante)
  - [database.py](#databasepy-1)
  - [⚠ Pegadinhas](#-pegadinhas-3)
- **[Parte 5 — Página 404 (conceito A)](#parte-5--página-404-conceito-a)**
  - [O que o enunciado pedia](#o-que-o-enunciado-pedia)
  - [servidor.py — o else do roteamento](#servidorpy--o-else-do-roteamento)
  - [views.py](#viewspy)
  - [templates/404.html (partes que atendem o enunciado)](#templates404html-partes-que-atendem-o-enunciado)
  - [🔍 Conferir o código de status no navegador](#-conferir-o-código-de-status-no-navegador)
  - [⚠ Pegadinhas](#-pegadinhas-4)
- **[Parte 6 — Extras do A+ (favoritar, ordenar, validar)](#parte-6--extras-do-a-favoritar-ordenar-validar)**
  - [O que o A+ pedia](#o-que-o-a-pedia)
  - [🔸 If ternário (aparece várias vezes)](#-if-ternário-aparece-várias-vezes)
  - [1. Favoritar](#1-favoritar)
  - [2. Favoritos primeiro](#2-favoritos-primeiro)
  - [3. Validação do formulário](#3-validação-do-formulário)
  - [⚠ Pegadinhas](#-pegadinhas-5)

---

## Como rodar

```bash
cd "projeto 1A"      # aspas por causa do espaço
python servidor.py
```

- ⚠ Rodar **de dentro** da pasta `projeto 1A`: o `Database('banco')` cria o `banco.db` na pasta onde o terminal está
- Abrir **http://localhost:8080** em **aba anônima**
- Mudou arquivo `.py`? → **Ctrl+C** e roda de novo (o servidor não recarrega sozinho)
- Mudou só HTML? → só recarregar a página (o `load_template` lê o arquivo a cada pedido)
- O terminal imprime cada requisição que chega → use para debugar (ver rota e método)

## Mapa dos arquivos

| Arquivo | O que faz |
|---|---|
| `servidor.py` | Recebe a requisição, descobre a rota e chama a função certa do `views.py` |
| `views.py` | Uma função por página/ação. Monta o HTML ou processa o POST e devolve a resposta |
| `utils.py` | Ferramentas: `extract_route`, `read_file`, `load_template`, `build_response` |
| `database.py` | Banco SQLite: classe `Database` + dataclass `Note` |
| `templates/` | `index.html`, `components/note.html`, `edit.html`, `delete.html`, `404.html` |
| `getit.css`, `getit.js`, `img/` | Arquivos estáticos (devolvidos direto pelo `is_file()`) |
| `banco.db` | Arquivo do banco (no repo do 1A estava no `.gitignore`; no repo da prova foi commitado) |

---

# Parte 0 — A base: `servidor.py` e `utils.py`

📖 Site: Handout Get-it partes 1 a 4 → https://barbaratieko.github.io/tecweb/aulas/01-getit/

## Conceitos

O **navegador** (cliente) pede, o **servidor** responde. Os dois conversam em **HTTP**, que é só texto.

A primeira linha da requisição tem **método** e **rota**:

```
GET /edit/3 HTTP/1.1
```

| Método | Quando acontece |
|---|---|
| **GET** | Digitar URL, clicar em link `<a href>`, navegador buscando CSS/JS/imagem |
| **POST** | Enviar `<form method="post">`. Os dados vêm no **corpo**, depois de uma linha em branco |

Formato da resposta:

```
HTTP/1.1 200 OK      ← linha de status
Location: /          ← headers (opcional)
                     ← linha em branco (obrigatória)
<html>...</html>     ← corpo
```

| Código | Significado | Uso no projeto |
|---|---|---|
| 200 OK | Deu certo | Mostrar página ou arquivo |
| 303 See Other | Vá para outro lugar (`Location`) | Depois de um POST, voltar para `/` |
| 404 Not Found | Não existe | Rota desconhecida |

`str` → `.encode()` → `bytes` (para enviar). `bytes` → `.decode()` → `str` (para ler).

## `servidor.py`

### 🔹 Só reconhecer (nunca muda)

- `socket`, `bind`, `listen` → ligam o servidor na porta 8080
- `while True` + `accept()` → espera o navegador conectar (uma volta = uma requisição)
- `recv(1024).decode()` → lê a requisição como string
- `print(request)` → mostra a requisição no terminal
- `sendall(response)` + `close()` → envia a resposta (tem que ser **bytes**) e fecha

### 🔸 Precisa entender

**Import das views** (toda função nova do `views.py` entra aqui):

```python
from views import index, delete, edit, confirm_delete, not_found, favorite
```

**Roteamento** (testado de cima para baixo, para no primeiro verdadeiro):

```python
route = extract_route(request)
filepath = CUR_DIR / route          # "/" do Path junta caminhos

if filepath.is_file():              # arquivo que existe (css, js, img)
    response = build_response() + read_file(filepath)
elif route == '':                   # página principal
    response = index(request)
elif route.startswith('delete/'):   # startswith porque a rota tem o id
    if request.startswith('POST'):
        response = delete(request)          # clicou "Sim" (form POST)
    else:
        response = confirm_delete(request)  # clicou na lixeira (link GET)
elif route.startswith('edit/'):
    response = edit(request)        # GET/POST tratado dentro da função
elif route.startswith('fav/'):
    response = favorite(request)
else:
    response = not_found(request)   # 404
```

Por que `is_file()` vem primeiro: ao abrir a home, o navegador faz vários pedidos
(`/`, `/getit.css`, `/img/logo-getit.png`, `/getit.js`...). Os arquivos precisam ser
devolvidos direto, senão caem no `else` (404).

> `GET /favicon.ico` caindo no 404 no terminal é normal (é o navegador procurando o ícone da aba).

## `utils.py`

Na prova você **não edita** essas funções, só **chama** `load_template` e `build_response`.

| Função | Exemplo | Devolve |
|---|---|---|
| `extract_route(request)` | `"GET /edit/3 HTTP/1.1"` | `'edit/3'` (home = `''`) |
| `read_file(filepath)` | `img/fav.png` | bytes do arquivo (modo `'rb'`) |
| `load_template(nome)` | `'edit.html'` | string do arquivo em `templates/` |
| `build_response(body, code, reason, headers)` | ver abaixo | bytes da resposta HTTP |

`load_data` e `add_note` são sobras da época do `notes.json`. Nada usa mais.

**Os 3 usos do `build_response`:**

```python
build_response(body=html)                                         # 200 — mostrar página
build_response(code=303, reason='See Other', headers='Location: /') # 303 — depois de POST
build_response(body=html, code=404, reason='Not Found')           # 404
```

## ✅ Rota nova: o que muda no `servidor.py`

```python
# 1. no import
from views import index, delete, edit, confirm_delete, not_found, favorite, nova_funcao

# 2. no roteamento, ANTES do else
    elif route == 'hoje/agora':
        response = nova_funcao(request)
```

(A função em si e o HTML ficam no `views.py` e em `templates/` → ver próximas partes.)

## ⚠ Pegadinhas

1. **Rota com barra no meio** (`/hoje/agora`, `/edit/3`): no HTML use caminhos **com barra no começo**
   (`/getit.css`, `/img/logo-getit.png`). Sem a barra, o navegador pede `/hoje/getit.css` → 404 → sem estilo.
2. **Toda view retorna `build_response(...)`**. String pura quebra o `sendall`.
3. **Função nova não aparece?** Confere se entrou no `from views import ...` e se reiniciou o servidor.
4. **O `elif` novo tem que vir antes do `else`**, senão nunca é alcançado.
5. **Aba anônima** para evitar cache.

---

# Parte 1 — Estilo da página

📖 Site: Desafio CSS → https://barbaratieko.github.io/tecweb/aulas/02-desafio-css/
📖 CSS (seletores, propriedades): https://developer.mozilla.org/pt-BR/docs/Web/CSS

## O que a tarefa pedia

Copiar `getit.css` e `getit.js` do Desafio CSS para a pasta do projeto e juntar o HTML
do desafio com o do handout (`index.html` e `components/note.html`). Mais encaixar do que programar.

## Como o CSS e o JS chegam no navegador

```html
<link rel="stylesheet" href="getit.css" />                <!-- no <head> -->
<script type="text/javascript" src="getit.js"></script>   <!-- no fim do <body> -->
```

O navegador lê essas linhas e faz `GET /getit.css` e `GET /getit.js` → caem no `is_file()` do servidor.

> Em página com rota com barra (`/edit/3`, `/hoje/agora`) usar `href="/getit.css"` (com barra).

## CSS básico

Sintaxe: `seletor { propriedade: valor; }`

```css
body  { background-color: #f7d736; }   /* seletor de tag */
.card { background-color: #ead3a7; }   /* seletor de classe → class="card" no HTML */
```

Estilo direto na tag (sem arquivo CSS, sem chaves):

```html
<body style="background-color: #FFC300">
```

### 🔹 Só reconhecer

- `getit.css` → estilos do Desafio CSS
- `getit.js` → aumenta a altura do textarea (`class="autoresize"`) e sorteia cor/rotação dos cards

## 🔸 Templates e `.format()` (precisa entender)

Os HTMLs em `templates/` têm **buracos** `{nome}` que o Python preenche.

| Template | Buracos |
|---|---|
| `index.html` | `{error}` (mensagem da validação), `{notes}` (todos os cards) |
| `components/note.html` | `{title}`, `{details}`, `{id}`, `{favorite_icon}` (molde de 1 card) |

Quem preenche é o `render_index` no `views.py`:

```python
note_template = load_template('components/note.html')     # molde de 1 card
notes_li = [
    note_template.format(title=nota.title, details=nota.content,
                         id=nota.id, favorite_icon=...)
    for nota in db.get_all()                               # 1 card por nota
]
notes = '\n'.join(notes_li)                                # junta todos os cards
body = load_template('index.html').format(notes=notes, error=error_html)
return build_response(body=body)
```

**Regra geral:** para levar um valor do Python para o HTML →
1. criar o buraco `{nome}` no template
2. passar `nome=valor` no `.format()`

## ⚠ Pegadinhas

1. **Buraco no template sem passar no `.format()`** → `KeyError: 'nome'`.
2. **Chaves de CSS dentro de um template quebram o `.format()`**, porque ele acha que é buraco:
   ```html
   <style> body { background-color: red; } </style>      <!-- ❌ quebra -->
   <style> body {{ background-color: red; }} </style>    <!-- ✅ chaves dobradas -->
   ```
   O `{{` vira `{` no resultado final. Alternativas mais seguras: deixar o CSS no `getit.css`
   ou usar `style="..."` na tag.
3. **CSS não aplicou?** Aba anônima (cache) e conferir o caminho do `href`.

---

# Parte 2 — Persistência de dados (SQLite)

📖 Site: Handout Persistência de dados → https://barbaratieko.github.io/tecweb/aulas/03-persistencia-de-dados/
📖 Docs: sqlite3 do Python → https://docs.python.org/3/library/sqlite3.html
📖 Docs: dataclasses → https://docs.python.org/3/library/dataclasses.html

## O que a tarefa pedia

Trocar o `notes.json` por um banco **SQLite**, usando o `database.py` do handout.

## Conceitos

O SQLite é um banco que mora inteiro em **um arquivo** (`banco.db`). Dentro dele, a tabela `note`:

| id | title | content | favorite |
|---|---|---|---|
| 1 | Mercado | Comprar leite | 0 |
| 2 | Receita | Sorvete de banana | 1 |

O `id` é gerado sozinho (`INTEGER PRIMARY KEY`) e é o que aparece nas rotas `/edit/3`, `/delete/3`.

| Comando SQL | O que faz | Método |
|---|---|---|
| `CREATE TABLE IF NOT EXISTS` | Cria a tabela se não existir | `__init__` |
| `INSERT INTO note (...) VALUES (...)` | Adiciona linha | `add` |
| `SELECT ... FROM note WHERE ...` | Busca linhas | `get_all`, `get` |
| `UPDATE note SET ... WHERE id = X` | Altera linha | `update`, `toggle_favorite` |
| `DELETE FROM note WHERE id = X` | Apaga linha | `delete` |

> ⚠ `UPDATE` ou `DELETE` **sem `WHERE`** afeta a tabela inteira.

## `database.py`

### Classe `Note` (formato de uma nota no Python)

```python
@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''
    favorite: bool = False
```

Criar: `Note(title='Mercado', content='Comprar leite')` · Acessar: `nota.id`, `nota.title`, `nota.content`, `nota.favorite`

### Classe `Database` (operações no banco)

```python
def __init__(self, nome):
    self.conn = sqlite3.connect(nome + '.db')   # abre/cria banco.db
    self.conn.execute("CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL, favorite INTEGER DEFAULT 0);")
```

**Padrão de método que ALTERA** (`add`, `update`, `delete`, `toggle_favorite`):

```python
def delete(self, note_id):
    self.conn.execute("DELETE FROM note WHERE id = " + str(note_id) + ";")
    self.conn.commit()          # commit = salvar. Sem ele, nada é gravado!
```

**Padrão de método que LÊ vários** (`get_all`):

```python
def get_all(self):
    notes = []
    cursor = self.conn.execute("SELECT id, title, content, favorite FROM note ORDER BY favorite DESC, id ASC")
    for linha in cursor:        # linha = tupla na ordem das colunas do SELECT
        notes.append(Note(id=linha[0], title=linha[1], content=linha[2], favorite=bool(linha[3])))
    return notes
```

**Padrão de método que LÊ um** (`get`):

```python
def get(self, note_id):
    cursor = self.conn.execute("SELECT id, title, content, favorite FROM note WHERE id = " + str(note_id) + ";")
    linha = cursor.fetchone()   # primeira linha ou None
    if linha is None:
        return None
    return Note(id=linha[0], title=linha[1], content=linha[2], favorite=bool(linha[3]))
```

| Método | Recebe | Devolve |
|---|---|---|
| `add(note)` | `Note` sem id | nada |
| `get_all()` | nada | lista de `Note` (favoritos primeiro) |
| `get(note_id)` | int | `Note` ou `None` |
| `update(note)` | `Note` com id | nada |
| `delete(note_id)` | int | nada |
| `toggle_favorite(note_id)` | int | nada (inverte 0 ↔ 1) |

## Como o `views.py` usa

```python
from database import Database, Note
db = Database('banco')          # no topo: uma conexão para todas as funções

db.get_all()                    # listar
db.add(Note(title=t, content=c))
db.get(3)
db.update(Note(id=3, title=t, content=c))
db.delete(3)
```

## ✅ Na prova

Quase sempre só **chamar** os métodos. Se precisar de algo novo, copiar o padrão:
`execute` + `commit` (altera) ou `execute` + `for`/`fetchone` (lê).

## ⚠ Pegadinhas e dicas

1. **Esqueceu o `commit()`** → a mudança some.
2. **Ordem dos índices**: `linha[0]`, `linha[1]`... seguem a ordem das colunas escritas no `SELECT`.
3. **Zerar as notas**: parar o servidor e apagar `banco.db` (é recriado sozinho).
4. No repositório original do 1A, `banco.db` está no `.gitignore` → clonado começa vazio. (No repo da prova ele foi commitado.)
5. `python exemplo_de_uso.py` → imprime todas as notas salvas.
6. **`banco.db` aparece em outra pasta / notas sumiram?** `sqlite3.connect('banco.db')` é um caminho
   **relativo**: o Python procura/cria o arquivo na pasta **onde o terminal está** ao rodar o programa.

   | Terminal está em | Comando | Banco usado |
   |---|---|---|
   | `projeto 1A/` | `python servidor.py` | `projeto 1A/banco.db` ✅ |
   | raiz do repositório | `python "projeto 1A/servidor.py"` | `banco.db` da raiz (criado novo, vazio) |

   - Causa comum sem perceber: **botão ▶ (play) do VS Code** com a raiz do repositório aberta → roda com o terminal na raiz.
     Foi assim que apareceu o `banco.db` solto na raiz do repositório da prova (é sobra, pode ignorar).
   - Templates e CSS funcionam de qualquer lugar porque usam `CUR_DIR` (pasta do próprio `.py`). **Só o banco depende do terminal.**
   - ✅ Na prova: rodar **pelo terminal**, `cd "projeto 1A"` e depois `python servidor.py`.
7. **Apóstrofo quebra o SQL** (`Copo d'água`), porque o SQL é montado grudando strings. Não testar com apóstrofo.

---

# Parte 3 — Apagar anotações

📖 Enunciado (tarefa 3 + conceito A): https://barbaratieko.github.io/tecweb/projetos/projeto1/projeto1a/
📖 Tag `<a>`: https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/a
📖 Tag `<form>`: https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/form

## O que a tarefa pedia

- **Tarefa 3 (B+):** botão em cada card para apagar a nota.
- **Conceito A:** antes de apagar, página de confirmação com a nota e os botões "Sim" (apaga e volta para home) e "Não" (só volta).

## Conceitos-chave

| Elemento HTML | Gera | Uso |
|---|---|---|
| `<a href="/rota">` | sempre **GET** | navegar, mostrar página |
| `<form method="post" action="/rota">` | **POST** para a rota do `action` | enviar dados, alterar o banco |
| `<form method="post">` sem `action` | POST para a **rota atual** | ex: form de criar nota no `index.html` |

**Regra: todo POST termina em 303** (`Location: /`). Assim o F5 não reenvia o POST.

### 🔸 Tirar o id da rota (padrão usado em delete, edit e favorite)

```python
route = extract_route(request)       # 'delete/3'
note_id = int(route.split('/')[-1])  # split → ['delete', '3'] · [-1] → '3' · int → 3
```

### 🔸 Tirar dados do corpo de um POST (padrão usado em index, edit)

```python
request = request.replace('\r', '')       # remove caracteres indesejados
partes = request.split('\n\n')            # headers e corpo separados por linha em branco
corpo = partes[1]                         # ex: 'titulo=Oi&detalhes=Tudo+bem'
params = {}
for chave_valor in corpo.split('&'):      # ['titulo=Oi', 'detalhes=Tudo+bem']
    chave, valor = chave_valor.split('=')
    params[chave] = unquote_plus(valor)   # 'Tudo+bem' → 'Tudo bem'
# params = {'titulo': 'Oi', 'detalhes': 'Tudo bem'}
```

(`from urllib.parse import unquote_plus` no topo do `views.py`)

#### De onde vem o `params`? (do formulário até o dicionário)

O `params` **não vem pronto**: é criado dentro da view, a partir do corpo do POST.

**1. HTML** — cada campo tem um `name`:

```html
<input name="titulo" ... />
<textarea name="detalhes" ...></textarea>
```

**2. Navegador** — junta tudo como `name=valor`, separado por `&`, no fim da requisição
(espaço vira `+`, acento vira `%C3%A1`...):

```
POST / HTTP/1.1
Host: localhost:8080
...
                                         ← linha em branco
titulo=Mercado&detalhes=Comprar+leite
```

**3. View** — o `for` monta o dicionário volta por volta:

| Volta | `chave_valor` | `chave` | `valor` | `params` depois |
|---|---|---|---|---|
| 1 | `'titulo=Mercado'` | `'titulo'` | `'Mercado'` | `{'titulo': 'Mercado'}` |
| 2 | `'detalhes=Comprar+leite'` | `'detalhes'` | `'Comprar+leite'` | `{'titulo': 'Mercado', 'detalhes': 'Comprar leite'}` |

`unquote_plus` desfaz a codificação (`+` → espaço, `%C3%A1` → `á`).

**4. Usar** — `params['titulo']` → `'Mercado'`

> 🔑 **As chaves do `params` são exatamente os `name` do HTML.** Não bateu → `KeyError`.
> (`params` é só um nome de variável; poderia ser `dados`.)

---

## ✅ Versão 1 — A que eu entreguei (conceito A, com confirmação)

A mesma rota `/delete/3` faz duas coisas: **GET mostra a confirmação, POST apaga.**

### Fluxo

| Clique | Requisição | Função | Resposta |
|---|---|---|---|
| Lixeira | `GET /delete/3` | `confirm_delete` | 200 + página "tem certeza?" |
| "Não" | `GET /` | `index` | 200 + home |
| "Sim" | `POST /delete/3` | `delete` | 303 → `Location: /` |
| (automático) | `GET /` | `index` | 200 + home sem a nota |

### `templates/components/note.html` (link da lixeira)

```html
<a href="/delete/{id}" class="card-delete" title="Apagar">
  <img src="img/lixeira.png" alt="Apagar"/>
</a>
```

### `servidor.py`

```python
elif route.startswith('delete/'):
    if request.startswith('POST'):
        response = delete(request)
    else:
        response = confirm_delete(request)
```

### `views.py`

```python
def confirm_delete(request):
    route = extract_route(request)
    note_id = int(route.split('/')[-1])

    nota = db.get(note_id)
    body = load_template('delete.html').format(id=nota.id, title=nota.title, content=nota.content)
    return build_response(body=body)


def delete(request):
    route = extract_route(request)
    note_id = route.split('/')[-1]
    db.delete(int(note_id))

    return build_response(code=303, reason='See Other', headers='Location: /')
```

### `templates/delete.html` (parte importante)

```html
<h3 class="confirm-card-title">{title}</h3>
<p class="confirm-card-content">{content}</p>
<p class="confirm-card-question">Tem certeza que deseja apagar essa anotação?</p>

<a class="btn btn-secondary" href="/">Não</a>              <!-- GET / → nada apagado -->
<form method="post" action="/delete/{id}">                  <!-- POST /delete/3 → apaga -->
  <button class="btn" type="submit">Sim</button>
</form>
```

(Caminhos do CSS e imagens com barra: `/getit.css`, `/img/logo-getit.png`, porque a rota tem barra.)

---

## Versão 2 — Com POST + input hidden (a outra opção do enunciado, sem confirmação)

O id vai no **corpo** do POST, e não na rota. A rota fica fixa: `/delete`.

| Clique | Requisição | Corpo | Função | Resposta |
|---|---|---|---|---|
| Lixeira | `POST /delete` | `id=3` | `delete` | 303 → `Location: /` |

`templates/components/note.html` (troca o link por um form):

```html
<form method="post" action="/delete">
  <input type="hidden" name="id" value="{id}" />   <!-- escondido: o id não aparece na tela -->
  <button type="submit" class="card-delete">
    <img src="/img/lixeira.png" alt="Apagar"/>
  </button>
</form>
```

`servidor.py` (rota fixa → `==` em vez de `startswith`):

```python
elif route == 'delete':
    response = delete(request)
```

`views.py` (lê o id do corpo, não da rota):

```python
def delete(request):
    request = request.replace('\r', '')
    corpo = request.split('\n\n')[1]           # 'id=3'
    params = {}
    for chave_valor in corpo.split('&'):
        chave, valor = chave_valor.split('=')
        params[chave] = unquote_plus(valor)

    db.delete(int(params['id']))
    return build_response(code=303, reason='See Other', headers='Location: /')
```

---

## ⚠ Pegadinhas

1. **Rota com id → `startswith`**; rota fixa → `==`.
2. **O id vem como texto** (`'3'`) → converter com `int()` antes de usar no banco.
3. **Link nunca gera POST.** Se precisa de POST, tem que ser `<form method="post">`.
4. **Esqueceu o `action`?** O form envia para a rota da página atual.
5. **O id não deve aparecer na tela** (enunciado). Na rota (`/delete/3`) ou em `type="hidden"` pode.

---

# Parte 4 — Editar anotações

📖 Enunciado (tarefa 4): https://barbaratieko.github.io/tecweb/projetos/projeto1/projeto1a/
📖 `<input>`: https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/input
📖 `<textarea>`: https://developer.mozilla.org/pt-BR/docs/Web/HTML/Element/textarea

## O que a tarefa pedia

- Botão em cada card → **página nova** de edição
- Formulário **já preenchido** com título e conteúdo
- "Cancelar" → volta para home · "Salvar" → grava no banco e volta para home
- Método novo no `database.py` que recebe id e devolve um `Note` → `get(note_id)`

Junta tudo: id na rota (Parte 3) + template com `.format()` (Parte 1) + corpo do POST (Parte 3) + banco (Parte 2).

## Fluxo

| Clique | Requisição | Qual metade do `edit` | Resposta |
|---|---|---|---|
| Lápis | `GET /edit/3` | GET: `db.get` + `edit.html` | 200 + formulário preenchido |
| "Cancelar" | `GET /` | (vai para `index`) | home, nada mudou |
| "Salvar" | `POST /edit/3` · corpo `titulo=...&detalhes=...` | POST: `db.update` | 303 → `Location: /` |
| (automático) | `GET /` | (vai para `index`) | home com a nota editada |

## `templates/components/note.html` (link do lápis)

```html
<a href="/edit/{id}" class="card-edit" title="Editar">
  <img src="img/edit.png" alt="Editar"/>
</a>
```

## `servidor.py`

```python
elif route.startswith('edit/'):
    response = edit(request)       # GET/POST separado DENTRO da função
```

> Diferente do delete, onde o `if POST` fica no `servidor.py`. Os dois jeitos funcionam.

## `views.py` — função com duas metades

```python
def edit(request):
    route = extract_route(request)
    note_id = int(route.split('/')[-1])

    if request.startswith('POST'):
        # ---- METADE POST: clicou em "Salvar" ----
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[chave] = unquote_plus(valor)

        nota_editada = Note(id=note_id, title=params['titulo'], content=params['detalhes'])
        db.update(nota_editada)
        return build_response(code=303, reason='See Other', headers='Location: /')

    # ---- METADE GET: clicou no lápis ----
    nota = db.get(note_id)
    body = load_template('edit.html').format(id=nota.id, title=nota.title, content=nota.content)
    return build_response(body=body)
```

**Molde para qualquer página com formulário:**

```python
def minha_view(request):
    if request.startswith('POST'):
        # ler corpo → params
        # salvar no banco
        return build_response(code=303, reason='See Other', headers='Location: /')
    # GET: montar HTML
    return build_response(body=load_template('pagina.html').format(...))
```

## `templates/edit.html` (parte importante)

```html
<form class="edit-card" method="post" action="/edit/{id}">
  <input class="edit-card-title" type="text" name="titulo" value="{title}" />
  <textarea class="edit-card-content" name="detalhes">{content}</textarea>

  <a class="btn btn-secondary" href="/">Cancelar</a>
  <button class="btn" type="submit">Salvar</button>
</form>
```

| Detalhe | Por quê |
|---|---|
| `<input ... value="{title}">` | texto inicial do input vai no **atributo `value`** |
| `<textarea>{content}</textarea>` | texto inicial do textarea vai **entre as tags** |
| `name="titulo"`, `name="detalhes"` | viram as chaves do corpo → `params['titulo']`, `params['detalhes']` |
| `action="/edit/{id}"` | POST vai para a rota com o id → metade POST sabe qual nota salvar |

## `database.py`

```python
def get(self, note_id):          # método novo pedido pelo enunciado
    cursor = self.conn.execute("SELECT id, title, content, favorite FROM note WHERE id = " + str(note_id) + ";")
    linha = cursor.fetchone()
    if linha is None:
        return None
    return Note(id=linha[0], title=linha[1], content=linha[2], favorite=bool(linha[3]))

def update(self, entry):
    self.conn.execute("UPDATE note SET title = '" + entry.title + "', content = '" + entry.content + "' WHERE id = " + str(entry.id) + ";")
    self.conn.commit()
```

## ⚠ Pegadinhas

1. **`Note` sem `id` no update** → o banco não sabe qual linha alterar.
2. **`name` do HTML ≠ chave em `params[...]`** → `KeyError`.
3. **`value` só no `<input>`**. No `<textarea>` o texto vai entre as tags.
4. **Esqueceu o `return` dentro do `if POST`** → o código segue e roda a metade GET também.
5. **Rota com barra** (`/edit/3`) → CSS e imagens com barra no começo (`/getit.css`).

---

# Parte 5 — Página 404 (conceito A)

📖 Enunciado (conceito A): https://barbaratieko.github.io/tecweb/projetos/projeto1/projeto1a/
📖 Códigos de status HTTP: https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status

## O que o enunciado pedia

- Rota inexistente → servidor devolve `404.html`
- **Código HTTP também 404** (não 200)
- Mesmo estilo da página principal, mensagem amigável, link para home, imagem ilustrativa

## `servidor.py` — o `else` do roteamento

```python
    elif route.startswith('fav/'):
        response = favorite(request)
    else:
        response = not_found(request)     # nada bateu → 404
```

> Toda rota nova entra **antes** do `else`, senão nunca é alcançada.

## `views.py`

```python
def not_found(request):
    body = load_template('404.html')                          # sem .format(): não tem buraco
    return build_response(code=404, reason='Not Found', body=body)
```

Sem `code=404` a página aparece igual na tela, mas o navegador recebe `200 OK` → não atende o enunciado.

**Padrão de página sem buracos:** `build_response(body=load_template('pagina.html'))`

## `templates/404.html` (partes que atendem o enunciado)

```html
<link rel="stylesheet" href="/getit.css" />                    <!-- mesmo estilo, COM barra -->
<img src="/img/logo-getit.png" class="logo" />
...
<h1 class="not-found-title">Ops, essa página não existe</h1>    <!-- mensagem amigável -->
<a class="btn" href="/">Voltar para a página principal</a>      <!-- link para home -->
```

A 404 aparece em **qualquer** rota (`/a/b/c`), então os caminhos precisam ser absolutos (com `/`).

## 🔍 Conferir o código de status no navegador

**F12** (ou botão direito → Inspecionar) → aba **Network / Rede** → recarregar → coluna **Status**.
Serve para ver 200, 303, 404 de qualquer página.

## ⚠ Pegadinhas

1. **Id que não existe** (`/edit/999`, `/delete/999`): a rota **bate** com o `startswith`, então não cai no 404.
   `db.get(999)` devolve `None` → `nota.id` dá `AttributeError` → **o servidor cai**.
2. **Erro dentro de uma view derruba o servidor inteiro.** Página parou de carregar do nada?
   → olhar o **terminal**. Última linha do traceback = o erro; linha de cima = arquivo e linha.
   → corrigir e rodar `python servidor.py` de novo.
3. **Esqueceu `code=404`** → aparece certo na tela, mas o status é 200.

---

# Parte 6 — Extras do A+ (favoritar, ordenar, validar)

📖 Enunciado (conceito A+): https://barbaratieko.github.io/tecweb/projetos/projeto1/projeto1a/
📖 SQL ORDER BY: https://www.sqlite.org/lang_select.html#orderby

## O que o A+ pedia

| Requisito | Onde está |
|---|---|
| Lógica de deletar/editar/favoritar no `views.py` | já atendido: views fazem tudo |
| `servidor.py` só direciona rotas | já atendido: só `if/elif` chamando views |
| Favoritar | link `/fav/{id}` + `toggle_favorite` |
| Favoritos primeiro | `ORDER BY favorite DESC` |
| Validação de nota vazia | metade POST do `index` + `{error}` |

## 🔸 If ternário (aparece várias vezes)

```python
valor_se_verdadeiro if condição else valor_se_falso

'fav.png' if nota.favorite else 'notfav.png'
0 if nota.favorite else 1
```

---

## 1. Favoritar

### Fluxo

| Clique | Requisição | Função | Resposta |
|---|---|---|---|
| Estrela | `GET /fav/3` | `favorite` → `db.toggle_favorite(3)` | 303 → `Location: /` |
| (automático) | `GET /` | `index` | home com a estrela trocada e a nota reordenada |

### `templates/components/note.html`

```html
<a href="/fav/{id}" class="card-fav" title="Favoritar">
  <img src="img/{favorite_icon}" alt="Favoritar"/>     <!-- a imagem também é um buraco -->
</a>
```

### `views.py` — no `render_index`, o Python escolhe a imagem

```python
note_template.format(..., favorite_icon='fav.png' if nota.favorite else 'notfav.png')
```

> 🔑 **Padrão: o Python escolhe um valor e passa para o template pelo `.format()`.**
> O HTML não decide nada, só mostra o que recebeu.

### `servidor.py`

```python
elif route.startswith('fav/'):
    response = favorite(request)
```

### `views.py`

```python
def favorite(request):
    route = extract_route(request)
    note_id = int(route.split('/')[-1])
    db.toggle_favorite(note_id)
    return build_response(code=303, reason='See Other', headers='Location: /')
```

### `database.py`

Coluna nova (SQLite não tem booleano → `0` = não, `1` = sim):

```sql
CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL, favorite INTEGER DEFAULT 0);
```

Na `Note`: `favorite: bool = False` · Na leitura: `favorite=bool(linha[3])`

```python
def toggle_favorite(self, note_id):
    nota = self.get(note_id)
    novo_valor = 0 if nota.favorite else 1       # inverte (interruptor)
    self.conn.execute("UPDATE note SET favorite = " + str(novo_valor) + " WHERE id = " + str(note_id) + ";")
    self.conn.commit()
```

---

## 2. Favoritos primeiro

No `get_all`:

```sql
SELECT id, title, content, favorite FROM note ORDER BY favorite DESC, id ASC
```

- `favorite DESC` → decrescente: `1` (favoritas) antes de `0`
- `, id ASC` → desempate: dentro de cada grupo, ordem de criação

---

## 3. Validação do formulário

### `views.py` — metade POST do `index`

```python
titulo = params.get('titulo', '').strip()      # .get: não dá erro se faltar · .strip: tira espaços
detalhes = params.get('detalhes', '').strip()

if not titulo or not detalhes:                 # string vazia = falso
    return render_index(error='Preencha o título e o conteúdo antes de criar a nota.')   # 200, NÃO 303

nova_nota = Note(title=titulo, content=detalhes)
db.add(nova_nota)
return build_response(code=303, reason='See Other', headers='Location: /')
```

Por que **200 e não 303** no erro: a mensagem precisa aparecer na tela. Com 303 o navegador
iria para a home e a mensagem se perderia.

### `views.py` — `render_index` (usado no GET e na validação)

```python
def render_index(error=''):                    # padrão '' = sem mensagem
    note_template = load_template('components/note.html')
    notes_li = [note_template.format(...) for nota in db.get_all()]
    notes = '\n'.join(notes_li)

    error_html = f'<p class="form-error">{error}</p>' if error else ''
    body = load_template('index.html').format(notes=notes, error=error_html)
    return build_response(body=body)
```

| Chamada | `{error}` no HTML vira |
|---|---|
| `render_index()` | nada |
| `render_index(error='Preencha...')` | `<p class="form-error">Preencha...</p>` |

### `templates/index.html`

```html
<form class="form-card" method="post">
  {error}
  ...
</form>
```

---

## ⚠ Pegadinhas

1. **Coluna nova no banco não aparece** (`no such column`): o `CREATE TABLE IF NOT EXISTS` não altera
   tabela que já existe → parar o servidor, **apagar `banco.db`**, rodar de novo.
2. **Validação com 303** → a mensagem some. Erro de validação = página normal (200).
3. **Sem `.strip()`** → dá para criar nota só com espaços.
4. **Buraco novo no `index.html`** (`{error}`) → passar em **todo** `.format()` desse template.