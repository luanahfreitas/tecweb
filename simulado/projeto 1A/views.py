from urllib.parse import unquote_plus
from utils import load_template, build_response, extract_route
from database import Database, Note

# [SIMULADO 1.1] ✅ imports para a data (código do enunciado)
import locale
import datetime

# [SIMULADO 1.2] ✅ import para sortear a cor
import random

db = Database('banco')

def index(request):
    if request.startswith('POST'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        for chave_valor in corpo.split('&'):
            chave, valor = chave_valor.split('=')
            params[chave] = unquote_plus(valor)

        titulo = params.get('titulo', '').strip()
        detalhes = params.get('detalhes', '').strip()

        if not titulo or not detalhes:
            return render_index(error='Preencha o título e o conteúdo antes de criar a nota.')

        nova_nota = Note(title=titulo, content=detalhes)
        db.add(nova_nota)

        return build_response(code=303, reason='See Other', headers='Location: /')

    return render_index()

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

def edit(request):
    route = extract_route(request)
    note_id = int(route.split('/')[-1])

    if request.startswith('POST'):
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

    nota = db.get(note_id)
    body = load_template('edit.html').format(id=nota.id, title=nota.title, content=nota.content)
    return build_response(body=body)

def not_found(request):
    body = load_template('404.html')
    return build_response(code=404, reason='Not Found', body=body)

def favorite(request):
    route = extract_route(request)
    note_id = int(route.split('/')[-1])
    db.toggle_favorite(note_id)

    return build_response(code=303, reason='See Other', headers='Location: /')

def render_index(error=''):
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=nota.title,details=nota.content,id=nota.id,favorite_icon='fav.png' if nota.favorite else 'notfav.png',)
        for nota in db.get_all()
    ]
    notes = '\n'.join(notes_li)

    error_html = f'<p class="form-error">{error}</p>' if error else ''

    # [SIMULADO 1.2] ✅ sem JS → o PYTHON sorteia. Cada carregamento = novo GET = sorteio novo.
    # Sorteio no render_index porque é ele que monta a home (GET normal e validação).
    cores = ['#DAF7A6', '#FFC300', '#FF5733', '#C70039', '#900C3F', '#581845']   # 6 cores diferentes
    cor = random.choice(cores)                                                   # item aleatório

    # ✅ cor=cor preenche o buraco {cor} do index.html (faltando → KeyError: 'cor')
    body = load_template('index.html').format(notes=notes, error=error_html, cor=cor)
    return build_response(body=body)

# [SIMULADO 1.1] ✅ view da rota /hoje/agora
# 📖 README_SIMULADO → "Quando pedirem uma página nova com um valor do Python"
def data(request):
    # Os espaços em "locale . setlocale ( ..." vieram da cópia do PDF. Funciona igual,
    # mas o normal é sem espaço: locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    locale . setlocale ( locale . LC_TIME , 'pt_BR.UTF-8')
    hoje = datetime . datetime . now ()
    # Formata a data por extenso
    # ⚠ AJUSTE 1: o enunciado pede "data E HORA" → acrescentei ', %H:%M' (hora:minuto).
    # ⚠ AJUSTE 2: '%A , %d' tinha um espaço antes da vírgula (veio do PDF) → 'segunda-feira , 28'.
    #   Era: hoje.strftime('%A , %d de %B de %Y')
    data_em_extenso = hoje.strftime('%A, %d de %B de %Y, %H:%M')
    # ✅ data=... preenche o buraco {data} do data.html (nome do buraco = nome no .format)
    body = load_template('data.html').format(data=data_em_extenso)
    return build_response(body=body) 