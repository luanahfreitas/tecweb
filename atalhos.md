# Atalhos e coisas que não posso esquecer — TecWeb

> ## 🚨 AVISO — FALAR COM A PROFESSORA ANTES DA PROVA
> O Projeto 1B está rodando na **porta 8000** (orientação da professora por causa de um erro).

📖 Site da disciplina: https://barbaratieko.github.io/tecweb/

## 📑 Sumário

- [Repositório da prova](#repositório-da-prova)
- [Checklist antes de começar a prova](#checklist-antes-de-começar-a-prova)
- [Projeto 1A — Get-it na mão](#projeto-1a--get-it-na-mão)
- [Projeto 1B — Django](#projeto-1b--django)
- [Portas](#portas)
- [Ambiente virtual (venv) — Mac](#ambiente-virtual-venv--mac)
- [Django — comandos](#django--comandos)
- [Docker / PostgreSQL (Projeto 1B, tarefa 3 — 🔹 só reconhecer)](#docker--postgresql-projeto-1b-tarefa-3---só-reconhecer)
- [Deploy (Projeto 1B, tarefa 4 — 🔹 só reconhecer)](#deploy-projeto-1b-tarefa-4---só-reconhecer)
- [Terminal — básico (Mac)](#terminal--básico-mac)

---

## Repositório da prova

**`BarbaraTieko/tecweb-26-2-avaliacao-intermediaria-luanahf`** (privado)

```
tecweb-26-2-avaliacao-intermediaria-luanahf/   ← raiz: aqui ficam o .git e os commits
├── projeto 1A/      ← código do 1A (tem o banco.db CERTO dentro)
├── projeto 1B/      ← código do 1B (SQLite + DEBUG=True + env/)
├── .gitignore
├── README.md
└── banco.db         ← sobra: criado quando o 1A foi rodado da raiz. IGNORAR (não é o usado)
```

- Pastas com **espaço** no nome → sempre `cd "projeto 1A"` / `cd "projeto 1B"`
- Comandos **git** funcionam de qualquer pasta dentro do repositório

## Checklist antes de começar a prova

- [ ] Avisar a professora sobre a porta 8000 do Projeto 1B
- [ ] Rodar o 1A de dentro de `projeto 1A` (usa o `projeto 1A/banco.db`, o certo)
- [ ] Ligar o 1A e o 1B e abrir no navegador (aba anônima) para ver se estão funcionando
- [ ] Deixar abertos: site da disciplina, READMEs, enunciado da prova

---

## Projeto 1A — Get-it na mão

📖 README_1A.md

```bash
cd "projeto 1A"              # ASPAS por causa do espaço no nome
python servidor.py
```

> ⚠ **Rodar SEMPRE de dentro da pasta `projeto 1A`.** O banco é aberto com `Database('banco')`,
> que cria/usa o `banco.db` na pasta **onde o terminal está**, não na pasta do projeto.
> Rodar de outro lugar (ex: `python "projeto 1A/servidor.py"` da raiz) cria um `banco.db` novo e vazio ali.
> **Não usar o botão ▶ (play) do VS Code** com a raiz aberta: ele roda com o terminal na raiz → usa o banco errado.
> (Foi assim que surgiu o `banco.db` solto na raiz do repositório.) 📖 README_1A → Parte 2 → Pegadinhas

| | |
|---|---|
| Endereço | **http://localhost:8080** (aba anônima) |
| Porta definida em | `servidor.py` → `SERVER_PORT = 8080` |
| Mudou `.py` | **Ctrl+C** e rodar de novo (não reinicia sozinho) |
| Mudou só HTML | só recarregar a página |
| Parar | **Ctrl+C** |
| Zerar as notas | parar o servidor e apagar `banco.db` |
| Ver notas salvas | `python exemplo_de_uso.py` |

---

## Projeto 1B — Django

📖 README_1B.md

```bash
cd "projeto 1B"              # ASPAS por causa do espaço no nome
source env/bin/activate      # ativar o ambiente virtual (Mac)
python manage.py runserver
```

| | |
|---|---|
| Endereço | **http://localhost:8000** |
| Porta definida em | nenhum arquivo do projeto: é o padrão do `runserver` do Django |
| Mudou `.py` | reinicia **sozinho** |
| Parar | **Ctrl+C** |
| Banco na prova | SQLite (`db.sqlite3`), `DEBUG = True` |

> ⚠ Não renomear nem mover a pasta `projeto 1B` (quebra o ambiente virtual).

---

## Portas

| Comando | Abre em |
|---|---|
| `python servidor.py` (1A) | `localhost:8080` |
| `python manage.py runserver` (1B) | `localhost:8000` |
| `python manage.py runserver 8080` | `localhost:8080` (porta escolhida no comando) |

- 1A e 1B podem rodar **ao mesmo tempo**, em dois terminais (portas diferentes).
- `Error: That port is already in use.` / `Address already in use` → tem outro servidor aberto nessa porta:
  **Ctrl+C** no outro terminal, ou rodar em outra porta.

---

## Ambiente virtual (venv) — Mac

📖 Site: Material Auxiliar → https://barbaratieko.github.io/tecweb/auxiliar/venv/

| Ação | Comando |
|---|---|
| Criar | `python3 -m venv env` |
| Ativar | `source env/bin/activate` |
| Saber se está ativo | aparece `(env)` no começo da linha do terminal |
| Instalar dependências | `pip install -r requirements.txt` |
| Salvar dependências | `pip freeze > requirements.txt` |
| Desativar | `deactivate` |

> Rodar `python manage.py ...` **sem** o `(env)` → `ModuleNotFoundError: No module named 'django'`.

---

## Django — comandos

📖 Handout Django: https://barbaratieko.github.io/tecweb/aulas/04-django/

(Sempre com o ambiente ativado e dentro da pasta que tem o `manage.py`.)

| Comando | Quando usar |
|---|---|
| `python manage.py runserver` | ligar o servidor |
| `python manage.py makemigrations` | **depois de mexer no `models.py`** (gera o arquivo de migração) |
| `python manage.py migrate` | logo depois do `makemigrations` (aplica no banco) |
| `python manage.py createsuperuser` | criar login para `localhost:8000/admin` |
| `python manage.py showmigrations notes` | ver quais migrações foram aplicadas (`[X]`) e quais estão pendentes (`[ ]`) |

> 🔑 Mexeu no `models.py` → `makemigrations` → `migrate`. Sempre os dois, nessa ordem.

> ⚠ **`makemigrations` perguntou "Select an option"** (campo novo em tabela com linhas, ex: `ForeignKey`):
> - existe linha na outra tabela (ex: id 1) → `1` Enter, `1` Enter
> - não existe → `2` Enter, colocar `null=True` no campo, rodar de novo
> - 📖 README_1B → Parte 2 → Passo 3

---

## Docker / PostgreSQL (Projeto 1B, tarefa 3 — 🔹 só reconhecer)

📖 https://barbaratieko.github.io/tecweb/aulas/05-bd/ · 📖 README_1B → Parte 3

| Ação | Comando |
|---|---|
| Ligar o Postgres | `docker run --rm --name pg-docker -e POSTGRES_PASSWORD=escolhaumasenha -d -p 5432:5432 -v "$HOME/docker/volumes/postgres:/var/lib/postgresql/data" postgres` |
| Ver containers rodando | `docker ps` |
| Parar o container | `docker stop pg-docker` |

> Na prova: **não precisa** (a pasta `projeto 1B` usa SQLite).

---

## Deploy (Projeto 1B, tarefa 4 — 🔹 só reconhecer)

📖 https://barbaratieko.github.io/tecweb/aulas/06-deploy/ · 📖 README_1B → Parte 4

🌐 https://tecweb-2026-2-projeto1b-so8f.onrender.com

| Ação | Comando |
|---|---|
| Instalar libs de deploy | `pip install gunicorn whitenoise dj-database-url psycopg2` |
| Atualizar requirements | `pip freeze > requirements.txt` |
| Juntar estáticos | `python manage.py collectstatic` |
| Start no Render | `gunicorn getit.wsgi` |

> Deploy = `DEBUG = False` + `ALLOWED_HOSTS` + WhiteNoise + `STATIC_ROOT` + `dj_database_url` + `gunicorn`.

---

## Terminal — básico (Mac)

| Comando | O que faz |
|---|---|
| `pwd` | mostra em qual pasta estou |
| `ls` | lista arquivos da pasta |
| `cd pasta` | entra na pasta (`cd "nome com espaço"`) |
| `cd ..` | volta uma pasta |
| **Ctrl+C** | para o programa rodando (servidor) |
| **↑** (seta para cima) | repete o comando anterior |
| **Tab** | completa o nome de pasta/arquivo |

