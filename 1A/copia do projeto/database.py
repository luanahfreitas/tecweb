# =============================================================================
# database.py — O BANCO DE DADOS (SQLite)
# O banco mora inteiro no arquivo banco.db, com a tabela "note":
#     id | title | content | favorite
# Zerar as notas: parar o servidor e apagar banco.db (é recriado sozinho).
# 📖 README_1A.md → "Parte 2 — Persistência de dados (SQLite)"
# =============================================================================

import sqlite3
from dataclasses import dataclass


# -----------------------------------------------------------------------------
# Note — o "formato" de uma nota no Python
# @dataclass = atalho para uma classe que só guarda dados.
# Criar: Note(title='Mercado', content='Comprar leite')
# Usar:  nota.id, nota.title, nota.content, nota.favorite
# Valores depois do = são o padrão, se não passar.
# -----------------------------------------------------------------------------
@dataclass
class Note:
    id: int = None          # None = ainda não está no banco (o banco gera o id no INSERT)
    title: str = None
    content: str = ''
    favorite: bool = False  # A+ (no banco vira 0/1)


# -----------------------------------------------------------------------------
# Database — todas as operações no banco
# Métodos que ALTERAM (add, update, delete, toggle_favorite): execute + commit
# Métodos que LEEM (get_all, get): execute + for/fetchone (sem commit)
# ⚠ O SQL é montado grudando strings → apóstrofo no texto (Copo d'água) quebra o comando
# -----------------------------------------------------------------------------
class Database:
    def __init__(self, nome):
        # Roda em Database('banco'): abre (ou cria) banco.db
        self.conn = sqlite3.connect(nome + '.db')
        # Cria a tabela SÓ se ela ainda não existe.
        # id INTEGER PRIMARY KEY → gerado sozinho (1, 2, 3...)
        # favorite INTEGER DEFAULT 0 → coluna do A+ (0 = não, 1 = sim)
        # ⚠ Coluna nova aqui NÃO altera tabela que já existe → apagar banco.db (📖 README → Parte 6)
        self.conn.execute("CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL, favorite INTEGER DEFAULT 0);")

    def add(self, note):
        # INSERT: adiciona uma linha (id e favorite ficam com o padrão)
        self.conn.execute("INSERT INTO note (title, content) VALUES ('" + note.title + "', '" + note.content + "');")
        self.conn.commit()   # commit = SALVAR. Sem ele a mudança some.

    def get_all(self):
        # SELECT de todas as notas → lista de Note
        notes = []
        # ORDER BY favorite DESC → favoritas (1) antes das outras (0)   [A+]
        #          , id ASC      → desempate: ordem de criação
        cursor = self.conn.execute("SELECT id, title, content, favorite FROM note ORDER BY favorite DESC, id ASC")
        for linha in cursor:
            # linha = tupla na MESMA ordem das colunas do SELECT: (id, title, content, favorite)
            notes.append(Note(id=linha[0], title=linha[1], content=linha[2], favorite=bool(linha[3])))
        return notes

    def update(self, entry):
        # UPDATE ... WHERE id → altera SÓ a nota com esse id (entry precisa ter id!)
        # ⚠ UPDATE sem WHERE alteraria a tabela inteira
        self.conn.execute("UPDATE note SET title = '" + entry.title + "', content = '" + entry.content + "' WHERE id = " + str(entry.id) + ";")
        self.conn.commit()

    def delete(self, note_id):
        # DELETE ... WHERE id → apaga SÓ essa nota (⚠ sem WHERE apagaria tudo)
        self.conn.execute("DELETE FROM note WHERE id = " + str(note_id) + ";")
        self.conn.commit()

    def get(self, note_id):
        # Método pedido na tarefa 4 (editar): recebe id, devolve UM Note
        # 📖 README → Parte 4 → "database.py"
        cursor = self.conn.execute("SELECT id, title, content, favorite FROM note WHERE id = " + str(note_id) + ";")
        linha = cursor.fetchone()   # primeira linha do resultado, ou None se não achou
        if linha is None:
            return None
        return Note(id=linha[0], title=linha[1], content=linha[2], favorite=bool(linha[3]))

    def toggle_favorite(self, note_id):
        # A+: "interruptor" → cada chamada inverte o estado
        # 📖 README → Parte 6 → "1. Favoritar"
        nota = self.get(note_id)                    # busca o estado atual
        novo_valor = 0 if nota.favorite else 1      # ternário: era favorita → 0, senão → 1
        self.conn.execute("UPDATE note SET favorite = " + str(novo_valor) + " WHERE id = " + str(note_id) + ";")
        self.conn.commit()
