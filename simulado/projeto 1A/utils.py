import json
from pathlib import Path
 
CUR_DIR = Path(__file__).parent

def extract_route(request):
    first_line = request.split('\n')[0]
    route = first_line.split(' ')[1]
    return route[1:]
 
def read_file(filepath):
    with open(filepath, 'rb') as f:
        return f.read()

def load_data(filename):
    filepath = CUR_DIR / 'data' / filename
    with open(filepath, encoding='utf-8') as f:
        return json.load(f)

def load_template(filename):
    filepath = CUR_DIR / 'templates' / filename
    with open(filepath, encoding='utf-8') as f:
        return f.read()

def add_note(titulo, detalhes):
    filepath = CUR_DIR / 'data' / 'notes.json'
    notas = load_data('notes.json')
    notas.append({'titulo': titulo, 'detalhes': detalhes})
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(notas, f, ensure_ascii=False, indent=2)

def build_response(body='', code=200, reason='OK', headers=''):
    if isinstance(body, str):
        body = body.encode()

    response_line = f'HTTP/1.1 {code} {reason}\n'
    if headers:
        headers = headers + '\n'
    response = response_line + headers + '\n'
    return response.encode() + body