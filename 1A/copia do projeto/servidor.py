# =============================================================================
# servidor.py — O ROTEADOR
# Recebe cada requisição do navegador, descobre a rota e chama a função
# certa do views.py. NÃO tem lógica de página aqui (requisito do A+).
# 📖 README_1A.md → "Parte 0 — A base: servidor.py e utils.py"
# =============================================================================

# ---- IMPORTS ----------------------------------------------------------------
import socket                  # biblioteca de rede: deixa o programa "ouvir" a porta 8080
from pathlib import Path       # para montar caminhos de arquivos/pastas
from utils import extract_route, read_file, build_response
# ⚠ Toda função NOVA do views.py precisa ser adicionada nesta linha,
#   senão o servidor não enxerga ela. (README → Parte 0 → "Rota nova")
from views import index, delete, edit, confirm_delete, not_found, favorite

# ---- CONFIGURAÇÕES ----------------------------------------------------------
CUR_DIR = Path(__file__).parent  # pasta onde este arquivo está (a pasta do projeto)
SERVER_HOST = '0.0.0.0'          # aceita conexões por qualquer endereço desta máquina
SERVER_PORT = 8080               # porta → por isso o site abre em localhost:8080

# ---- LIGANDO O SERVIDOR (🔹 só reconhecer, nunca muda) -----------------------
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # cria o socket (IPv4 + TCP)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # evita "Address already in use" ao reiniciar
server_socket.bind((SERVER_HOST, SERVER_PORT))                       # prende o socket no endereço:porta
server_socket.listen()                                               # começa a esperar conexões

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

# ---- LOOP PRINCIPAL: cada volta = UMA requisição ------------------------------
# Para parar o servidor: Ctrl+C no terminal.
while True:
    # Fica PARADO aqui até um navegador conectar.
    # client_connection = canal com esse navegador (lê o pedido e manda a resposta)
    client_connection, client_address = server_socket.accept()

    # Lê até 1024 bytes da requisição e converte bytes → string
    request = client_connection.recv(1024).decode()

    # Imprime a requisição no terminal → MELHOR FERRAMENTA DE DEBUG
    # (mostra o método GET/POST, a rota e, no POST, o corpo com os dados)
    print('*'*100)
    print(request)

    # "GET /edit/3 HTTP/1.1" → 'edit/3'   |   "GET / HTTP/1.1" → ''
    route = extract_route(request)

    # O "/" do Path JUNTA caminhos (não é divisão): pasta_do_projeto/edit/3
    filepath = CUR_DIR / route

    # ---- ROTEAMENTO (🔸 precisa entender) -------------------------------------
    # Testado de cima para baixo; para no PRIMEIRO que for verdadeiro.
    # Rota nova entra como um elif ANTES do else.
    if filepath.is_file():
        # Arquivo estático que existe (getit.css, getit.js, img/...).
        # Vem PRIMEIRO porque, ao abrir a home, o navegador também pede CSS/JS/imagens.
        # build_response() sem argumentos = cabeçalho "200 OK" (bytes) + conteúdo do arquivo (bytes)
        response = build_response() + read_file(filepath)
    elif route == '':
        # Página principal (GET mostra a lista | POST cria nota)
        # 📖 README → Parte 1 (templates) e Parte 6 (validação)
        response = index(request)
    elif route.startswith('delete/'):
        # startswith porque a rota carrega o id: 'delete/3', 'delete/15'...
        # MESMA rota, duas ações dependendo do método:
        # 📖 README → Parte 3 — Apagar anotações
        if request.startswith('POST'):
            response = delete(request)          # clicou "Sim" (form method="post") → apaga
        else:
            response = confirm_delete(request)  # clicou na lixeira (link = GET) → página "tem certeza?"
    elif route.startswith('edit/'):
        # Aqui o GET/POST é separado DENTRO da função edit
        # 📖 README → Parte 4 — Editar anotações
        response = edit(request)
    elif route.startswith('fav/'):
        # 📖 README → Parte 6 — Favoritar
        response = favorite(request)
    else:
        # Nenhuma rota bateu → página 404 (com código HTTP 404)
        # 📖 README → Parte 5 — Página 404
        response = not_found(request)

    # Envia a resposta (PRECISA ser bytes → por isso toda view retorna build_response)
    client_connection.sendall(response)

    # Fecha a conexão com esse navegador e volta para o accept()
    client_connection.close()

# Na prática nunca chega aqui (o while True só para com Ctrl+C)
server_socket.close()
