import socket
from pathlib import Path
from utils import extract_route, read_file, build_response
# [SIMULADO 1.1] ✅ função nova 'data' adicionada no import (sem isso o servidor não enxerga a função)
# 📖 README_SIMULADO → "Quando pedirem uma página nova"
from views import index, delete, edit, confirm_delete, not_found, favorite, data

CUR_DIR = Path(__file__).parent
SERVER_HOST = '0.0.0.0'
# ⚠ Porta 8000 (não 8080 como no enunciado) → avisar a professora antes da prova
#   (1A e 1B não rodam juntos: para o 1B usar python manage.py runserver 8001)
SERVER_PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    print('*'*100)
    print(request)

    route = extract_route(request)

    filepath = CUR_DIR / route
    if filepath.is_file():
        response = build_response() + read_file(filepath)
    elif route == '':
        response = index(request)
    elif route.startswith('delete/'):
        if request.startswith('POST'):
            response = delete(request)
        else:
            response = confirm_delete(request)
    elif route.startswith('edit/'):
        response = edit(request)
    elif route.startswith('fav/'):
        response = favorite(request)
    # [SIMULADO 1.1] ✅ rota nova: '==' porque é fixa (sem id), sem a barra do começo, ANTES do else
    elif route == 'hoje/agora':
        response = data(request)
    else:
        response = not_found(request)

    client_connection.sendall(response)

    client_connection.close()

server_socket.close()