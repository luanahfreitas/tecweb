# =============================================================================
# utils.py — FERRAMENTAS
# Funções auxiliares usadas pelo servidor.py e pelo views.py.
# Na prova: NÃO precisa editar. Só CHAMAR load_template e build_response.
# 📖 README_1A.md → "Parte 0 — A base" → "utils.py"
# =============================================================================

import json
from pathlib import Path

CUR_DIR = Path(__file__).parent  # pasta do projeto


def extract_route(request):
    """Tira a rota da requisição, sem a barra inicial.
    "GET /edit/3 HTTP/1.1" → 'edit/3'   |   "GET / HTTP/1.1" → ''
    """
    first_line = request.split('\n')[0]   # 1ª linha: 'GET /edit/3 HTTP/1.1'
    route = first_line.split(' ')[1]     # corta nos espaços → ['GET', '/edit/3', 'HTTP/1.1'] → '/edit/3'
    return route[1:]                     # fatiamento: pula o 1º caractere (a barra) → 'edit/3'


def read_file(filepath):
    """Lê um arquivo e devolve BYTES.
    Modo 'rb' = read binary, porque imagens não são texto.
    """
    with open(filepath, 'rb') as f:      # with = abre e fecha sozinho no fim do bloco
        return f.read()


# ---- SOBRA DO HANDOUT (era usada com data/notes.json; nada usa depois do SQLite)
def load_data(filename):
    filepath = CUR_DIR / 'data' / filename
    with open(filepath, encoding='utf-8') as f:
        return json.load(f)              # texto JSON → lista/dicionário Python


def load_template(filename):
    """Lê um HTML da pasta templates/ e devolve STRING.
    load_template('edit.html') → conteúdo de templates/edit.html
    O HTML tem "buracos" com chaves que as views preenchem com .format().
    📖 README → Parte 1 → "Templates e .format()"
    """
    filepath = CUR_DIR / 'templates' / filename
    with open(filepath, encoding='utf-8') as f:   # utf-8 para ler acentos certo
        return f.read()


# ---- SOBRA DO HANDOUT (adicionava nota no notes.json; nada usa depois do SQLite)
def add_note(titulo, detalhes):
    filepath = CUR_DIR / 'data' / 'notes.json'
    notas = load_data('notes.json')
    notas.append({'titulo': titulo, 'detalhes': detalhes})
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(notas, f, ensure_ascii=False, indent=2)


def build_response(body='', code=200, reason='OK', headers=''):
    """Monta a resposta HTTP e SEMPRE devolve BYTES.

    Formato:
        HTTP/1.1 <code> <reason>   ← linha de status
        <headers>                  ← opcional
                                   ← linha em branco (obrigatória)
        <body>                     ← corpo (opcional)

    Os 3 usos do projeto:
        build_response(body=html)                                          → 200, mostrar página
        build_response(code=303, reason='See Other', headers='Location: /') → depois de POST, volta p/ home
        build_response(body=html, code=404, reason='Not Found')            → 404
    📖 README → Parte 0 → "Os 3 usos do build_response"
    """
    # Parâmetros têm valor padrão (depois do =): se não passar, usa o padrão.
    if isinstance(body, str):            # body é string? converte para bytes
        body = body.encode()             # (assim aceita tanto str quanto bytes)

    response_line = f'HTTP/1.1 {code} {reason}\n'
    if headers:                          # string vazia conta como falso
        headers = headers + '\n'
    response = response_line + headers + '\n'   # + linha em branco que separa do corpo
    return response.encode() + body              # cabeçalho (bytes) + corpo (bytes)
