# =============================================================================
# views.py — AS PÁGINAS / AÇÕES
# Uma função por página ou ação. Cada função recebe a requisição (string)
# e SEMPRE devolve build_response(...) (bytes).
# Toda a lógica (criar, apagar, editar, favoritar) fica AQUI (requisito do A+).
#
# Molde de view com formulário (📖 README → Parte 4):
#     if request.startswith('POST'):  ler corpo → params → salvar → return 303
#     (GET) montar HTML com load_template + .format → return build_response(body=...)
# =============================================================================

from urllib.parse import unquote_plus   # desfaz a codificação do form: '+' → ' ', '%C3%A1' → 'á'
from utils import load_template, build_response, extract_route
from database import Database, Note

# UMA conexão com o banco, criada quando o servidor importa este arquivo.
# Todas as funções usam esse mesmo "db". Cria o banco.db se não existir.
# 📖 README → Parte 2 → "Como o views.py usa"
db = Database('banco')


# -----------------------------------------------------------------------------
# PÁGINA PRINCIPAL — rota ''  (GET mostra | POST cria nota)
# 📖 README → Parte 3 → "De onde vem o params?" e Parte 6 → "Validação"
# -----------------------------------------------------------------------------
def index(request):
    # A requisição sempre começa com o método: 'GET ...' ou 'POST ...'
    if request.startswith('POST'):
        # ---- LER O CORPO DO POST (padrão que se repete no edit) ----
        request = request.replace('\r', '')  # remove caracteres indesejados
        partes = request.split('\n\n')       # headers e corpo são separados por uma linha em branco
        corpo = partes[1]                    # ex: 'titulo=Mercado&detalhes=Comprar+leite'
        params = {}                          # dicionário criado AQUI
        for chave_valor in corpo.split('&'):          # ['titulo=Mercado', 'detalhes=Comprar+leite']
            chave, valor = chave_valor.split('=')     # 'titulo', 'Mercado'
            params[chave] = unquote_plus(valor)       # 'Comprar+leite' → 'Comprar leite'
        # As chaves do params são os name="..." do formulário no index.html

        # ---- VALIDAÇÃO (A+) ----
        # .get(chave, '') → não dá erro se a chave faltar
        # .strip() → tira espaços das pontas (nota só com espaços não passa)
        titulo = params.get('titulo', '').strip()
        detalhes = params.get('detalhes', '').strip()

        # string vazia = falso → "se o título OU o conteúdo estiver vazio"
        if not titulo or not detalhes:
            # NÃO salva e devolve a página com a mensagem (200, NÃO 303),
            # senão o redirecionamento faria a mensagem sumir
            return render_index(error='Preencha o título e o conteúdo antes de criar a nota.')

        # ---- SALVAR NO BANCO ----
        nova_nota = Note(title=titulo, content=detalhes)   # sem id: o banco gera sozinho
        db.add(nova_nota)

        # Todo POST termina em 303 → navegador faz GET / (F5 não reenvia o form)
        return build_response(code=303, reason='See Other', headers='Location: /')

    # GET: só mostra a página
    return render_index()


# -----------------------------------------------------------------------------
# CONFIRMAR APAGAR — GET /delete/<id>  (clicou na lixeira)
# 📖 README → Parte 3 — Apagar anotações (Versão 1)
# -----------------------------------------------------------------------------
def confirm_delete(request):
    # ---- TIRAR O ID DA ROTA (padrão que se repete em delete, edit, favorite) ----
    route = extract_route(request)          # 'delete/3'
    note_id = int(route.split('/')[-1])     # split → ['delete', '3'] · [-1] = último → '3' · int → 3

    nota = db.get(note_id)                  # busca a nota (⚠ id inexistente → None → erro abaixo derruba o servidor)
    # Preenche os buracos do delete.html para mostrar a nota que vai ser apagada
    body = load_template('delete.html').format(id=nota.id, title=nota.title, content=nota.content)
    return build_response(body=body)        # 200


# -----------------------------------------------------------------------------
# APAGAR — POST /delete/<id>  (clicou "Sim" no delete.html)
# 📖 README → Parte 3 — Apagar anotações
# -----------------------------------------------------------------------------
def delete(request):
    route = extract_route(request)          # 'delete/3'
    note_id = route.split('/')[-1]          # '3' (texto)
    db.delete(int(note_id))                 # int() antes de mandar pro banco

    return build_response(code=303, reason='See Other', headers='Location: /')


# -----------------------------------------------------------------------------
# EDITAR — /edit/<id>   GET mostra o formulário | POST salva
# 📖 README → Parte 4 — Editar anotações
# -----------------------------------------------------------------------------
def edit(request):
    route = extract_route(request)          # 'edit/3'
    note_id = int(route.split('/')[-1])     # 3

    if request.startswith('POST'):
        # ---- METADE POST: clicou em "Salvar" ----
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]                   # 'titulo=...&detalhes=...'
        params = {}
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[chave] = unquote_plus(valor)

        # Note COM id → o banco sabe QUAL linha alterar
        # params['titulo'] e params['detalhes'] = os name="..." do edit.html (não bateu → KeyError)
        nota_editada = Note(id=note_id, title=params['titulo'], content=params['detalhes'])
        db.update(nota_editada)

        # return dentro do if → a metade GET abaixo NÃO roda
        return build_response(code=303, reason='See Other', headers='Location: /')

    # ---- METADE GET: clicou no lápis ----
    nota = db.get(note_id)
    # Formulário vem preenchido: {title} vai no value do input, {content} dentro do textarea
    body = load_template('edit.html').format(id=nota.id, title=nota.title, content=nota.content)
    return build_response(body=body)


# -----------------------------------------------------------------------------
# 404 — qualquer rota que não bateu no servidor.py
# 📖 README → Parte 5 — Página 404
# -----------------------------------------------------------------------------
def not_found(request):
    body = load_template('404.html')        # sem .format(): o 404.html não tem buracos
    # code=404 é obrigatório: sem ele a página aparece igual, mas o status seria 200
    return build_response(code=404, reason='Not Found', body=body)


# -----------------------------------------------------------------------------
# FAVORITAR — GET /fav/<id>  (clicou na estrela)
# 📖 README → Parte 6 → "1. Favoritar"
# -----------------------------------------------------------------------------
def favorite(request):
    route = extract_route(request)
    note_id = int(route.split('/')[-1])
    db.toggle_favorite(note_id)             # inverte: favorita ↔ não favorita

    # Veio de um link (GET), mas altera o banco → também volta para home com 303
    return build_response(code=303, reason='See Other', headers='Location: /')


# -----------------------------------------------------------------------------
# MONTA A PÁGINA PRINCIPAL — usada no GET do index E na validação (com erro)
# error='' é o padrão → render_index() = sem mensagem
# 📖 README → Parte 1 → "Templates e .format()" e Parte 6 → "render_index"
# -----------------------------------------------------------------------------
def render_index(error=''):
    note_template = load_template('components/note.html')   # molde de UM card (string com buracos)

    # List comprehension: um card preenchido para cada nota do banco
    # (db.get_all já vem ordenado: favoritas primeiro)
    notes_li = [
        note_template.format(
            title=nota.title,
            details=nota.content,
            id=nota.id,
            # If ternário: valor_se_verdadeiro if condição else valor_se_falso
            # 🔑 O Python ESCOLHE o valor e passa para o template pelo .format()
            favorite_icon='fav.png' if nota.favorite else 'notfav.png',
        )
        for nota in db.get_all()
    ]
    notes = '\n'.join(notes_li)             # junta todos os cards num texto só

    # Ternário de novo: com mensagem → parágrafo HTML | sem mensagem → nada
    error_html = f'<p class="form-error">{error}</p>' if error else ''

    # Encaixa os cards no buraco {notes} e o erro no buraco {error} do index.html
    # ⚠ Buraco no template sem passar aqui → KeyError
    body = load_template('index.html').format(notes=notes, error=error_html)
    return build_response(body=body)
